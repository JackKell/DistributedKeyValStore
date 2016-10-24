setup:
    if [[ "$VIRTUAL_ENV" != "" ]]; then deactivate; fi
    pip install --target=./virtualenv/ virtualenv
    python ./virtualenv/virtualenv.py -p python3 env
    source env/bin/activate
    pip install grpcio

clean:
    if [[ "$VIRTUAL_ENV" != "" ]]; then deactivate; fi
    rm -rf env
