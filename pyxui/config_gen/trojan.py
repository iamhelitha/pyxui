from typing import Dict, Any
from urllib.parse import urlencode, quote

def generate_trojan_config(config: Dict[str, Any], data: Dict[str, Any] = None) -> str:
    """Generate Trojan configuration string.
    
    Parameters:
        config (dict):
            Base configuration with required fields:
            - ps (str): Configuration name
            - add (str): Server address
            - port (str): Server port
            - password (str): Authentication password
            
        data (dict, optional):
            Additional configuration data:
            - security (str): Security type (default: tls)
            - type (str): Network type
            - host (str): Server hostname
            - path (str): WebSocket path
            - sni (str): SNI value
            - alpn (str): ALPN protocols
            - fp (str): TLS fingerprint
            
    Returns:
        str: Trojan configuration string
    """
    if not all(k in config for k in ["ps", "add", "port", "password"]):
        raise ValueError("Missing required fields in config")
        
    # Build the base URL
    base_url = f"trojan://{config['password']}@{config['add']}:{config['port']}"
    
    # Process additional parameters
    params = {}
    if data:
        for key, value in data.items():
            if value:
                params[key] = value
    
    # Build the final URL
    if params:
        query_string = urlencode(params)
        final_url = f"{base_url}?{query_string}"
    else:
        final_url = base_url
        
    # Add remarks (ps) at the end
    final_url = f"{final_url}#{quote(config['ps'])}"
    
    return final_url 