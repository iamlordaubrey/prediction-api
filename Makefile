# Variables
FLASK = flask

# Targets
.PHONY: help init db migrate upgrade seed run

help:
	@echo "Usage:"
	@echo "  make init      - Initialize the migrations directory"
	@echo "  make migrate   - Generate a new migration script"
	@echo "  make upgrade   - Apply the migrations to the database"
	@echo "  make setup   	- Setup the application. A combination of multiple commands"
	@echo "  make run       - Run the Flask application"

VENV := .venv

claen_venv:
	source deactivate || true
	rm -rf $(VENV)

$(VENV): clean_venv
	command -v deactivate && source deactivate || true
	python -m venv $(VENV)
	source $(VENV)/bin/activate && pip install --upgrade pip

init:
	$(FLASK) db init

migrate:
	$(FLASK) db migrate -m "Database tables setup"

upgrade:
	$(FLASK) db upgrade

setup_db:
	$(FLASK) db init
	$(FLASK) db migrate -m "Database tables setup"
	$(FLASK) db upgrade

seed:
	python seed.py

run:
	source $(VENV)/bin/activate \
	&& FLASK_APP=app.py FLASK_ENV=development $(FLASK) run

setup:
	test -r $(VENV) || MAKE $(VENV)
	source $(VENV)/bin/activate && pip install -r requirements.txt
	make setup_db || true
	make seed
	make run

spec=tests
runtests:
	source $(VENV)/bin/activate \
	&& PYTHONDONTWRITEBYTECODE=1 $(VENV)/bin/pytest -vvv '${spec}'
