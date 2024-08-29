venv:
	python -m venv venv/
	
.PHONY: test
test: tests/ venv 
	python -m unittest discover -s $< -p "*_test.py"
	
generate: venv woregnets
	python -m woregnets build/ 