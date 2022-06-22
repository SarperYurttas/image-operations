import os
from skimage import io
import torch
from torch.autograd import Variable
# import torch.optim as optim
import numpy as np

from PIL import Image
from .data_loader import image_loader

from .model import U2NETP  # small version u2net 4.7 MB


# normalize the predicted SOD probability map
def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d-mi)/(ma-mi)

    return dn


def naive_cutout(img, mask):
    empty = Image.new("RGBA", (img.size), 0)
    cutout = Image.composite(img, empty, mask)
    return cutout


def save_output(image_name, pred):
    img_name = image_name.split('.')[0]

    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    image = Image.open(image_name)

    mask = Image.fromarray((predict_np * 255).astype("uint8"), mode="L")
    mask = mask.resize(image.size, Image.LANCZOS)

    cutout = naive_cutout(image, mask)

    cutout.save(img_name+'_bgremoved.png', format='png')


def remove_background(image_path: str):
    model_dir = os.path.join(os.getcwd(), 'image_operations/u2net/models/u2netp.pth')

    net = U2NETP(3, 1)

    if torch.cuda.is_available():
        net.load_state_dict(torch.load(model_dir))
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))
    net.eval()

    inputs_test = image_loader(image_path)

    inputs_test = inputs_test.type(torch.FloatTensor)

    if torch.cuda.is_available():
        inputs_test = Variable(inputs_test.cuda())
    else:
        inputs_test = Variable(inputs_test)
    with torch.inference_mode():
        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

    # normalization
    pred = d1[:, 0, :, :]
    pred = normPRED(pred)

    save_output(image_name=image_path, pred=pred)

    del d1, d2, d3, d4, d5, d6, d7


if __name__ == "__main__":
    remove_background(image_name = 'boat.jpg')
