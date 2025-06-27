import argparse
import os
import numpy as np
import cv2
import asyncio
import nats
import io
import time

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", default='pc23')
    args = parser.parse_args()

    # Connect to NATS
    nc = await nats.connect("demo.nats.io")

    # Subscribe to the specified subject
    sub = await nc.subscribe(args.subject)

    print(f"Subscribed to NATS subject: {args.subject}")

    try:
        while True:
            # Wait for a message

            msg = await sub.next_msg()
            # Decode JPEG frame
            buffer = io.BytesIO(msg.data)
            img_array = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Display the frame
            cv2.imshow("NATS Video Stream", img)

            # Exit if Esc is pressed
            if cv2.waitKey(1) == 27:
                break
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting...")
    except:
        pass
    #finally:
        # Clean up
        # cv2.destroyAllWindows()
        # await nc.close()
        # print("NATS connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
