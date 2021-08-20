venv:
	pyenv install 3.8.7 --skip-existing
	pyenv virtualenv 3.8.7 tnm --force
	pyenv local tnm

show:
	python Show_Maker.py

lint:
	black . --check

tests:
	pytest