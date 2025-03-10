import json
import yaml


def load_openapi_schema(file_path):
    """Loads an OpenAPI file (JSON or YAML)"""
    with open(file_path, "r") as f:
        if file_path.endswith(".json"):
            return json.load(f)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported format: JSON or YAML only.")
