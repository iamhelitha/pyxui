import json
from typing import Union, Optional

import pyxui
from pyxui import errors
from pyxui.protocols import Protocol, ClientConfig, create_client_settings

class Clients:
    def get_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None,
        password: str = None
    ) -> Union[dict, errors.NotFound]:
        """Get client from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``, optional):
               Email of the client
                
            uuid (``str``, optional):
               UUID of the client (for VMESS/VLESS)
               
            password (``str``, optional):
               Password of the client (for TROJAN)
            
        Returns:
            `~Dict`: On success, a dict is returned or else 404 an error will be raised
        """
        
        get_inbounds = self.get_inbounds()
        
        if not any([email, uuid, password]):
            raise ValueError("At least one of email, uuid, or password must be provided")
        
        for inbound in get_inbounds['obj']:
            if inbound['id'] != inbound_id:
                continue
            
            settings = json.loads(inbound['settings'])
            protocol = inbound.get('protocol', 'vless')
            
            for client in settings['clients']:
                if protocol in ['vmess', 'vless']:
                    if (email and client['email'] == email) or (uuid and client.get('id') == uuid):
                        return client
                elif protocol == 'trojan':
                    if (email and client['email'] == email) or (password and client.get('password') == password):
                        return client
                elif protocol == 'shadowsocks':
                    if email and client['email'] == email:
                        return client

        raise errors.NotFound()

    def get_client_stats(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str,
    ) -> Union[dict, errors.NotFound]:
        """Get client stats from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``):
               Email of the client
            
        Returns:
            `~Dict`: On success, a dict is returned or else 404 error will be raised
        """
        
        get_inbounds = self.get_inbounds()
        
        if not email:
            raise ValueError()
        
        for inbound in get_inbounds['obj']:
            if inbound['id'] != inbound_id:
                continue
            
            client_stats = inbound['clientStats']
            
            for client in client_stats:
                if client['email'] != email:
                    continue
                
                return client

        raise errors.NotFound()

    def add_client(
        self: "pyxui.XUI",
        inbound_id: int,
        protocol: Union[str, Protocol],
        email: str,
        enable: bool = True,
        flow: str = "",
        limit_ip: int = 0,
        total_gb: int = 0,
        expire_time: int = 0,
        telegram_id: str = "",
        subscription_id: str = "",
        uuid: Optional[str] = None,
        password: Optional[str] = None,
        method: Optional[str] = None
    ) -> Union[dict, errors.NotFound]:
        """Add client to the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
            protocol (``str`` | ``Protocol``):
                Protocol type (vmess, vless, trojan, shadowsocks)
            email (``str``):
                Email of the client
            enable (``bool``, optional):
                Status of the client
            flow (``str``, optional):
                Flow of the client
            limit_ip (``int``, optional):
                IP Limit of the client
            total_gb (``int``, optional):
                Download and upload limitation in bytes
            expire_time (``int``, optional):
                Client expiration date in timestamp (epoch)
            telegram_id (``str``, optional):
                Telegram id of the client
            subscription_id (``str``, optional):
                Subscription id of the client
            uuid (``str``, optional):
                UUID for VMESS/VLESS clients
            password (``str``, optional):
                Password for TROJAN clients
            method (``str``, optional):
                Encryption method for Shadowsocks clients
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        if isinstance(protocol, str):
            protocol = Protocol(protocol.lower())
            
        # Validate protocol-specific requirements
        if protocol in [Protocol.VMESS, Protocol.VLESS] and not uuid:
            raise ValueError(f"UUID is required for {protocol.value} protocol")
        elif protocol == Protocol.TROJAN and not password:
            raise ValueError("Password is required for TROJAN protocol")
            
        client_config = ClientConfig(
            protocol=protocol,
            email=email,
            enable=enable,
            flow=flow,
            limit_ip=limit_ip,
            total_gb=total_gb,
            expire_time=expire_time,
            telegram_id=telegram_id,
            subscription_id=subscription_id,
            uuid=uuid,
            password=password,
            method=method
        )
        
        settings = create_client_settings(client_config)
        
        params = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }

        response = self.request(
            path="addClient",
            method="POST",
            params=params
        )

        return self.verify_response(response)

    def delete_client(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = None,
        uuid: str = None,
        password: str = None
    ) -> Union[dict, errors.NotFound]:
        """Delete client from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``, optional):
               Email of the client
                
            uuid (``str``, optional):
               UUID of the client (for VMESS/VLESS)
               
            password (``str``, optional):
               Password of the client (for TROJAN)
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        # First get the inbound to determine the protocol
        inbounds = self.get_inbounds()
        protocol = None
        for inbound in inbounds['obj']:
            if inbound['id'] == inbound_id:
                protocol = inbound.get('protocol', 'vless')
                break
                
        if not protocol:
            raise errors.NotFound("Inbound not found")
            
        # Find the client
        try:
            find_client = self.get_client(
                inbound_id=inbound_id,
                email=email,
                uuid=uuid,
                password=password
            )
        except errors.NotFound:
            raise errors.NotFound("Client not found")
            
        # Get the appropriate identifier based on protocol
        if protocol in ['vmess', 'vless']:
            client_id = find_client.get('id')
            if not client_id:
                raise ValueError(f"UUID not found for {protocol} client")
        elif protocol == 'trojan':
            client_id = find_client.get('password')
            if not client_id:
                raise ValueError("Password not found for TROJAN client")
        else:  # shadowsocks
            client_id = find_client.get('email')
            if not client_id:
                raise ValueError("Email not found for Shadowsocks client")
        
        response = self.request(
            path=f"{inbound_id}/delClient/{client_id}",
            method="POST"
        )

        return self.verify_response(response)

    def update_client(
        self: "pyxui.XUI",
        inbound_id: int,
        protocol: Union[str, Protocol],
        email: str,
        enable: bool,
        flow: str,
        limit_ip: int,
        total_gb: int,
        expire_time: int,
        telegram_id: str,
        subscription_id: str,
        uuid: Optional[str] = None,
        password: Optional[str] = None,
        method: Optional[str] = None,
    ) -> Union[dict, errors.NotFound]:
        """Update client in the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
            protocol (``str`` | ``Protocol``):
                Protocol type (vmess, vless, trojan, shadowsocks)
            email (``str``):
                Email of the client
            enable (``bool``):
                Status of the client
            flow (``str``):
                Flow of the client
            limit_ip (``int``):
                IP Limit of the client
            total_gb (``int``):
                Download and upload limitation in bytes
            expire_time (``int``):
                Client expiration date in timestamp (epoch)
            telegram_id (``str``):
                Telegram id of the client
            subscription_id (``str``):
                Subscription id of the client
            uuid (``str``, optional):
                UUID for VMESS/VLESS clients
            password (``str``, optional):
                Password for TROJAN clients
            method (``str``, optional):
                Encryption method for Shadowsocks clients
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        if isinstance(protocol, str):
            protocol = Protocol(protocol.lower())
            
        # Validate protocol-specific requirements
        if protocol in [Protocol.VMESS, Protocol.VLESS] and not uuid:
            raise ValueError(f"UUID is required for {protocol.value} protocol")
        elif protocol == Protocol.TROJAN and not password:
            raise ValueError("Password is required for TROJAN protocol")
            
        client_config = ClientConfig(
            protocol=protocol,
            email=email,
            enable=enable,
            flow=flow,
            limit_ip=limit_ip,
            total_gb=total_gb,
            expire_time=expire_time,
            telegram_id=telegram_id,
            subscription_id=subscription_id,
            uuid=uuid,
            password=password,
            method=method
        )
        
        settings = create_client_settings(client_config)
        
        params = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }
        
        # Find existing client
        find_client = self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid,
            password=password
        )
        
        # Get the appropriate identifier based on protocol
        if protocol in [Protocol.VMESS, Protocol.VLESS]:
            client_id = find_client.get('id')
            if not client_id:
                raise ValueError(f"UUID not found for {protocol.value} client")
        elif protocol == Protocol.TROJAN:
            client_id = find_client.get('password')
            if not client_id:
                raise ValueError("Password not found for TROJAN client")
        else:  # Shadowsocks
            client_id = find_client.get('email')
            if not client_id:
                raise ValueError("Email not found for Shadowsocks client")
        
        response = self.request(
            path=f"updateClient/{client_id}",
            method="POST",
            params=params
        )

        return self.verify_response(response)
    
    def reset_client_traffic(
        self: "pyxui.XUI",
        inbound_id: int,
        email: str = False,
        uuid: str = False
    ) -> Union[dict, errors.NotFound]:
        """Delete client from the existing inbound.

        Parameters:
            inbound_id (``int``):
                Inbound id
                
            email (``str``, optional):
               Email of the client
                
            uuid (``str``, optional):
               UUID of the client
            
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        find_client = self.get_client(
            inbound_id=inbound_id,
            email=email,
            uuid=uuid
        )
        
        response = self.request(
            path=f"{inbound_id}/resetClientTraffic/{find_client['email']}",
            method="POST"
        )

        return self.verify_response(response)