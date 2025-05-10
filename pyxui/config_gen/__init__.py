import json
import base64
from urllib.parse import urlencode
from typing import Dict, Any, Union
from .vmess import generate_vmess_config
from .vless import generate_vless_config
from .trojan import generate_trojan_config
from .shadowsocks import generate_shadowsocks_config
from ..protocols import Protocol

def config_generator(protocol: Union[str, Protocol], config: Dict[str, Any], data: Dict[str, Any] = None) -> str:
    """Generate configuration string for various protocols.
    
    Parameters:
        protocol (str | Protocol):
            Protocol type (vmess, vless, trojan, shadowsocks)
        config (dict):
            Base configuration with protocol-specific required fields
        data (dict, optional):
            Additional configuration data
            
    Returns:
        str: Protocol-specific configuration string
    """
    if isinstance(protocol, str):
        protocol = Protocol(protocol.lower())
        
    if protocol == Protocol.VMESS:
        return generate_vmess_config(config)
    elif protocol == Protocol.VLESS:
        return generate_vless_config(config, data)
    elif protocol == Protocol.TROJAN:
        return generate_trojan_config(config, data)
    elif protocol == Protocol.SHADOWSOCKS:
        return generate_shadowsocks_config(config, data)
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")