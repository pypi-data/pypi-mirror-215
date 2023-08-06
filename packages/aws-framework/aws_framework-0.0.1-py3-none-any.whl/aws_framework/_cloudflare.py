from ._config import cfg
from ._types import MaybeJson, Method, asyncio
from .client import ApiClient
from .utils import nginx_render


class CloudFlare(ApiClient):
    """Domain provisioning service"""

    base_url = "https://api.cloudflare.com/client/v4/"
    headers = {
        "X-Auth-Email": cfg.CF_EMAIL,
        "X-Auth-Key": cfg.CF_API_KEY,
        "Content-Type": "application/json",
    }

    async def provision(self, name: str, port: int):
        """
        Provision a new domain
        """
        try:
            response = await self.fetch(
                f"/zones/{cfg.CF_ZONE_ID}/dns_records",
                "POST",
                json={
                    "type": "A",
                    "name": name,
                    "content": cfg.IP_ADDR,
                    "ttl": 1,
                    "priority": 10,
                    "proxied": True,
                },
            )
            print(response)
            assert isinstance(response, dict)
            assert response["success"] is True
            data = response["result"]
            assert isinstance(data, dict)
            nginx_render(name=name, port=port)
            return {
                "url": f"https://{name}.aiofauna.com",
                "ip": f"https://{cfg.IP_ADDR}:{port}",
                "data": data,
            }
        except Exception as exc:
            raise exc
