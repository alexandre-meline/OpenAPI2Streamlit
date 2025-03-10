import os
import re
from jinja2 import Environment, FileSystemLoader


def generate_creation_file_info(file_name: str):
    """Prints a message when a file is generated"""
    print(f"[✅] Generation of the file {file_name} completed.")


def generate_error_file_info(file_name: str):
    """Prints an error message when a file is not generated"""
    print(f"[❌] Error during the generation of the file {file_name}.")


def generate_requirements_file(output_dir):
    """Generates an requirements.txt file"""
    with open(f"{output_dir}requirements.txt", "w") as f:
        f.write("streamlit\n")
        f.write("python-dotenv\n")
        f.write("requests\n")

        file_name = f"{output_dir}requirements.txt"
        generate_creation_file_info(file_name)


def generate_env_file(base_url, output_dir):
    """Generates an .env file"""
    env = Environment(loader=FileSystemLoader("openapi2streamlit/templates/streamlit/"))
    template = env.get_template("env_file.jinja")

    output = template.render(
        base_url=base_url
    )

    file_name = f"{output_dir}.env"

    with open(file_name, "w") as f:
        f.write(output)

    generate_creation_file_info(file_name)


def generate_init_file(output_dir):
    """Generates an __init__.py file"""
    if os.path.exists(f"{output_dir}__init__.py"):
        return
    with open(f"{output_dir}__init__.py", "w") as f:
        f.write("")
        
        file_name = f"{output_dir}__init__.py"
        generate_creation_file_info(file_name)


def serialize_path_to_import(output_dir: str, path: str, func_name: str):
    """Serialize """
    from_import = path.strip(f"{output_dir}/").replace('/', '.').replace('.py', '')
    return f"from {from_import} import {func_name}"

def generate_streamlit_component_folder(output_dir: str, sub_folder: str, group_request_name: str):
    """Generates the folder for the components."""
    folder = f"{output_dir}{sub_folder}{group_request_name}/"
    os.makedirs(folder, exist_ok=True)
    generate_init_file(folder)
    return folder

def add_tabulation_to_multiline_string(tab: str = "\t", multi_line_string: str = "") -> str:
    """
    Adds a tab to the beginning of each line of a multi-line string.
    """
    lines = multi_line_string.split("\n")

    tabulated_lines = [f"{tab}{line.strip()}" for line in lines]
    
    tabulated_string = "\n".join(tabulated_lines)
    
    return tabulated_string

def generate_streamlit_fields(args_str: str):
    """
    Generates Streamlit fields based on the provided arguments with their type.

    :param args_str: String containing the arguments and their type (ex: 'id: int, name: str, amount: float')
    :return: Jinja code generating the Streamlit fields
    """
    type_mapping = {
        "int": 'st.number_input("{label}", min_value=1, step=1)',
        "float": 'st.number_input("{label}", min_value=0.0, format="%.2f")',
        "str": 'st.text_input("{label}")'
    }

    pattern = r"(\w+):\s*(\w+)"
    matches = re.findall(pattern, args_str)

    fields_code = []
    first_iteration = True
    for arg_name, arg_type in matches:
        tab_prefix = "        " if not first_iteration else ""
        label = arg_name.replace("_", " ").capitalize()
        field_code = type_mapping.get(arg_type, 'st.text_input("{label}")')
        field = f"{tab_prefix}{label.replace(' ', '_').lower()} = {field_code.format(label=label)}"
        fields_code.append(field)
        first_iteration = False

    return "\n".join(fields_code)
