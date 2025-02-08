from fastapi import Request
import logging
from src.exception import ForbiddenException

logging.basicConfig(level=logging.INFO)

allowed_subnets = [
    "127.0.0.1",
    "192.168.1.",
    "192.168.2.",
    "172.23.32.",
    "localhost",
    "172.25.208.",
    "172.27.32."
]


async def ip_restriction_middleware(request: Request, call_next):
    client_ip = request.client.host
    logging.info(f"Client IP: {client_ip}")

    if not any(client_ip.startswith(subnet) for subnet in allowed_subnets):
        logging.warning(f"Access denied for IP: {client_ip}")
        raise ForbiddenException(detail="Access forbidden: your IP address is not allowed")

    return await call_next(request)
