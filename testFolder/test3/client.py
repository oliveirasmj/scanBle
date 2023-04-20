import asyncio
import aiocoap

async def main():
    # Create CoAP context and send GET request to services resource
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri="coap://localhost/services")
    response = await context.request(request).response

    # Print response payload
    print(response.payload.decode())

    # Send POST request to services resource to create a new service
    payload = "New Service"
    request = aiocoap.Message(code=aiocoap.POST, uri="coap://localhost/services", payload=payload.encode("utf-8"))
    response = await context.request(request).response

    # Print response payload
    print(response.payload.decode())

    # Send GET request to a specific service resource
    service_id = "63fd16394f04887892593963"
    request = aiocoap.Message(code=aiocoap.GET, uri=f"coap://localhost/services/{service_id}")
    response = await context.request(request).response

    # Print response payload
    print(response.payload.decode())

    # Send PUT request to update a specific service resource
    service_id = "63fd16394f04887892593963"
    payload = "Updated Service"
    request = aiocoap.Message(code=aiocoap.PUT, uri=f"coap://localhost/services/{service_id}", payload=payload.encode("utf-8"))
    response = await context.request(request).response

    # Print response payload
    print(response.payload.decode())

    # Send DELETE request to delete a specific service resource
    service_id = "63fd16394f04887892593963"
    request = aiocoap.Message(code=aiocoap.DELETE, uri=f"coap://localhost/services/{service_id}")
    response = await context.request(request).response

    # Print response payload
    print(response.payload.decode())

if __name__ == "__main__":
    asyncio.run(main())
