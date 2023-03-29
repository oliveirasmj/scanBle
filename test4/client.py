import asyncio
from aiocoap import *

# GET request
async def get_request():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/services')
    response = await protocol.request(request).response
    print('GET request response code:', response.code)
    print('GET request response payload:', response.payload.decode())

# POST request
async def post_request():
    protocol = await Context.create_client_context()
    payload = b'{"address": "11:22:33:44:55:66", "name": "device-2"}'
    request = Message(code=POST, uri='coap://localhost/services', payload=payload)
    response = await protocol.request(request).response
    print('POST request response code:', response.code)
    print('POST request response payload:', response.payload.decode())

# PUT request
async def put_request():
    protocol = await Context.create_client_context()
    payload = b'{"name": "device-2-renamed"}'
    request = Message(code=PUT, uri='coap://localhost/services/641aede88758a114d4badc40', payload=payload)
    response = await protocol.request(request).response
    print('PUT request response code:', response.code)
    print('PUT request response payload:', response.payload.decode())

# DELETE request
async def delete_request():
    protocol = await Context.create_client_context()
    request = Message(code=DELETE, uri='coap://localhost/services/63fd16394f04887892593963')
    response = await protocol.request(request).response
    print('DELETE request response code:', response.code)
    print('DELETE request response payload:', response.payload.decode())

# run the requests
async def main():
    await get_request()
    await post_request()
    await put_request()
    await delete_request()

asyncio.run(main())
