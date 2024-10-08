version = "latest"

build/main-container-id: .github/Dockerfile
	mkdir -p build/
	docker build . \
      --rm \
      --file .github/Dockerfile \
      --tag "ghcr.io/woregnets/build:${version}" > $@

venv:
	python -m venv venv/
	
.PHONY: test
test: tests/ venv 
	python -m unittest discover -s $< -p "*_test.py"

.PHONY: build 
build: woregnets
	python -m woregnets $@

node_modules:
	pnpm install 
	
build/dist: build node_modules
	pnpm run build
	mv build/dist/build/html/index.html build/dist
	rm -r build/dist/build/