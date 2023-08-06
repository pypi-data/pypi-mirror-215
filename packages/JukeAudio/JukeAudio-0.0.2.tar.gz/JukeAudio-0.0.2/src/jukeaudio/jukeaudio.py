"""Module for working with Juke Audio device"""

import aiohttp
import base64

from .exceptions import AuthenticationException, UnexpectedException
from typing import List

api_version = "v2"

def create_auth_header(user_name: str, password: str):
    """Return auth header value"""
    return base64.b64encode(bytes(f"{user_name}:{password}", "utf-8")).decode("utf-8")


def is_juke_compatible(ver: str):
    """Create auth header value"""
    return ver.startswith(f"{api_version}.")


async def can_connect_to_juke(ip_address: str):
    """Verify connectivity to a compatible Juke device"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip_address}/api/") as response:
                contents = await response.json()
                return is_juke_compatible(contents["versions"][0])
    except aiohttp.ClientError:
        return False


async def get_devices(ip_address: str, username: str, password: str) -> List[str]:
    """Get device list"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/devices/") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc
    
async def get_device_connection_info(ip_address: str, username: str, password: str, device_id: str):
    """Get connection information"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/devices/{device_id}/connection") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_device_attributes(ip_address: str, username: str, password: str, device_id: str):
    """Get device attributes"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/devices/{device_id}/attributes") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_device_config(ip_address: str, username: str, password: str, device_id: str):
    """Get device attributes"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/devices/{device_id}/config") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc
    
async def get_device_metrics(ip_address: str, username: str, password: str, device_id: str):
    """Get device metrics"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/devices/{device_id}/metrics") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_zones(ip_address: str, username: str, password: str):
    """Get zone ids"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/zones") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_zone_config(ip_address: str, username: str, password: str, zone_id: str):
    """Get zone config"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/zones/{zone_id}") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc
    
async def set_zone_volume(ip_address: str, username: str, password: str, zone_id: str, volume: int):
    """Set zone volume"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.put(f"http://{ip_address}/api/{api_version}/zones/{zone_id}/volume", data = { "volume": volume}) as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.text()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def set_zone_input(ip_address: str, username: str, password: str, zone_id: str, input: str):
    """Set zone volume"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        data = "[]"
        if input is not None and len(input)>0:
            data = f"[\"{input}\"]"

        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.put(f"http://{ip_address}/api/{api_version}/zones/{zone_id}/input", data = data) as response:
                if response.status != 200:
                    print(response.status)
                    raise AuthenticationException
                else:
                    contents = await response.text()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_inputs(ip_address: str, username: str, password: str):
    """Get input ids"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/inputs") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc

async def get_input_config(ip_address: str, username: str, password: str, input_id: str):
    """Get input config"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/inputs/{input_id}") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc
    
async def get_available_inputs(ip_address: str, username: str, password: str, input_id: str):
    """Get available inputs"""
    try:
        hdr = {"Authorization": f"Bearer {create_auth_header(username, password)}"}
        async with aiohttp.ClientSession(headers=hdr) as session:
            async with session.get(f"http://{ip_address}/api/{api_version}/inputs/{input_id}/available-types") as response:
                if response.status != 200:
                    raise AuthenticationException
                else:
                    contents = await response.json()
                    return contents["available_types"]
    except aiohttp.ClientError as exc:
        raise UnexpectedException from exc
