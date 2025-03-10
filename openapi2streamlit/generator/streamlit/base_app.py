from jinja2 import Environment, FileSystemLoader
import os
from openapi2streamlit.generator.streamlit.utils import (
    generate_env_file, 
    generate_init_file, 
    generate_requirements_file, 
    generate_creation_file_info
    )

"""
api (folder)
│   ├── __init__.py
│   ├── {component1} (folder)
│   │   ├── __init__.py
│   │   ├── {component1}_endpoints.py
│   ├── {component2} (folder)
│   │   ├── __init__.py
│   │   ├── {component2}_endpoints.py
components (folder)
│   ├── __init__.py
│   ├── {component1} (folder)
│   │   ├── __init__.py
│   │   ├── {component1}_layout.py
│   ├── {component2} (folder)
│   │   ├── __init__.py
│   │   ├── {component2}_layout.py
run_app.py
.env
requirements.txt
"""

def generate_run_app_file(api_title="My app title", api_description="Welcome to the my app", api_version="0.1", output_dir="output/"):
    """Generate the run_app.py file"""
    env = Environment(loader=FileSystemLoader("openapi2streamlit/templates/streamlit/"))
    template = env.get_template("runapp_file.jinja")

    output = template.render(
        api_title=api_title,
        api_description=api_description,
        api_version=api_version
    )

    file_name = f"{output_dir}run_app.py"

    with open(file_name, "w") as f:
        f.write(output)
    
    generate_creation_file_info(file_name)


def generate_streamlit_baseapp_component(api_infos: dict, base_url:str, output_dir="output/"):
    """Generates the basic architecture of a Streamlit project"""

    # Create output folder
    os.makedirs(output_dir, exist_ok=True)

    # Generate the base api folders
    os.makedirs(f"{output_dir}api", exist_ok=True)

    # Generate the __init__.py files
    generate_init_file(f"{output_dir}api/")

    # Generate the base components folders
    os.makedirs(f"{output_dir}components", exist_ok=True)

    # Generate the __init__.py files
    generate_init_file(f"{output_dir}components/")
    
    # Generate the run_app.py file
    generate_run_app_file(api_infos["title"], api_infos["description"], api_infos["version"], output_dir)

    # Generate the .env file
    generate_env_file(base_url, output_dir)

    # Generate the requirements.txt file
    generate_requirements_file(output_dir)

    file_name = f"{output_dir}api"
    generate_creation_file_info(file_name)


