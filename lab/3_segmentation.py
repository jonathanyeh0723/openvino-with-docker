import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from openvino.runtime import Core


def segmentation_map_to_image(
    result: np.ndarray, colormap: np.ndarray, remove_holes: bool = False
) -> np.ndarray:
    """
    Convert network result of floating point numbers to an RGB image with
    integer values from 0-255 by applying a colormap.

    :param result: A single network result after converting to pixel values in H,W or 1,H,W shape.
    :param colormap: A numpy array of shape (num_classes, 3) with an RGB value per class.
    :param remove_holes: If True, remove holes in the segmentation result.
    :return: An RGB image where each pixel is an int8 value according to colormap.
    """
    if len(result.shape) != 2 and result.shape[0] != 1:
        raise ValueError(
            f"Expected result with shape (H,W) or (1,H,W), got result with shape {result.shape}"
        )

    if len(np.unique(result)) > colormap.shape[0]:
        raise ValueError(
            f"Expected max {colormap[0]} classes in result, got {len(np.unique(result))} "
            "different output values. Please make sure to convert the network output to "
            "pixel values before calling this function."
        )
    elif result.shape[0] == 1:
        result = result.squeeze(0)

    result = result.astype(np.uint8)

    contour_mode = cv2.RETR_EXTERNAL if remove_holes else cv2.RETR_TREE
    mask = np.zeros((result.shape[0], result.shape[1], 3), dtype=np.uint8)
    for label_index, color in enumerate(colormap):
        label_index_map = result == label_index
        label_index_map = label_index_map.astype(np.uint8) * 255
        contours, hierarchies = cv2.findContours(
            label_index_map, contour_mode, cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(
            mask,
            contours,
            contourIdx=-1,
            color=color.tolist(),
            thickness=cv2.FILLED,
        )

    return mask


core = Core()
model = core.read_model('intel/road-segmentation-adas-0001/FP16/road-segmentation-adas-0001.xml')
compiled_model = core.compile_model(model, 'AUTO')
input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

image = cv2.imread('images/empty_road_mapillary.jpg')
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_h, image_w, image_c = image.shape

b, c, h, w = input_layer.shape
resized = cv2.resize(image, (w, h))
transposed = resized.transpose((2, 0, 1))
input_tensor = np.expand_dims(transposed, axis=0)

infer_request = compiled_model.create_infer_request()
results = infer_request.infer({0: input_tensor})

segmentation_mask = np.argmax(results[output_layer], axis=1)

# Define colormap, each color represents a class.
colormap = np.array([[68, 1, 84], [48, 103, 141], [53, 183, 120], [199, 216, 52]])

# Define the transparency of the segmentation mask on the photo.
alpha = 0.3

# Use function from notebook_utils.py to transform mask to an RGB image.
mask = segmentation_map_to_image(segmentation_mask, colormap)
resized_mask = cv2.resize(mask, (image_w, image_h))

# Create an image with mask.
image_with_mask = cv2.addWeighted(resized_mask, alpha, rgb_image, 1 - alpha, 0)

# Data visualization pipeline
data = {"Original": rgb_image, "Segmentation": mask, "Masked": image_with_mask}
fig, axs = plt.subplots(1, len(data.items()), figsize=(15, 7))
for ax, (name, image) in zip(axs, data.items()):
    ax.axis("Off")
    ax.set_title(name)
    ax.imshow(image)

plt.show()
