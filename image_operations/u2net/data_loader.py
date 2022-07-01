from __future__ import division, print_function

import numpy as np
import torch
import cv2
from torchvision import transforms


class RescaleT(object):
    def __init__(self, output_size: int) -> None:
        self.output_size = output_size

    def __call__(self, image):
        img = cv2.resize(image, (self.output_size, self.output_size),
                         interpolation=cv2.INTER_LINEAR)
        return img


class ToTensorLab(object):
    def __init__(self) -> None:
        pass

    def __call__(self, image):
        tmpImg = np.zeros((image.shape[0], image.shape[1], 3))
        image = image / np.max(image)
        if image.shape[2] == 1:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmpImg[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmpImg[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225

        tmpImg = tmpImg.transpose((2, 0, 1))

        return torch.from_numpy(tmpImg)


def image_loader(path: str):
    image = cv2.imread(path)
    transform = transforms.Compose([RescaleT(320), ToTensorLab()])

    if 2 == len(image.shape):
        image = image[:, :, np.newaxis]
    if transform:
        image = transform(image)

    return image.unsqueeze(0)
