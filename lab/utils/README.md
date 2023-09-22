# Building the utils as helper function...
A Utils class is a general purposed utility class using which we can reuse the existing block of code without creating instance of the class.

## Counting the total size of docker images downloaded
We all have limited hard drive in our local machine, wisely distribute your space is what we all need to learn.<br> 
Imagine you downloaded various docker images for testing, you want to sum up all of these images so that you could better estimate how much free spaces left to prioritize your ongoing task.<br>
For example, you have the following images:
```
REPOSITORY                TAG       IMAGE ID       CREATED        SIZE
dockerflamejc/advanipc    v3        bfc8a2c83834   9 days ago     6.21GB
<none>                    <none>    57cac29a60e0   9 days ago     6.22GB
dockerflamejc/advanipc    latest    1f31b8535cc2   2 weeks ago    6.08GB
dockerflamejc/advanipc    v2        1f31b8535cc2   2 weeks ago    6.08GB
advanipc/demo             latest    59ffd52622f0   7 weeks ago    7.3GB
openvino-yolov8           latest    5d9f8f729d2f   2 months ago   11.6GB
sertek_hero_project       latest    572d6a933ec1   3 months ago   2.89GB
ov_2023_ubuntu22_pyt311   latest    020d8c9ba799   3 months ago   2.38GB
hello-world               latest    9c7a54a9a43c   4 months ago   13.3kB
```
By executing the script `count_downloaded_images_size.py`, you can quickly check the total `SIZE` of them.
```
python3 count_downloaded_images_size.py
```
```
Total docker images size downloaded:
48.76GB,  0MB,  13.3kB
```
