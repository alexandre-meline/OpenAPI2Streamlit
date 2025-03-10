import argparse
from openapi2streamlit.openapi_parser.loader import load_openapi_schema
from openapi2streamlit.openapi_parser.extractor import (
    extract_info, extract_endpoints, get_endpoint_with_data
    )
from openapi2streamlit.generator.streamlit.streamlit_baseapp_generator import (
    generate_streamlit_baseapp_component
    )
from openapi2streamlit.generator.streamlit.streamlit_generator import generate_streamlit_component
from openapi2streamlit.generator.streamlit.streamlit_api_generator import generate_streamlit_api_component


def main():
    parser = argparse.ArgumentParser(description="Streamlit Component Generator from OpenAPI")

    parser.add_argument("openapi_file", help="OpenAPI file path (JSON or YAML)")
    parser.add_argument("--base-url", default="https://api.example.com", help="API Base URL")
    parser.add_argument("--output", default="output/", help="Output folder for generated files")

    args = parser.parse_args()

    # Load and parse OpenAPI schema
    schema = load_openapi_schema(args.openapi_file)
    api_infos = extract_info(schema)
    endpoints = extract_endpoints(schema)

    # Generates the basic architecture of the application
    generate_streamlit_baseapp_component(api_infos, args.base_url, args.output)

    # Generate components for the Streamlit project's api folder
    api_files_paths = []
    for endpoint, details in endpoints.items():
        endpoint_datas = get_endpoint_with_data(endpoint, details, schema)

        file_path = generate_streamlit_api_component(endpoint_datas, args.output)
        api_files_paths.append(file_path)
    print(f"[📦] Files Generated: {api_files_paths}")

    print(f"[🎉] Generation Completed! Files Available in {args.output}")

if __name__ == "__main__":
    main()
