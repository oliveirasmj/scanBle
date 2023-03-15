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

if __name__ == "__main__":
    asyncio.run(main())
