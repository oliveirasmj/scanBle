import logging
import asyncio
import json
from pymongo import MongoClient
from aiocoap import *
from aiocoap import resource


logging.basicConfig(level=logging.INFO)

# Crie uma conexão com o banco de dados MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Selecione o banco de dados e a coleção
db = client['services']
collection = db['collection']

# Classe de recurso de serviço
class ServiceResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.content_type = 0

    # Lidar com solicitações GET
    async def render_get(self, request):
        # Recupere todos os serviços da coleção
        services = collection.find({})
        # Crie uma lista de dicionários para representar cada serviço
        services_list = []
        for service in services:
            services_list.append({"id": str(service["_id"]), "name": service["name"]})
        # Serialize a lista de serviços como JSON
        payload = json.dumps(services_list, ensure_ascii=False).encode('utf-8')
        # Crie uma resposta COAP com a lista de serviços
        return Message(payload=payload, code=CONTENT, content_format=40)


# Configurar e iniciar o servidor
async def main():
    # Crie a raiz do recurso
    root = resource.Site()
    # Adicione o recurso do serviço à raiz
    root.add_resource(('services',), ServiceResource())

    # Inicie o servidor em um endpoint IPv6 global
    endpoint = await Context.create_server_context(root, bind=('::', 5683))
    logging.info('Servidor COAP iniciado em ::5683')
    await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
