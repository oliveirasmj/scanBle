import asyncio
from aiocoap import *


async def get_all_services():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/services')
    response = await protocol.request(request).response
    print('GET all services response code:', response.code)
    print('GET all services response payload:', response.payload.decode())


async def get_service_by_id(service_id):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=f'coap://localhost/services/{service_id}')
    response = await protocol.request(request).response
    print(f'GET service {service_id} response code:', response.code)
    print(f'GET service {service_id} response payload:', response.payload.decode())


async def post_new_service():
    protocol = await Context.create_client_context()
    payload = b'{"name": "new-service"}'
    request = Message(code=POST, uri='coap://localhost/services', payload=payload)
    response = await protocol.request(request).response
    print('POST new service response code:', response.code)
    print('POST new service response payload:', response.payload.decode())


async def put_service_by_id(service_id):
    protocol = await Context.create_client_context()
    payload = b'{"name": "updated-service"}'
    request = Message(code=PUT, uri=f'coap://localhost/services/{service_id}', payload=payload)
    response = await protocol.request(request).response
    print(f'PUT service {service_id} response code:', response.code)
    print(f'PUT service {service_id} response payload:', response.payload.decode())


async def delete_service_by_id(service_id):
    protocol = await Context.create_client_context()
    request = Message(code=DELETE, uri=f'coap://localhost/services/{service_id}')
    response = await protocol.request(request).response
    print(f'DELETE service {service_id} response code:', response.code)
    print(f'DELETE service {service_id} response payload:', response.payload.decode())


async def main():
    #await get_all_services()
    #await get_service_by_id("6425cf2e51ac4d1cb7807be9")
    #await post_new_service()
    await put_service_by_id("6425cf2e51ac4d1cb7807be9")
    #await delete_service_by_id("6425cf2e51ac4d1cb7807be9")


asyncio.run(main())
