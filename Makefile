PYTHON ?= .venv/bin/python
GUNICORN ?= .venv/bin/gunicorn
PORT ?= 5000

.PHONY: install test quality run prod backup init

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -q

quality:
	$(PYTHON) scripts/content/quality_report.py

run:
	cd backend && $(PYTHON) app.py

prod:
	SECRET_KEY=$${SECRET_KEY:-replace-me} ADMIN_PASSWORD=$${ADMIN_PASSWORD:-replace-me} FLASK_DEBUG=0 PORT=$(PORT) $(GUNICORN) --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:$(PORT) wsgi:app

backup:
	$(PYTHON) scripts/ops/backup_db.py

init:
	bash scripts/db/init_db.sh
