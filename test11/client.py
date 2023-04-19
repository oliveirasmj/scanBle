import asyncio
import aiocoap
from aiocoap import *
import json
import time
from bson.objectid import ObjectId
import os
import scan

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
            input("Press enter to continue...")
            await post_new_service(payload)
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

