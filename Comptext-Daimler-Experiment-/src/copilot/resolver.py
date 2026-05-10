"""
Resolver – Support for comptext:// custom protocol resolving.
"""

def resolve_comptext_uri(uri: str) -> dict:
    """
    Resolves URIs like comptext://diagnostics/{id}
    """
    if not uri.startswith("comptext://"):
        return {"error": "Invalid protocol"}
    
    path = uri.replace("comptext://", "")
    parts = path.split("/")
    
    if len(parts) < 2:
        return {"error": "Invalid URI format"}
    
    resource_type = parts[0]
    resource_id = parts[1]
    
    return {
        "type": resource_type,
        "id": resource_id,
        "resolved": True,
        "provider": "CompText V6 Resolver"
    }
