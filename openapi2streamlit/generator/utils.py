import os
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