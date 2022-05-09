#!/usr/bin/env bash

set -e

CUR_DIR=$(cd $(dirname "$0");pwd)
PROJECT_DIR=$(dirname $(dirname $CUR_DIR))

source $PROJECT_DIR/deploy/scripts/const.properties
cd ${PROJECT_DIR}

# install coordinator
python3 -m pip install $coordinator_whl \
                         --disable-pip-version-check

echo "Install NeurSafe FL Coordinator successfully."
