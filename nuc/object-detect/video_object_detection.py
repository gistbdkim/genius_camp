import os
import argparse
import cv2
import numpy as np
import nats
import io
import asyncio
from object_detection_functions import YOLOModel, read_classes, show_detected_objects

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight_path", type=str, default="./yolov3-tiny.weights")
    parser.add_argument("--cfg_path", type=str, default="./yolov3-tiny.cfg")
    parser.add_argument("--class_path", type=str, default="./coco.names")
    parser.add_argument("--subject", default='pc23')
    args = parser.parse_args()

    # Model 정의
    print("모델을 로딩합니다... ")
    model = YOLOModel(args.weight_path, args.cfg_path)
    print("모델 로딩이 완료되었습니다")

    # Connect to NATS
    print("NATS에 연결합니다...")
    nc = await nats.connect("demo.nats.io")
    sub = await nc.subscribe(args.subject)
    print(f"NATS에 연결되었습니다. 주제: {args.subject}")
    classes = read_classes(args.class_path)
    print(f"클래스 파일 로드 완료: {args.class_path}")
    
    print("객체 검출을 시작합니다. 이미지 창에서 esc 버튼을 누르면 종료합니다.")

    try:
        while True:
            print("메시지 대기 중...")
            # Wait for a message
            msg = await sub.next_msg()
            print("메시지 수신됨")
            # Decode JPEG frame
            buffer = io.BytesIO(msg.data)
            img_array = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            print("이미지 디코딩 완료")

            # Display the frame
            cv2.imshow("NATS Video Stream", img)

            outs = model.inference(img)
            show_detected_objects(img, outs, classes, threshold=0.4)

            # Exit if Esc is pressed
            if cv2.waitKey(1) == 27:
                break
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("객체 검출을 종료합니다")

if __name__ == "__main__":
    asyncio.run(main())
