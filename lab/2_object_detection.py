"""Import necessary libraries."""
from openvino.runtime import Core
import numpy as np
import cv2
import matplotlib.pyplot as plt


def main():
    """Perform object detection."""
    classes = []
    with open('labels/coco_91cl_bkgr.txt', 'r') as f:
        labels_list = (f.readlines())
        for i in labels_list:
            i = i.strip()
            classes.append(i)

    core = Core()
    model_xml = 'public/ssdlite_mobilenet_v2/FP16/ssdlite_mobilenet_v2.xml'
    model = core.read_model(model_xml)
    compiled_model = core.compile_model(model, 'AUTO')
    input_layers = compiled_model.input(0)
    b, h, w, c = input_layers.shape

    image = cv2.imread('images/neymar.jpg')
    original = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_h, image_w, image_c = image.shape
    resized = cv2.resize(image, (w, h))
    input_tensor = np.expand_dims(resized, axis=0)

    infer_request = compiled_model.create_infer_request()
    results = infer_request.infer({0: input_tensor})

    for res in results.values():
        for obj in res[0][0]:
            label = int(obj[1])
            conf = obj[2]
            if conf >= 0.6 and classes[label] == 'cat':
                xmin = int(obj[3] * image_w)
                ymin = int(obj[4] * image_h)
                xmax = int(obj[5] * image_w)
                ymax = int(obj[6] * image_h)
                drew_image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax),
                                           (0, 255, 0), 3)
                cv2.putText(drew_image, f"{classes[label]}: {conf:.2f}",
                            (xmin+10, ymin+25), cv2.FONT_HERSHEY_COMPLEX,
                            image.shape[1]/1000*1.5, (0, 255, 0), 2,
                            lineType=cv2.LINE_AA)

    shown = cv2.cvtColor(drew_image, cv2.COLOR_BGR2RGB)
    data = {"Original Photo": original, "Inferenced Photo": shown}
    fig, axs = plt.subplots(1, len(data.items()), figsize=(12, 8))

    for ax, (name, image) in zip(axs, data.items()):
        ax.axis('off')
        ax.set_title(name)
        ax.imshow(image)

    plt.show()


if __name__ == "__main__":
    main()
