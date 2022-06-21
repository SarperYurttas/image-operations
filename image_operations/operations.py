from PIL import Image


def resize_img(img, factor, method):
    methods = {
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC,
        'nearest': Image.NEAREST,
        'lanczos': Image.LANCZOS,
    }
    newsize = (img.width * factor, img.height * factor)
    resized_img = img.resize(newsize, methods.get(method))

    return resized_img
