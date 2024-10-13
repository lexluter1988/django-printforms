deps:
	pip-compile requirements.in
	pip-sync requirements.txt
