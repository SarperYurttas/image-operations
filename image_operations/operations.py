from PIL import Image

from .u2net import remove_background


def resize_img(img_path, scale_factor, method):
    img = Image.open(img_path)

    methods = {
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC,
        'nearest': Image.NEAREST,
        'lanczos': Image.LANCZOS,
    }
    newsize = (img.width * scale_factor, img.height * scale_factor)
    resized_img = img.resize(newsize, methods.get(method))

    resized_img.save(img_path, format='png')
