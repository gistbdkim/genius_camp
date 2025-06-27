import asyncio
import nats

async def main():
    # Connect to NATS!
    nc = await nats.connect("demo.nats.io")

    try:
        while True:
            # Publish a message to 'foo'
            await nc.publish("pc23", b'Hello from Python!')
            print("asd")
            # Make sure all published messages have reached the server
            await nc.flush()
    except:
        pass
    # Process a message
    msg = await sub.next_msg()
    print("Received:", msg)

    # Close NATS connection
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())