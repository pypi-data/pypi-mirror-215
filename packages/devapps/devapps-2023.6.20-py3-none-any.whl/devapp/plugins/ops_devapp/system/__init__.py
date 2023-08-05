#!/usr/bin/env python
"""
# System Building
"""
# TODO: set up ssh -R to tinyproxy for airight deploys in ssh mode
import devapp.gevent_patched
from .tools import run_app, do, FLG, load_spec, app, g, waitfor, spawn, time, workdir, os
from .tools import write_file, read_file, out_table, api, have_all, partial, system
from .tools import exists, dir_of, now, json, organize_bzip2
from hashlib import md5
from shutil import copyfile


class Flags:
    autoshort = ''

    class cache_expiry:
        d = 600

    class user:
        n = 'leave empty to log in as user given in spec'
        d = ''

    class user_home_dir:
        n = 'leave empty to set /home/<user>'
        d = ''

    class dbg_non_parallel:
        n = 'Non parallel execution'
        d = False

    class system_spec:
        n = 'File which contains your system spec - absolute or relative to project root'
        d = 'conf/system.py'

    class node_mappings:
        n = ''
        d = ''

    class deploy_mode:
        t = ['ssh', 'infra_hetzner', 'k8s']
        d = 'ssh'

    class node:
        n = 'Node mapping'
        t = 'multi_string'

    class Actions:
        class deploy:
            d = True


class Node:
    name = None
    mem_gb_tot = None
    cores = None
    have_ssh_user_login = None

    def __repr__(self):
        return self.name


def make_instances(spec, api):
    """run all spec funcs"""

    def make_instance(f):
        host, n = f.split(':')
        N = g(spec, n, ('Not in spec', 'node'))
        n = type(n, (N, Node), {'ip': host, 'type': n})()
        n.name = f'Node {n.type} {n.ip}'
        N.instances = getattr(N, 'instances', [])
        n.nr = len(N.instances)
        N.instances.append(n)
        api.instances.append(n)

    [make_instance(f) for f in FLG.node]


def pull_private_pips(spec):
    pp = g(spec, 'priv_pips')
    if not pp:
        return pp
    d = f'{workdir}/pips'
    cmd = f"ops pkgs fetch --into {workdir}/priv_pips --private_pips '{pp}'"
    do(system, cmd)


def lc_hubs():
    hub = api.spec.hub
    p = int((hub.bind + ':1880').rsplit(':', 1)[-1])
    H = [f'{i.ip}:{p}' for i in api.instances if hub in i.svcs]
    return ','.join(H)


class deploy_modes:
    class ssh:
        @classmethod
        def deploy(ssh):
            api.spec = spec = load_spec()
            u = FLG.user or getattr(spec, 'user')
            setattr(FLG, 'user', u)
            pull_private_pips(spec)
            make_instances(spec, api)
            [spawn(ssh.run_get_resources, host) for host in api.instances]
            waitfor('check host resources', partial(have_all, lambda n: n.mem_gb_tot))
            out_table('mem_gb_tot', 'cores')
            if any([h for h in api.instances if not h.have_bzip2]):
                do(organize_bzip2)
            [spawn(ssh.run_install_mamba, host) for host in api.instances]

        @classmethod
        def run_get_resources(ssh, host):
            cmds = [
                'cat /proc/meminfo',
                'cat /proc/cpuinfo',
                'ls $HOME/.cache/priv_pips 2>/dev/null',
                'type bzip2',
            ]
            res = ssh.run_cmd(cmds, host)
            _ = res[0].split('MemTotal:', 1)[1].split('\n', 1)[0]
            _ = _.replace(' kB', '').strip()
            host.mem_gb_tot = int(int(_) / 1024 / 1024 + 0.5)
            host.cores = len(('\n' + res[1]).split('\nprocessor')) - 1
            host.have_priv_pips = res[2]
            host.have_bzip2 = res[3]

        @classmethod
        def run_install_mamba(ssh, host):
            scp_files(host)
            cmds = ['chmod +x installer.sh', './installer.sh']
            breakpoint()   # FIXME BREAKPOINT
            res = ssh.run_cmd(cmds, host)

        @classmethod
        def run_cmd(ssh, cmds, host, as_root=False, sep='!!cmd output!!'):
            def arr(res):
                return [i.strip() for i in res.split(sep)[1:]]

            nfo = app.warn if as_root else app.debug

            nfo(f'ssh {ssh_user(as_root)} {host.ip}', host=host, cmds=cmds)

            h = md5(str(cmds).encode('utf-8')).hexdigest()
            dw = f'{workdir}/{host.ip}/{h}'
            fn = f'{dw}/cmd'
            fnr = f'{dw}/cmd.res'
            fnt = f'{dw}/cmd.ts'
            os.makedirs(dw, exist_ok=True)
            if now() - float(read_file(fnt, '0')) < FLG.cache_expiry:
                nfo('from cache')
                return arr(read_file(fnr))

            t = ['#!/usr/bin/env bash']
            for cmd in cmds:
                t.append(f'echo "{sep}"')
                t.append(cmd)
            write_file(fn, '\n'.join(t))
            os.unlink(fnr) if exists(fnr) else 0
            cmd = f'cat "{fn}" | {SSH} {ssh_user(as_root)}@{host.ip} > {fnr}'
            os.popen(cmd).read()
            res = read_file(fnr).strip()
            if not res:
                if host.have_ssh_user_login:
                    msg, kw = ('Could not log in', dict(host=host, cmds=cmds, user=user))
                    raise Exception(msg, kw)
                host.have_ssh_user_login = True
                ssh.create_user(host=host)
                return ssh.run_cmd(cmds, host)
            write_file(fnt, str(now()))
            return arr(res)

        @classmethod
        def create_user(ssh, host):
            user = FLG.user
            d = FLG.user_home_dir or f'/home/{user}'
            app.info('Creating user', user=user, host=host)
            cmds = [
                f'adduser --home-dir {d} {user}',
                f'mkdir -p {d}/.ssh',
                f'cp -a /root/.ssh/authorized_keys {d}/.ssh/',
                f'chown -R {user}:{user} {d}/.ssh/',
            ]
            ssh.run_cmd(cmds, host=host, as_root=True)


SSH = 'ssh -q -o PasswordAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'


def scp_files(host):
    """identify files to send and scp using our ssh with a pipe"""
    files = []   # will copy
    pips = json.loads(read_file(f'{workdir}/priv_pips/pips.json', '{}')).values()
    dw = f'{workdir}/{host.ip}'
    dirs = [dw + '/.cache', dw + '/.cache/priv_pips', dw + '/.local/bin']
    [os.makedirs(d, exist_ok=True) for d in dirs]

    def cp(fn):
        if not exists(f'{dw}/{fn}'):
            copyfile(f'{workdir}/{fn}', f'{dw}/.cache/{fn}')
        return '.cache/' + fn

    files += [cp(f'priv_pips/{p}') for p in pips if not p in host.have_priv_pips]

    g = lambda k: getattr(api.spec, k, '')
    T = read_file(dir_of(__file__) + '/templates/inst_base.sh')
    ctx = {
        'node': f'{host.type}.{host.nr}',
        'lc_hubs': lc_hubs(),
        'd_project': g('d_project'),
        'app_libs': g('app_libs'),
    }
    write_file(f'{dw}/installer.sh', T % ctx)
    files.append('installer.sh')
    if not host.have_bzip2:
        copyfile(f'{workdir}/static/bzip2', f'{dw}/.local/bin/bzip2')
        files.append('.local/bin/bzip2')
    f = ' '.join(files)
    cmd = f'cd "{dw}"; tar cfvz - {f} | {SSH} {ssh_user()}@{host.ip} tar xfz -'
    err = os.system(cmd)
    if err:
        raise Exception('scp error', {'files': files, 'host': host})


def ssh_user(as_root=False):
    return 'root' if as_root else FLG.user


def run():
    os.makedirs(workdir, exist_ok=True)
    if FLG.deploy:
        return do(getattr(deploy_modes, FLG.deploy_mode).deploy)


main = lambda: run_app(run, flags=Flags)


if __name__ == '__main__':
    main()


# begin_archive
# # # Could be done far smaller.
# from re import match
# from devapp import gevent_patched
# import hashlib
# import json
# import os
# import shutil
# from copy import deepcopy
# from functools import partial
#
# import requests

# from devapp import tools
# from devapp.tools import (
#     exists,
#     to_list,
#     repl_dollar_var_with_env_val,
#     project,
#     read_file,
#     write_file,
# )
# import devapp.tools.resource as api
#
