from PIL import Image, ImageChops, ImageOps
import PIL
from PIL import ImageFilter


# import scipy
from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario


def generate_black_and_white_from_png(use_beaches, use_gradients, png_img, path, basename, size=Size.GIANT, rotation=0):
    print(PIL.PILLOW_VERSION)
    scn = Scenario(size=size)
    img = Image.open(png_img)
    img = img.convert('L')
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    img = img.resize((scn.map.width, scn.map.height), Image.ANTIALIAS)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img = ImageOps.invert(img.convert("RGB")).convert('1')
    img = img.rotate(rotation)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            is_black = img.getpixel((x, y)) == 0
            if is_black:
                scn.map.tiles[x][y].type = 22

    if use_beaches is True:
        erosion_img = img.filter(ImageFilter.MinFilter(3))
        for _ in range(1):
            erosion_img = erosion_img.filter(ImageFilter.MinFilter(3))

        beaches = ImageChops.subtract(img, erosion_img)
        # beaches.show()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                is_white = beaches.getpixel((x, y)) == 255
                if is_white:
                    scn.map.tiles[x][y].type = 2

    if use_gradients is True: # to avoid any other type of stuff

        # inverted.show()
        dilation_img_for_azure = img.filter(ImageFilter.MaxFilter(3))
        for _ in range(7):
            dilation_img_for_azure = dilation_img_for_azure.filter(ImageFilter.MaxFilter(3))
        azure_water = ImageChops.subtract(dilation_img_for_azure, img)
        # azure_water.show()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                is_white = azure_water.getpixel((x, y)) == 255
                if is_white:
                    scn.map.tiles[x][y].type = 1

        dilation_img_for_medium = dilation_img_for_azure.filter(ImageFilter.MaxFilter(3))
        for _ in range(7):
            dilation_img_for_medium = dilation_img_for_medium.filter(ImageFilter.MaxFilter(3))
        medium_water = ImageChops.subtract(dilation_img_for_medium, dilation_img_for_azure)
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                is_white = medium_water.getpixel((x, y)) == 255
                if is_white:
                    scn.map.tiles[x][y].type = 23

    scn.save(path, basename)


