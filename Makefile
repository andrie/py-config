
.PHONY: docs test

docs:
	cd docs && python -m quartodoc build --verbose
	cd docs && quarto render

test: 
	pytest -v