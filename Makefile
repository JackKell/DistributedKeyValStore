setup:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	pip install --target=./virtualenv/ virtualenv
	python ./virtualenv/virtualenv.py -p python3 env

	bash -c "source env/bin/activate; \
	pip install grpcio;"

	@echo ''
	@echo ''
	@echo 'Everythings Works'
	@echo 'Please run `source env/bin/activate`'

clean:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	rm -rf env
