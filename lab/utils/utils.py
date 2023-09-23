"""Import required libraries."""
import subprocess


class utils:
    """Define utils class."""

    @classmethod
    def count_images_size(cls):
        """Use subprocess to count total size of docker images."""
        subprocess.call(["docker image ls >> docker_images.txt"], shell=True)

        image_size_gb_total = 0
        image_size_mb_total = 0
        image_size_kb_total = 0
        with open('docker_images.txt', mode='r') as f:
            result = f.readlines()
            for line in result:
                if 'GB' in line:
                    image_size_gb = float(line.split(' ')[-1].split('GB')[0])
                    image_size_gb_total += image_size_gb
                if 'MB' in line:
                    image_size_mb = float(line.split(' ')[-1].split('MB')[0])
                    image_size_mb_total += image_size_mb
                if 'kB' in line:
                    image_size_kb = float(line.split(' ')[-1].split('kB')[0])
                    image_size_kb_total += image_size_kb

        print("Total docker images size downloaded:")
        print(str(image_size_gb_total) + "GB, ",
              str(image_size_mb_total) + "MB, ",
              str(image_size_kb_total) + "kB")
        subprocess.call(["rm docker_images.txt"], shell=True)
