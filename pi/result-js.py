import asyncio
import nats
from picamera2 import Picamera2, MappedArray
import io

async def main():
    # Connect to NATS
    nc = await nats.connect("demo.nats.io")
    js = nc.jetstream()
    await js.add_stream(name="sample-stream", subjects=["foo"])
    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    async def send_frame():
        print("in")
        while True:
            print("loop")
            # Capture frame
            buffer = io.BytesIO()
            picam2.capture_file(buffer, format='jpeg')
            # Publish frame to NATS
            print("shot")
            await js.publish("pc23", buffer.getvalue())
            await asyncio.sleep(1/30)  # Send 30 frames per second

    # Start the sending task
    sender_task = asyncio.create_task(send_frame())

    # Run for a certain amount of time then clean up
    await asyncio.sleep(60)  # Run for 60 seconds

    # Cancel the sending task and stop the camera
    sender_task.cancel()
    picam2.stop()
    await nc.flush()
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())
