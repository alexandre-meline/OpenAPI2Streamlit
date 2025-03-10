.PHONY: install run

install:
	poetry install

run:
	openapi2streamlit datas_test/schema.yaml --output "generated_files/" --base-url "http://localhost:8000"

