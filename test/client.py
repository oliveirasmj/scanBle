import asyncio
import aiocoap.resource as resource
import aiocoap

async def get_services():
    # Faz uma solicitação GET ao endpoint /services para obter uma lista de todos os serviços disponíveis
    protocol = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri='coap://[::1]/services')
    response = await protocol.request(request).response
    print('Lista de serviços disponíveis:')
    print(response.payload.decode())

async def get_service_by_id(id):
    # Faz uma solicitação GET ao endpoint /services/{id} para obter detalhes sobre um serviço específico
    protocol = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri=f'coap://[::1]/services/{id}')
    response = await protocol.request(request).response
    print(f'Detalhes do serviço {id}:')
    print(response.payload.decode())

async def main():
    await get_services()
    await get_service_by_id('640f0e4b546af41569d850d3')

if __name__ == '__main__':
    asyncio.run(main())
