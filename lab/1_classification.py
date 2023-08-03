"""Import libraries."""
import cv2
import numpy as np
from openvino.runtime import Core


def main():
    """Run inference hello world."""
    core = Core()
    model = core.read_model('public/googlenet-v2/FP16/googlenet-v2.xml')
    compiled_model = core.compile_model(model, 'AUTO')
    input_layers = compiled_model.input(0)
    b, c, h, w = input_layers.shape

    image = cv2.imread('images/neymar.jpg')
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(converted, (w, h))
    transposed = resized.transpose((2, 0, 1))
    input_tensor = np.expand_dims(transposed, axis=0)

    infer_request = compiled_model.create_infer_request()
    results = infer_request.infer({0: input_tensor})

    labels = []
    with open('labels/imagenet_2015.txt', 'r') as f:
        labels_list = f.readlines()
        for i in labels_list:
            new_label = i.strip()[10:]
            labels.append(new_label)

    probs = next(iter(results.values()))
    idx = np.argsort(probs[0])[::-1]
    print("Top 5 classification results:")
    dash_line = '-'.join('' for x in range(50))
    print(dash_line)
    for i in range(5):
        print(idx[i], str(round(probs[0][idx[i]]*100))+"%", labels[idx[i]])


if __name__ =="__main__":
    main()
