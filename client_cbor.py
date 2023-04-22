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

async def get_service_by_id(service_id):
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=f'coap://localhost/services/{service_id}')
    response = await protocol.request(request).response
    print(f'GET service {service_id} response code:', response.code)
    #payload = cbor2.loads(response.payload)
    #print('GET service response payload:', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('GET service response payload (CBOR):', payload_hex)

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
    #payload = cbor2.loads(response.payload)
    #print('POST new service response (CBOR):', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('POST new service response (CBOR):', payload_hex)

async def delete_service_by_id(service_id):
    protocol = await Context.create_client_context()
    request = Message(code=DELETE, uri=f'coap://localhost/services/{service_id}')
    response = await protocol.request(request).response
    print(f'DELETE service {service_id} response code:', response.code)
    #payload = cbor2.loads(response.payload)
    #print('DELETE service response payload (CBOR):', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('DELETE service response payload (CBOR):', payload_hex)

async def count_services():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/services/count')
    response = await protocol.request(request).response
    print('GET count services response code:', response.code)
    #payload = cbor2.loads(response.payload)
    #print('GET count services response payload (CBOR):', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('GET count services response payload (CBOR):', payload_hex)

async def calculate_disk_space():
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri="coap://localhost/diskspace")
    response = await context.request(request).response
    print('Disk space information services response code:', response.code)
    #payload = cbor2.loads(response.payload)
    #print('Disk space information:', payload)
    payload_hex = " ".join(hex(b)[2:].zfill(2) for b in response.payload)
    print('Disk space information (CBOR):', payload_hex)


async def main():
    os.system('cls' if os.name=='nt' else 'clear') # clear the screen
    while True:
        print("Select an option:")
        print("1. Get all services")
        print("2. Get service by ID")
        print("3. Add new service")
        print("4. Delete service by ID")
        print("5. Count services")
        print("6. Calculate disk space")
        print("7. Scan")
        print("0. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            await get_all_services()
            input("Press enter to continue...")
        elif choice == "2":
            service_id = input("Enter service ID: ")
            await get_service_by_id(service_id)
            input("Press enter to continue...")
        elif choice == "3":
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
            await post_new_service(payload)
            input("Press enter to continue...")
        elif choice == "4":
            service_id = input("Enter service ID: ")
            await delete_service_by_id(service_id)
            input("Press enter to continue...")
        elif choice == "5":
            await count_services()
            input("Press enter to continue...")
        elif choice == "6":
            await calculate_disk_space()
            input("Press enter to continue...")
        elif choice == "7":
            try:
                await scan.main()
            except scan.BLEScanError as e:
                print(f"BLE scanning failed with error: {e}")
            input("Press enter to continue...")
        elif choice == "0":
            break
        else:
            print("Invalid choice")
        os.system('cls' if os.name=='nt' else 'clear') # clear the screen


asyncio.run(main())

