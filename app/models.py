from torchvision import models
from torchvision.models.detection.ssd import SSDClassificationHead
from torchvision.models.detection import _utils
from torch import nn


def create_model(num_classes):
    # w_b_path = './weights/vgg16_features-amdegroot-88682ab5.pth'
    # weights = torch.load(w_b_path)
    model = models.detection.ssdlite320_mobilenet_v3_large(weights=None, weights_backbone=None)

    model.roi_heads.box_predictor.cls_score = nn.Linear(1024, num_classes)

    return model
