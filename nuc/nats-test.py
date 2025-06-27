import asyncio
import nats

async def main():
    # Connect to NATS!
    nc = await nats.connect("demo.nats.io")

    # Receive messages on 'foo'
    sub = await nc.subscribe("pc23")

    while True:
    # Process a message
        msg = await sub.next_msg()
        print("Received:", msg)

    # Make sure all published messages have reached the server
    await nc.flush()

    # Close NATS connection
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
