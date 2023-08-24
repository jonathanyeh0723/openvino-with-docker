import os 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


current_location = os.getcwd()
photo_path = []

for i in os.listdir(current_location):
    if i.startswith('b'):
        photo_path.append(i)
# To have photo list in ascending order
photo_path.sort()

name_list = ["desert", "space", "sea", "Kinderdijk", "camp", "Alpen"]

data = {}

for item in range(len(name_list)):
    data[name_list[item]] = photo_path[item]

fig = plt.subplots(2, 3, figsize=(15, 7))
for index, (name, img_path) in enumerate(data.items()):
    plt.subplot(2, 3, index+1)
    plt.axis("Off")
    plt.title(list(data.keys())[index], fontsize=15)
    image = mpimg.imread(img_path)
    plt.imshow(image)

plt.savefig('what_was_i_made_for.png')
plt.show()
