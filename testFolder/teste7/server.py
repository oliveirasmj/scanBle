import asyncio
import aiocoap.resource as resource
import aiocoap
import pymongo
from bson.objectid import ObjectId

# Define MongoDB connection details
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DATABASE = "dbscan"
MONGODB_COLLECTION = "services"

# Create a MongoDB client and database connection
mongo_client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
mongo_db = mongo_client[MONGODB_DATABASE]
mongo_collection = mongo_db[MONGODB_COLLECTION]

class ServicesResource(resource.Resource):
    """
    CoAP resource for interacting with MongoDB services collection
    """
    def __init__(self):
        super().__init__()
        self.allowed_methods = ["GET", "POST"]

    async def render_get(self, request):
        """
        Handle GET requests to retrieve all services in the collection
        """
        services = mongo_collection.find()
        response = "\n".join([str(s) for s in services])
        return aiocoap.Message(payload=response.encode())

    async def render_post(self, request):
        """
        Handle POST requests to create a new service in the collection
        """
        service_data = request.payload.decode()
        result = mongo_collection.insert_one({"name": service_data})
        response = f"Inserted service with ID: {result.inserted_id}"
        return aiocoap.Message(payload=response.encode())

class ServiceByIdResource(resource.Resource):
    """
    CoAP resource for interacting with a specific MongoDB service by ID
    """
    def __init__(self, service_id):
        super().__init__()
        self.service_id = service_id
        self.allowed_methods = ["GET"]

    async def render_get(self, request):
        """
        Handle GET requests to retrieve the service with the given ID
        """
        service = mongo_collection.find_one({"_id": ObjectId(self.service_id)})
        response = str(service) if service else "Service not found"
        return aiocoap.Message(payload=response.encode())


# Create CoAP server
root = resource.Site()
root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
root.add_resource(('services',), ServicesResource())

async def main():
    # Add ServiceByIdResource resources
    services = mongo_collection.find()
    for service in services:
        root.add_resource(('services', str(service["_id"])), ServiceByIdResource(str(service["_id"])))

    # Start CoAP server
    protocol = await aiocoap.Context.create_server_context(root)

    # Keep server running until interrupted
    await asyncio.sleep(1000)

    # Clean up
    protocol.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
