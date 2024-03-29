import asyncio
import aiocoap
from aiocoap import *
import json
import time
from bson.objectid import ObjectId
import os

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

async def post_new_service(payload):
    protocol = await Context.create_client_context()
    # Encode the payload as JSON and convert it to bytes
    payload = json.dumps(payload).encode()
    # Create the request
    request = Message(code=POST, uri='coap://localhost/services', payload=payload)
    # Send the request and wait for the response
    response = await protocol.request(request).response
    # Print the response
    print('POST new service response code:', response.code)
    print('POST new service response payload:', response.payload.decode())

async def delete_service_by_id(service_id):
    protocol = await Context.create_client_context()
    request = Message(code=DELETE, uri=f'coap://localhost/services/{service_id}')
    response = await protocol.request(request).response
    print(f'DELETE service {service_id} response code:', response.code)
    print(f'DELETE service {service_id} response payload:', response.payload.decode())

async def count_services():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/services/count')
    response = await protocol.request(request).response
    print('GET count services response code:', response.code)
    print('GET count services response payload:', response.payload.decode())

async def calculate_disk_space():
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri="coap://localhost/diskspace")
    response = await context.request(request).response
    print(f"Disk space information: {response.payload.decode()}")


async def main():
    await get_all_services()
    await get_service_by_id("6425cf2e51ac4d1cb7807be9")
    
    # Construct the payload with the required structure
    payload = {
        "address": "66:9E:7A:1D:CE:E2",
        "name": "66-9E-7A-1D-CE-E2",
        "time": {
            "$date": {
                "$numberLong": str(int(time.time() * 1000))
            }
        },
        "services": [
            {
              "description": "Apple Nearby Service",
              "service": "9fa480e0-4967-4542-9390-d343dc5d04ae (Handle: 20): Apple Nearby Service",
              "uuid": "af0badb1-5b99-43cd-917a-a77bc549e3cc",
              "subDescription": "Nearby Characteristic",
              "handle": "21",
              "properties": "['write', 'notify', 'extended-properties', 'reliable-write']"
            }
        ]
    }

    # Call the post_new_service() method with the payload
    await post_new_service(payload)
    await delete_service_by_id("643d88c648d664d4e4951e48")
    await count_services()
    await calculate_disk_space()

asyncio.run(main())
