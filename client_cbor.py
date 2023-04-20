import asyncio
import aiocoap
from aiocoap import *
import json
import time
from bson.objectid import ObjectId
import os
import scan
import cbor2

async def get_all_services():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/services')
    response = await protocol.request(request).response
    print('GET all services response code:', response.code)
    #payload = cbor2.loads(response.payload)
    #print('GET all services response payload:', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('GET all services response payload (CBOR):', payload_hex)

async def main():
    await get_all_services()

asyncio.run(main())

