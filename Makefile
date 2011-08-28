.PHONY: lint pep8 pyflakes clean

lint: pep8 pyflakes

pep8:
	pep8 --repeat import.py

pyflakes:
	pyflakes import.py

clean:
	find . -name '*~' -o -name '*.pyc' -print0 | xargs -0 -r rm
