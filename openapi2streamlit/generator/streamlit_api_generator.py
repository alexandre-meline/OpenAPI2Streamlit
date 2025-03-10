import os
from jinja2 import Environment, FileSystemLoader
from openapi2streamlit.generator.utils import (
    generate_init_file, 
    generate_creation_file_info
    )


def type_serialization(prop):
    """Serialize the type of a property."""
    if prop.get("type") == "string":
        if prop.get("format") == "decimal":
            return "float"
        return "str"
    if prop.get("type") == "integer":
        return "int"
    if prop.get("type") == "number":
        return "float"
    if prop.get("type") == "boolean":
        return "bool"
    if prop.get("type") == "array":
        return "list"
    if prop.get("type") == "object":
        return "dict"
    return "str"


def format_parameters_for_signature(data: dict, parameters: list = []) -> str:
    """Format the data into a parameter signature for the function."""
    if parameters and not data:
        return ", ".join(
            f"{p['name']}: {type_serialization(p['schema'])}"
            for p in parameters
        )
    
    elif data:
        return ", ".join(
            f"{k}: {type_serialization(v)}"
            for k, v in data.items()
        )
    
    else:
        return ""


def format_json_data(data):
    """Formats the JSON data to be passed to the API call"""
    if not data:
        return ""
    return ",\n        ".join(f'"{k}": {k}' for k in data.keys())


def format_fonc_params_description(data: dict) -> str:
    """
    Formats the parameter description from a data dictionary.
    """
    if not data:
        return ""
    
    descriptions = []
    for param_name, properties in data.items():
        param_type = properties.get('type', 'unknown')
        param_format = properties.get('format', '')
        description = properties.get('description', '')

        if param_format:
            param_type = f"{param_type} ({param_format})"
        param_desc = f"\t- **{param_name}** ({param_type})"
        
        if description:
            param_desc += f": {description}"
        
        constraints = []
        if 'maxLength' in properties:
            constraints.append(f"max longueur: {properties['maxLength']}")
        if 'format' in properties:
            constraints.append(f"format: {properties['format']}")
        if 'enum' in properties:
            constraints.append(f"options: {', '.join(properties['enum'])}")
        
        if constraints:
            param_desc += f" [{'; '.join(constraints)}]"
        
        descriptions.append(param_desc)
    
    return "\n".join(descriptions)


def generate_streamlit_api_folder(output_dir: str, group_request_name: str):
    """Generates the folder for the API components."""
    folder = f"{output_dir}api/{group_request_name}/"
    os.makedirs(folder, exist_ok=True)
    generate_init_file(folder)
    return folder


def format_responses(responses: dict) -> str:
    """Formats the responses for the API call."""
    response_str = ""
    for status_code, response in responses.items():
        response_str += f"if response.status_code == {status_code}:\n"
        response_str += f"        return response.json()\n"
        response_str += "    return None\n"
    return response_str


def generate_streamlit_api_component(endpoint_data: dict, output_dir: str = "output/"):
    """Generates a Python file for a given endpoint with an API call."""
    env = Environment(loader=FileSystemLoader("openapi2streamlit/templates"))
    template = env.get_template("streamlit_api_component.jinja")

    group_request_name = endpoint_data["name"]
    responses = endpoint_data["responses"]
    function_name = endpoint_data["type"]
    endpoint = endpoint_data["endpoint"]
    method = endpoint_data["method"].lower()
    data = endpoint_data["data"]
    parameters = endpoint_data["parameters"]
    
    folder = generate_streamlit_api_folder(output_dir, group_request_name)
    
    parameters_signature = format_parameters_for_signature(data, parameters)
    responses_format = format_responses(responses)
    function_params_description = format_fonc_params_description(data)
    json_data = format_json_data(data)
    
    output = template.render(
        function_name=function_name,
        responses_format=responses_format,
        endpoint=endpoint,
        method=method,
        parameters_signature=parameters_signature,
        function_params_description=function_params_description,
        json_data=json_data
    )
    
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{folder}{function_name}.py"
    with open(file_name, "w") as f:
        f.write(output)
    
    generate_creation_file_info(file_name)

