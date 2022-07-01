import os

# import torch.optim as optim
import torch
from PIL import Image
from torch.autograd import Variable

from .data_loader import image_loader
from .model import U2NETP  # small version u2net 4.7 MB


GPU_INFERENCE = False

# normalize the predicted SOD probability map
def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d - mi) / (ma - mi)

    return dn


def naive_cutout(img, mask):
    empty = Image.new("RGBA", (img.size), 0)
    cutout = Image.composite(img, empty, mask)
    return cutout


def save_output(image_path, pred):

    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    image = Image.open(image_path)

    mask = Image.fromarray((predict_np * 255).astype("uint8"), mode="L")
    mask = mask.resize(image.size, Image.LANCZOS)

    cutout = naive_cutout(image, mask)

    cutout.save(image_path, format='png')


@torch.inference_mode()
def remove_background(image_path: str):
    model_dir = os.path.join(os.getcwd(), 'image_operations/u2net/models/u2netp.pth')

    net = U2NETP(3, 1)

    inputs_test = image_loader(image_path)
    inputs_test = inputs_test.type(torch.FloatTensor)

    if torch.cuda.is_available() and GPU_INFERENCE:
        net.load_state_dict(torch.load(model_dir))
        inputs_test = Variable(inputs_test.cuda())
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))
        inputs_test = Variable(inputs_test)
    net.eval()

    d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

    # normalization
    pred = d1[:, 0, :, :]
    pred = normPRED(pred)

    save_output(image_path=image_path, pred=pred)

    del d1, d2, d3, d4, d5, d6, d7, pred, net, inputs_test
    if torch.cuda.is_available() and GPU_INFERENCE:
        torch.cuda.empty_cache()


if __name__ == "__main__":
    remove_background(image_path='boat.jpg')
