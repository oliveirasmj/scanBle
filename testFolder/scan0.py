import asyncio
import platform
import sys
from bleak import BleakClient, BleakScanner
import pymongo
from pymongo import MongoClient
import datetime

cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
#cluster = pymongo.MongoClient("mongodb+srv://linux:1234@cluster0.7kmsjgc.mongodb.net/?retryWrites=true&w=majority")
db = cluster["dbscan"]

class textcolor:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GOLD = '\033[33m'
    BOLD = '\033[1m'
    END = '\033[0m'

def device_details_to_dict(raw_details):
    # Format device details into string. Accommodate errors caused by lack of data.
    dict_ = {
        'address': None,
        'details': None,
        'metadata': None,
        'name': None,
        'rssi': None
    }
    try:
        dict_['address'] = raw_details.address
    except Exception:
        print(f'Address not found for device with the following data: {raw_details}')
    try:
        dict_['details'] = raw_details.details
    except Exception:
        print(f'Details not found for device with the following data: {raw_details}')
    try:
        dict_['metadata'] = raw_details.metadata
    except Exception:
        print(f'Metadata not found for device with the following data: {raw_details}')
    try:
        dict_['name'] = raw_details.name
    except Exception:
        print(f'Name not found for device with the following data: {raw_details}')
    try:
        dict_['rssi'] = raw_details.rssi
    except Exception:
        print(f'RSSI not found for device with the following data: {raw_details}')

    return dict_


async def main():
    print('///////////////////////////////////////////////')
    print('Scanning for Bluetooth LE devices...')
    devices = await BleakScanner.discover()
    print('///////////////////////////////////////////////')
    print('\t\tServices scan')
    print('///////////////////////////////////////////////')
    print('Requesting list of services and characteristics from found Bluetooth LE devices...')
    for device in devices:
        try:
            temp_device = await BleakScanner.find_device_by_address(device.address, timeout=20)
            async with BleakClient(temp_device) as client:
                print('Services found for device')
                print(f'\tDevice address: {textcolor.GOLD}{device.address}{textcolor.END}')
                print(f'\tDevice name: {textcolor.GREEN}{device.name}{textcolor.END}')

                # Guardar address e name na BD
                # --------------------------------------------------------
                collection = db["services"]
                dado = {
                    'address': f'{device.address}',
                    'name': f'{device.name}',
                    'time': datetime.datetime.now(),
                    'services': []  # Lista para armazenar todas as características encontradas
                }
                # Inserir e guardar id
                _id = collection.insert_one(dado)
                # --------------------------------------------------------

                print("\tServices:")
                for service in client.services:
                    print('\t\tService')
                    print(f'\t\tDescription: {textcolor.CYAN}{service.description}{textcolor.END}')
                    print(f'\t\tService: {textcolor.GOLD}{service}{textcolor.END}')

                    characteristics = []
                    serviceDetails = {
                        'description': f'{service.description}',
                        'service': f'{service}'
                    }

                    for c in service.characteristics:
                        characteristics.append({
                            'uuid': f'{c.uuid}',
                            'subDescription': f'{c.description}',
                            'handle': f'{c.handle}',
                            'properties': f'{c.properties}'
                        })

                    # Armazenar todas as características encontradas para este serviço
                    serviceDetails['characteristics'] = characteristics

                    # Adicionar o serviço com todas as características à lista do dispositivo
                    collection.update_one({'_id': _id.inserted_id}, {"$push": {"services": serviceDetails}})

                    print(f'\t\tCharacteristics: {characteristics}')

        except asyncio.exceptions.TimeoutError:
            print(f'{textcolor.RED}TimeoutError:{textcolor.END} Device at address `{device.address}` timed out.')
        except Exception as error:
            print(f'Exception: An error occurred while connecting to device `{device.address}`:\n\t{error}')

if __name__ == "__main__":
    asyncio.run(main())
