#!/bin/bash

if [ -z "$JENKINS_URL" ]; then
    echo "Running outside Jenkins with"
    rm -rf venv/
    virtualenv venv
    git clone -b feature/zdm_client_dumps ssh://git@repo.zerynth.com:10022/zerynth-core/zerynth-toolchain.git
    # TODO: python 3.5 must not be hardcoded
    cp -r ./zerynth-toolchain/zdevicemanager ./venv/lib/python3.6/site-packages/zdevicemanager
    rm -rf ./zerynth-toolchain
    . venv/bin/activate
    pip install -r requirements.txt

else
    rm -rf venv/
    #virtualenv -p python3 venv
    python3 -m venv venv

    git clone -b feature/zdm_client_dumps ssh://git@repo.zerynth.com:10022/zerynth-core/zerynth-toolchain.git

    cp -r ./zerynth-toolchain/zdevicemanager ./venv/lib/python3.5/site-packages/zdevicemanager

    . venv/bin/activate
    pip install -r requirements.txt

    # added beacuse the packege need a zerynth installation
    mkdir -p  /root/.zerynth2_test/cfg
    mkdir -p  /root/.zerynth2/cfg
    json='{"version": "r2.5.1"}'
    echo $json> /root/.zerynth2_test/cfg/config.json
    echo $json> /root/.zerynth2/cfg/config.json
    #rm -rf zerynth-toolchain
fi