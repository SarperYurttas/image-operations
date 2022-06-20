import PIL


def resize_img(img, factor, method):
    methods = {
        'bilinear': PIL.Image.Resampling.BILINEAR,
        'bicubic': PIL.Image.Resampling.BICUBIC,
        'nearest': PIL.Image.Resampling.NEAREST,
        'lanczos': PIL.Image.Resampling.LANCZOS
    }
    newsize = (img.width * factor, img.height * factor)
    resized_img = img.resize(newsize, methods.get(method))

    return resized_img
