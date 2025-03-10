def extract_info(schema):
    """Extract general information from the API"""
    return {
        "title": schema.get("info", {}).get("title"),
        "description": schema.get("info", {}).get("description"),
        "version": schema.get("info", {}).get("version"),
    }

def resolve_ref(ref_path, schema):
    """Resolve a JSON reference in the OpenAPI schema."""
    parts = ref_path.lstrip('#/').split('/')
    ref = schema
    for part in parts:
        ref = ref.get(part, {})
    return ref

def extract_data_for_endpoint(endpoint_details, schema):
    """Extracts and resolves the necessary data from a given endpoint."""
    request_body = endpoint_details.get('requestBody', {}).get('content', {})

    ref = None
    for content_type, content_schema in request_body.items():
        if content_type == 'application/json':
            ref = content_schema.get('schema', {}).get('$ref')
            if ref:
                break
    if not ref:
        return None
    
    component_schema = resolve_ref(ref, schema)

    component_data = {}
    for name, prop in component_schema.get('properties', {}).items():
        component_data[name] = prop
        if prop.get('$ref'):
            resolved_ref = resolve_ref(prop['$ref'], schema)
            component_data[name] = resolved_ref
            
    return component_data
    
def get_endpoint_with_data(endpoint, endpoint_details, schema):
    """Returns the endpoint with the necessary data."""
    data = extract_data_for_endpoint(endpoint_details, schema)
    return {
        'name': endpoint_details.get('name'),
        'responses': endpoint_details.get('responses'),
        'type': endpoint_details.get('requestType'),
        'endpoint': endpoint.split('_')[0],
        'method': endpoint_details.get('method'),
        'parameters': endpoint_details.get('parameters'),
        'data': data
    }

def extract_endpoints(schema):
    """Extracts endpoints and their parameters."""
    endpoints = {}
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            endpoints[f"{path}_{method}"] = {
                "name": details.get("tags", [""])[0],
                "responses": details.get("responses"),
                "requestType": details.get("operationId"),
                "method": method,
                "parameters": details.get("parameters", []),
                "requestBody": details.get("requestBody", {})
            }
    return endpoints