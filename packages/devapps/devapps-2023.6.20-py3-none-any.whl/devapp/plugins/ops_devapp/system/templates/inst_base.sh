#!/usr/bin/env bash
# wget <url> | bash  OR source (not run)

set -a
node="%(node)s"
lc_hubs="%(lc_hubs)s"
app_libs="%(app_libs)s"
d_project="%(d_project)s"
PATH="$HOME/.local/bin:$PATH"
set +a

# anything we copied here before is exe:
chmod +x "$HOME/.local/bin/"*

#inst_url="$inst_protocol://$inst_host"
function d_artifacts { echo "$MAMBA_ROOT_PREFIX/artifacts/hubpkgs"; }

function sh {
    echo -e "🟩 $*k"
    eval "$*"
}
function die {
    echo -e "🟥 $*"
    exit 1
}
function activate_home_base {
    . "$HOME/.bashrc"
    #. micromamba/etc/profile.d/micromamba.sh
    micromamba activate base
}
function check_bootstrapped {
    micromamba activate 2>/dev/null && return 0 # e.g. mamba docker container
    test -e "$HOME/micromamba" && activate_home_base && echo "Mamba activated: $MAMBA_ROOT_PREFIX" && return 0
    return 1
}
function install_bzip {
    test "$UID" == "0" || {
        echo "Please install bzip2 as root"
        exit 1
    }
    type apt-get && {
        apt-get update
        apt-get install bzip2 && return 0
    }
    type yum && { yum install -y bzip2 && return; }
    exit 1
}
function bootstrap {
    type bzip2 || install_bzip
    builtin cd
    curl micro.mamba.pm/install.sh | bash
    activate_home_base
}
function ensure_channel {
    echo -e 'channels:\n  - conda-forge\n' >"$HOME/.condarc"
}
function ensure_mm {
    local h="$HOME/.bashrc"
    local line='function mm { micromamba "$@"; }'
    grep "$line" <"$h" && return 0
    echo "$line" >>"$h"
    source "$h"
}
function ensure_base_tools {
    local t r="$MAMBA_ROOT_PREFIX"
    test -z "$r" && {
        echo "No mamba"
        exit 1
    }
    local pkgs=""
    micromamba list >pkgs
    tools="python $app_libs"
    for t in git curl gcc jq fzf; do type "$t" || tools="$tools $t"; done
    for t in $tools; do grep "$t" <pkgs || pkgs="$t $pkgs"; done
    test -n "$pkgs" || return 0
    sh micromamba install --quiet -y "$pkgs" && return 0
    die "failure pkgs install $pkgs"
}

function ensure_lc_app_pkg {
    #local pips="$(pip list)"
    set -x
    d="$HOME/.cache/priv_pips"
    pip install --find-links="$d" "$d_project" && return 0
    die "pip failed. libs missing?"
}

function connect {
    mkdir -p "$d_project"
    cd "$_"
    git init
    curl "$inst_url/system.py" >system.py
    export PYTHONPATH="$d_project"
    app client --lc_hubs="$inst_host" --lc_tabs=System --lc_client_name="system:$node" -cf=system:System -ll 10
}

function main {
    sh check_bootstrapped || bootstrap
    sh ensure_channel
    sh ensure_mm
    sh activate_home_base
    sh ensure_base_tools
    sh ensure_lc_app_pkg
    sh connect
}

main "$@"
