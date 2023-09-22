import subprocess


subprocess.call(["docker image ls >> docker_images.txt"], shell=True)

image_size_gb_total = 0
image_size_mb_total = 0
image_size_kb_total = 0
with open ('docker_images.txt', mode='r') as f:
    result = f.readlines()
    for l in result:
        if 'GB' in l:
            image_size_gb = float(l.split(' ')[-1].split('GB')[0])
            image_size_gb_total += image_size_gb
        if 'MB' in l:
            image_size_mb = float(l.split(' ')[-1].split('MB')[0])
            image_size_mb_total += image_size_mb
        if 'kB' in l:
            image_size_kb = float(l.split(' ')[-1].split('kB')[0])
            image_size_kb_total += image_size_kb

print("Total docker images size downloaded:")
print(str(image_size_gb_total) + "GB, ",
      str(image_size_mb_total) + "MB, ",
      str(image_size_kb_total) + "kB")

subprocess.call(["rm docker_images.txt"], shell=True)

