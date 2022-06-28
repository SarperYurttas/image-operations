from PIL import Image

from .u2net import remove_background


def resize_img(img_path, factor, method):
    img = Image.open(img_path)

    methods = {
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC,
        'nearest': Image.NEAREST,
        'lanczos': Image.LANCZOS,
    }
    newsize = (img.width * factor, img.height * factor)
    resized_img = img.resize(newsize, methods.get(method))

    resized_img.save(img_path, format='png')
