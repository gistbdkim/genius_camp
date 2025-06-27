import asyncio
import argparse
import nats
from picamera2 import Picamera2, MappedArray
import io

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", default='pc23')
    args = parser.parse_args()

    # Connect to NATS
    nc = await nats.connect("demo.nats.io")
    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    async def send_frame():
        while True:
            # Capture frame
            buffer = io.BytesIO()
            picam2.capture_file(buffer, format='jpeg')
            # Publish frame to NATS
            print(f"Published to NATS subject: {args.subject}")
            await nc.publish(args.subject, buffer.getvalue())
            await asyncio.sleep(1/30)  # Send 30 frames per second

    # Start the sending task
    sender_task = asyncio.create_task(send_frame())

    # Run for a certain amount of time then clean up
    await asyncio.sleep(3600)  # Run for 60 seconds

    # Cancel the sending task and stop the camera
    sender_task.cancel()
    picam2.stop()
    await nc.flush()
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
