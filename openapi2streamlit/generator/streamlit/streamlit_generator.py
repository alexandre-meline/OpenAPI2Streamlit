from jinja2 import Environment, FileSystemLoader
import os

def generate_streamlit_component(endpoint, details, base_url, output_dir="output/"):
    """Generates a Streamlit file for a given endpoint"""
    
    env = Environment(loader=FileSystemLoader("openapi2streamlit/templates"))
    template = env.get_template("streamlit_component.jinja")
    
    output = template.render(
        endpoint=endpoint,
        parameters=details["parameters"],
        method=details["method"],
        base_url=base_url
    )

    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{output_dir}streamlit_{endpoint.replace('/', '_')}.py"
    
    with open(file_name, "w") as f:
        f.write(output)
    
    print(f"[✅] Fichier généré : {file_name}")

