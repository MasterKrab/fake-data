from utils.photo import create_image

for i in range(101, 501):
    create_image(i)
    print(f"{i} images created")
