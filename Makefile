clean:
	cd ../my_django_project && docker compose down -v --remove-orphans --rmi local || true
	cd .. && rm -Rf my_django_project || true

test: clean
	cd .. && cookiecutter dj-on --no-input
