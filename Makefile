venv:
	python -m venv venv/
	
.PHONY: test
test: tests/ venv 
	python -m unittest discover -s $< -p "*_test.py"
	
generate: venv
	python -m woregnets build/ 
	