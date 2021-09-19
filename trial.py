from PIL import Image
file = 'tithis'
im = Image.open(f"template_preperation/{file}.jpg")
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
top = 25
for i in range(16):
    left = 0
    right = left + width
    bottom = top + 83 # 83 for all, 76.5 for samvatsaras
    
    im1 = im.crop((left, top, right, bottom))
    
    # Shows the image in image viewer
    # im1.show()

    im1.save(f'template_preperation/{file}/{i+1}.jpg')

    top = bottom