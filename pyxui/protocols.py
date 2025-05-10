from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass

class Protocol(Enum):
    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "shadowsocks"

@dataclass
class ClientConfig:
    protocol: Protocol
    email: str
    enable: bool = True
    flow: str = ""
    limit_ip: int = 0
    total_gb: int = 0
    expire_time: int = 0
    telegram_id: str = ""
    subscription_id: str = ""
    
    # Protocol specific fields
    uuid: Optional[str] = None  # For VMESS/VLESS
    password: Optional[str] = None  # For TROJAN
    method: Optional[str] = None  # For Shadowsocks
    
    def to_dict(self) -> Dict[str, Any]:
        base_config = {
            "email": self.email,
            "enable": self.enable,
            "flow": self.flow,
            "limitIp": self.limit_ip,
            "totalGB": self.total_gb,
            "expiryTime": self.expire_time,
            "tgId": self.telegram_id,
            "subId": self.subscription_id
        }
        
        if self.protocol in [Protocol.VMESS, Protocol.VLESS]:
            base_config["id"] = self.uuid
        elif self.protocol == Protocol.TROJAN:
            base_config["password"] = self.password
        elif self.protocol == Protocol.SHADOWSOCKS:
            base_config["method"] = self.method or "aes-256-gcm"
            
        return base_config

def create_client_settings(client_config: ClientConfig) -> Dict[str, Any]:
    """Create client settings based on protocol"""
    settings = {
        "clients": [client_config.to_dict()],
        "decryption": "none",
        "fallbacks": []
    }
    
    # Add protocol-specific settings
    if client_config.protocol == Protocol.SHADOWSOCKS:
        settings["method"] = client_config.method or "aes-256-gcm"
    
    return settings 