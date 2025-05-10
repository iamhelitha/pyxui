from typing import Dict, Any
from urllib.parse import urlencode, quote
import base64

def generate_shadowsocks_config(config: Dict[str, Any], data: Dict[str, Any] = None) -> str:
    """Generate Shadowsocks configuration string.
    
    Parameters:
        config (dict):
            Base configuration with required fields:
            - ps (str): Configuration name
            - add (str): Server address
            - port (str): Server port
            - method (str): Encryption method
            - password (str): Authentication password
            
        data (dict, optional):
            Additional configuration data:
            - plugin (str): Plugin name
            - plugin-opts (str): Plugin options
            
    Returns:
        str: Shadowsocks configuration string
    """
    if not all(k in config for k in ["ps", "add", "port", "method", "password"]):
        raise ValueError("Missing required fields in config")
    
    # Create the user info string
    user_info = f"{config['method']}:{config['password']}"
    user_info_base64 = base64.b64encode(user_info.encode()).decode()
    
    # Build the base URL
    base_url = f"ss://{user_info_base64}@{config['add']}:{config['port']}"
    
    # Process additional parameters
    params = {}
    if data:
        if 'plugin' in data:
            plugin_str = data['plugin']
            if 'plugin-opts' in data:
                plugin_str += f";{data['plugin-opts']}"
            params['plugin'] = plugin_str
    
    # Build the final URL
    if params:
        query_string = urlencode(params)
        final_url = f"{base_url}?{query_string}"
    else:
        final_url = base_url
        
    # Add remarks (ps) at the end
    final_url = f"{final_url}#{quote(config['ps'])}"
    
    return final_url 