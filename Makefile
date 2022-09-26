export PYTHONPATH=$(shell pwd)/src/

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log


install-dev-requirements: clean
	pip install -r requirements/dev.txt

safety-check: clean
	safety check

test-coverage: clean
	py.test -c ./src/unit_tests/pytest.ini ./src/unit_tests/

run-api: clean
	@uvicorn my_awesome_app.entrypoints.http_api.main:app --reload

make-migrations:
	PYTHONPATH=$(shell pwd)/src/ alembic --config alembic_migrations/alembic.ini revision --autogenerate

migrate:
	PYTHONPATH=$(shell pwd)/src/ alembic --config alembic_migrations/alembic.ini upgrade head
