# PyXUI 
An application with python that allows you to modify your xui panel ([alireza0 x-ui](https://github.com/alireza0/x-ui)) ([Sanaeii 3x-ui](https://github.com/MHSanaei/3x-ui)) 

## How To Install
```
pip install -U git+https://github.com/staliox/pyxui.git
```

## Supported Protocols
PyXUI now supports multiple protocols:
- VMESS
- VLESS
- TROJAN
- Shadowsocks

Each protocol has its specific configuration requirements:
- VMESS/VLESS: Uses UUID for client identification
- TROJAN: Uses password for authentication
- Shadowsocks: Uses email and encryption method

## How To Use
- Import pyxui in your .py file
```python
from pyxui import XUI

# Basic:
xui = XUI(
    full_address="https://staliox.com:2087",
    panel="alireza", # Your panel name, "alireza" or "sanaei"
)

# Advanced:
xui = XUI(
    full_address="http://staliox.site:2087",
    panel="alireza", # Your panel name, "alireza" or "sanaei"
    https=False, # Make note if you don't use https set False else set True
    session_string=... # If you have session cookie to use panel without login
)
```

- Login in your panel
```python
from pyxui.errors import BadLogin

try:
  xui.login(USERNAME, PASSWORD)
except BadLogin:
  ...
```

- Get inbounds list
```python
get_inbounds = xui.get_inbounds()

# Result
{
    "success": true,
    "msg": "",
    "obj": [
        {
            "id": 1,
            "up": 552345026,
            "down": 18164200325,
            "total": 0,
            "remark": "Staliox",
            "enable": true,
            "expiryTime": 0,
            "clientStats": [
                {
                    "id": 1,
                    "inboundId": 1,
                    "enable": true,
                    "email": "Me",
                    "up": 191308877,
                    "down": 4945030148,
                    "expiryTime": 0,
                    "total": 0
                }
            ],
            "listen": "",
            "port": 443,
            "protocol": "vless",
            "settings": "{\n  \"clients\": [\n    {\n      \"email\": \"Me\",\n      \"enable\": true,\n      \"expiryTime\": 0,\n      \"flow\": \"\",\n      \"id\": \"c6419651-68d7-gfhg-d611-32v5df41g105\",\n      \"limitIp\": 0,\n      \"subId\": \"\",\n      \"tgId\": \"@staliox\",\n      \"totalGB\": 0\n    }\n  ],\n  \"decryption\": \"none\",\n  \"fallbacks\": []\n}",
            "tag": "inbound-443",
            "sniffing": "{\n  \"enabled\": true,\n  \"destOverride\": [\n    \"http\",\n    \"tls\"\n  ]\n}"
        }
    ]
}
```

- Add client to the existing inbound
```python
# For VMESS/VLESS
client = xui.add_client(
    inbound_id=1,
    protocol="vless",  # or "vmess"
    email="example@gmail.com",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",
    enable=True,
    flow="",
    limit_ip=0,
    total_gb=5368709120,
    expire_time=1684948641772,
    telegram_id="",
    subscription_id=""
)

# For TROJAN
client = xui.add_client(
    inbound_id=1,
    protocol="trojan",
    email="example@gmail.com",
    password="your_secure_password",
    enable=True,
    limit_ip=0,
    total_gb=5368709120,
    expire_time=1684948641772
)

# For Shadowsocks
client = xui.add_client(
    inbound_id=1,
    protocol="shadowsocks",
    email="example@gmail.com",
    method="aes-256-gcm",  # Encryption method
    enable=True,
    limit_ip=0,
    total_gb=5368709120,
    expire_time=1684948641772
)
```

- Update the existing client
```python
# Similar to add_client, but for updating existing clients
client = xui.update_client(
    inbound_id=1,
    protocol="vless",  # Specify the protocol
    email="example@gmail.com",
    # Protocol-specific fields (uuid, password, or method)
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa",  # For VMESS/VLESS
    enable=True,
    flow="",
    limit_ip=0,
    total_gb=5368709120,
    expire_time=1684948641772,
    telegram_id="",
    subscription_id=""
)
```

- Get client's information:
```python
# For VMESS/VLESS
get_client = xui.get_client(
    inbound_id=1,
    email="Me",
    uuid="5d3d1bac-49cd-4b66-8be9-a728efa205fa"  # Either email or uuid is required
)

# For TROJAN
get_client = xui.get_client(
    inbound_id=1,
    email="Me",
    password="your_secure_password"  # Either email or password is required
)

# For Shadowsocks
get_client = xui.get_client(
    inbound_id=1,
    email="Me"  # Email is required for Shadowsocks
)

# Result example
{
     'email': 'Me',
     'enable': True,
     'expiryTime': 0,
     'flow': 'xtls-rprx-vision',
     'id': '5d3d1bac-49cd-4b66-8be9-a728efa205fa',  # or 'password' for TROJAN
     'limitIp': 0,
     'subId': '',
     'tgId': '',
     'totalGB': 0
}
```

- Generate configuration strings
```python
from pyxui.config_gen import config_generator

# VMESS Configuration
vmess_config = {
    "v": "2",
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "id": "a85def57-0a86-43d1-b15c-0494519067c6",
    "aid": "0",
    "scy": "auto",
    "net": "tcp",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "tls": "tls",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}
vmess_string = config_generator("vmess", vmess_config)

# VLESS Configuration
vless_config = {
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "id": "a85def57-0a86-43d1-b15c-0494519067c6"
}
vless_data = {
    "security": "tls",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}
vless_string = config_generator("vless", vless_config, vless_data)

# TROJAN Configuration
trojan_config = {
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "password": "your_secure_password"
}
trojan_data = {
    "security": "tls",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}
trojan_string = config_generator("trojan", trojan_config, trojan_data)

# Shadowsocks Configuration
ss_config = {
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "method": "aes-256-gcm",
    "password": "your_secure_password"
}
ss_data = {
    "plugin": "v2ray-plugin",
    "plugin-opts": "tls;host=staliox.site;path=/"
}
ss_string = config_generator("shadowsocks", ss_config, ss_data)
```
