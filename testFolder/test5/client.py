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

# GET by ID request
async def get_by_id_request(id):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=f'coap://localhost/services?_id={id}')
    response = await protocol.request(request).response
    print('GET by ID request response code:', response.code)
    print('GET by ID request response payload:', response.payload.decode())


# run the requests
async def main():
    #await get_request()
    #await post_request()
    await get_by_id_request('63fd16394f04887892593963') # Replace with the actual ID you want to retrieve


asyncio.run(main())
