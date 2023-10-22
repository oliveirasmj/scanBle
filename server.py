import asyncio
import aiocoap.resource as resource
import aiocoap
import psutil
import pymongo
from bson.objectid import ObjectId
import json

# Define MongoDB connection details
MONGODB_HOST = "localhost"
#MONGODB_HOST = "mongodb+srv://linux:1234@cluster0.7kmsjgc.mongodb.net/?retryWrites=true&w=majority"
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
        service_data = json.loads(request.payload.decode())
        service_dict = {
            "address": service_data["address"],
            "name": service_data["name"],
            "time": service_data["time"],
            "services": service_data["services"]
        }
        result = mongo_collection.insert_one(service_dict)
        response = f"Inserted service with ID: {result.inserted_id}"
        return aiocoap.Message(payload=response.encode())


class ServiceByIdResource(resource.Resource):
    """
    CoAP resource for interacting with a specific MongoDB service by ID
    """
    def __init__(self, service_id):
        super().__init__()
        self.service_id = service_id
        self.allowed_methods = ["GET", "DELETE"]

    async def render_get(self, request):
        """
        Handle GET requests to retrieve the service with the given ID
        """
        service = mongo_collection.find_one({"_id": ObjectId(self.service_id)})
        response = str(service) if service else "Service not found"
        return aiocoap.Message(payload=response.encode())

    async def render_delete(self, request):
        """
        Handle DELETE requests to remove the service with the given ID
        """
        result = mongo_collection.delete_one({"_id": ObjectId(self.service_id)})
        if result.deleted_count == 1:
            response = f"Deleted service with ID: {self.service_id}"
        else:
            response = "Service not found"
        return aiocoap.Message(payload=response.encode())


class ServiceCountResource(resource.Resource):
    """
    CoAP resource for counting the number of services in the collection
    """
    def __init__(self):
        super().__init__()
        self.allowed_methods = ["GET"]

    async def render_get(self, request):
        """
        Handle GET requests to retrieve the count of services in the collection
        """
        count = mongo_collection.count_documents({})
        response = f"Total number of services: {count}"
        return aiocoap.Message(payload=response.encode())


class DiskSpaceResource(resource.Resource):
    """
    CoAP resource for getting disk space information
    """
    def __init__(self):
        super().__init__()
        self.allowed_methods = ["GET"]

    async def render_get(self, request):
        """
        Handle GET requests to retrieve disk space information
        """
        disk_usage = psutil.disk_usage("/")
        free_percentage = disk_usage.free / disk_usage.total * 100
        used_percentage = disk_usage.used / disk_usage.total * 100
        response = f"Free space: {disk_usage.free} ({free_percentage:.2f}%), Used space: {disk_usage.used} ({used_percentage:.2f}%)"
        return aiocoap.Message(payload=response.encode())
    

class ScanResource(resource.Resource):
    """
    CoAP resource for scanning
    """
    def __init__(self):
        super().__init__()
        self.allowed_methods = ["GET"]

    async def render_get(self, request):
        """
        Handle GET requests for scanning
        """
        # Call the perform_scan function from scan.py
        from scan import perform_scan
        await perform_scan()
        response = "Scan complete"
        return aiocoap.Message(payload=response.encode())



# Create CoAP server
root = resource.Site()
root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))
root.add_resource(('services',), ServicesResource())
root.add_resource(('services', 'count'), ServiceCountResource())
root.add_resource(('diskspace',), DiskSpaceResource())
root.add_resource(('scan',), ScanResource())


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
