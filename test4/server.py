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
        self.allowed_methods = ["GET", "POST", "DELETE"]

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
    
    async def render_delete(self, request):
        """
        Handle DELETE requests to delete a service from the collection by ID
        """
        service_id = request.opt.uri_path[-1]
        result = mongo_collection.delete_one({"_id": pymongo.ObjectId(service_id)})
        response = f"Deleted service with ID: {service_id}" if result.deleted_count > 0 else "Service not found"
        return aiocoap.Message(payload=response.encode())

# Create CoAP server
root = resource.Site()
root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
root.add_resource(('services',), ServicesResource())

async def main():
    # Start CoAP server
    protocol = await aiocoap.Context.create_server_context(root)

    # Keep server running until interrupted
    await asyncio.sleep(1000)

    # Clean up
    protocol.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
