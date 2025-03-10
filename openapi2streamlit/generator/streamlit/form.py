from jinja2 import Environment, FileSystemLoader
import os

from openapi2streamlit.generator.streamlit.utils import (
    serialize_path_to_import,
    generate_streamlit_fields,
    generate_creation_file_info,
    generate_streamlit_component_folder,
    add_tabulation_to_multiline_string
    )

"""
{
'group': 'accounts', 
'name': 'accounts_create', 
'path': 'output/api/accounts/accounts_create.py', 
'endpoint': '/api/accounts/', 
'args': 'id: int, account_type: str, name: str, initial_amout: float, actualy_amout: float, user: int', 
'json_data': '"id": id,\n        "account_type": account_type,\n        "name": name,\n        "initial_amout": initial_amout,\n        "actualy_amout": actualy_amout,\n        "user": user'}"""


def generate_streamlit_form_component(component_data: dict, 
                                      output_dir="output/"):
    """Generates a Streamlit file for a given endpoint"""

    env = Environment(loader=FileSystemLoader(
        "openapi2streamlit/templates/streamlit/components/"
        ))
    template = env.get_template("form.jinja")
    sub_folder = "components/"

    group_component = component_data.get('group', {})
    func_name = component_data.get('name', {})
    func_path = component_data.get('path', {})
    func_args = component_data.get('args', {})
    func_json_data = component_data.get('json_data', {})

    folder = generate_streamlit_component_folder(
        output_dir, sub_folder, group_component
        )

    import_file = serialize_path_to_import(output_dir, func_path, func_name)

    fields_form = generate_streamlit_fields(func_args)

    func_json_data = add_tabulation_to_multiline_string(func_json_data,
                                                        "\t\t\t\t")

    api_request = f"{func_name}(**data)"
    print(api_request)

    output = template.render(
        import_file=import_file,
        function_name=func_name,
        title=func_name,
        fields=fields_form,
        json_data=func_json_data,
        api_request=api_request
    )

    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{folder}{func_name}_form.py"
    with open(file_name, "w") as f:
        f.write(output)

    generate_creation_file_info(file_name)