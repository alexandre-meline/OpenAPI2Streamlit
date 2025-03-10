.PHONY: install run

install:
	poetry install

run:
	openapi2streamlit datas_test/schema.yaml --output "output/" --base-url "http://localhost:8000"

