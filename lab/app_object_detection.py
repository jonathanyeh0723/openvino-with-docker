"""People Counter App."""
import argparse
import cv2
import os
import time
import logging
from datetime import datetime
import numpy as np
from openvino.runtime import Core


def get_args():
    """To have a user-friendly command-line interfaces."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="The location of model.xml file.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="The path to input image/video/webcam.")
    parser.add_argument("-d", "--device", default="CPU", type=str,
                        help="To specify target device for inference.")
    parser.add_argument("-pt", "--prob_threshold", default=0.6, type=float,
                        help="Probability threhsold for detections filtering.")
    parser.add_argument("-c", "--color", default="GREEN", type=str,
                        help="The color to draw the bounding box.")
    args = parser.parse_args()

    return args


def infer_on_target(args):
    """Interpreted inference loop."""
    single_image_mode = False

    if args.input.split(".")[-1] in ["jpg", "jpeg", "bmp", "png"]:
        single_image_mode = True
        input_stream = args.input

    demo_start = time.time()

    core = Core()
    model = core.read_model(args.model)
    compiled_model = core.compile_model(model, args.device)
    input_layers = compiled_model.input(0)
    b, c, h, w = input_layers.shape

    full_device_name = core.get_property(args.device, 'FULL_DEVICE_NAME')

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        print("Can not detect streaming data. Abort!")
        exit()

    # Set text parameters to be printed
    font = cv2.FONT_HERSHEY_COMPLEX
    text_scale = 0.5
    text_color = (200, 10, 10)
    text_thickness = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        key_pressed = cv2.waitKey(60)
        frame_count += 1

        image_h, image_w, image_c = frame.shape
        resized = cv2.resize(frame, (w, h))
        transposed = resized.transpose((2, 0, 1))
        input_tensor = np.expand_dims(transposed, axis=0)

        # Restart inference loop
        detect_flag = False

        inf_start = time.time()
        infer_request = compiled_model.create_infer_request()
        results = infer_request.infer({0: input_tensor})
        inf_time = time.time() - inf_start

        inf_info = "Inference time: {:.3f} ms".format(inf_time)
        cv2.putText(frame, inf_info, (15, 15), font,
                    text_scale, text_color, text_thickness)

        color_dict = {"BLUE": (255, 0, 0), "GREEN": (0, 255, 0),
                      "RED": (0, 0, 255)}
        if args.color:
            out_color = color_dict.get(args.color)
        else:
            out_color = color_dict["BLUE"]

        for res in results.values():
            for obj in res[0][0]:
                label = int(obj[1])
                conf = obj[2]
                if conf >= args.prob_threshold:
                    xmin = int(obj[3] * image_w)
                    ymin = int(obj[4] * image_h)
                    xmax = int(obj[5] * image_w)
                    ymax = int(obj[6] * image_h)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),
                                  out_color, 3)
        # Image mode
        if single_image_mode:
            cv2.imwrite('output_image.jpg', frame)

    cap.release()
    cv2.destroyAllWindows()

def main():
    """Define main function."""
    args = get_args()
    infer_on_target(args)


if __name__ == "__main__":
    main()
