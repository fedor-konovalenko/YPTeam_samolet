from typing import List
from pathlib import Path
import torch
from torchvision.io import read_image

from models import create_model

W_PATH = './weights/mobile_net.pth'
model = create_model(3)
model.load_state_dict(torch.load(W_PATH, map_location=torch.device('cpu')))
model.eval()


def _glob_images(folder: Path, exts: List[str] = ('*.jpg', '*.png',)) -> List[Path]:
    images = []
    for ext in exts:
        images += list(folder.glob(ext))
    return images


def format_predictions(preds) -> str:
    formatted = []
    n = len(list(preds['scores']))
    for i in range(n):
        lb = int(list(preds['labels'])[i]) + 1
        score = round(float(list(preds['scores'])[i]), 4)
        xmin, ymin, xmax, ymax = map(int, list(preds['boxes'][i]))
        st = f"{lb} {score} {xmin} {ymin} {xmax} {ymax}"
        formatted.append(st)

    return "\n".join(formatted)


def write_predictions(predictions: str, output_path: Path) -> None:
    with open(output_path, 'w') as f:
        f.write(predictions)


def predict_folder(input_folder: str, output_folder: str) -> None:
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    images_path = _glob_images(input_folder)

    for img_path in images_path:
        img = read_image(str(img_path)).to(torch.float32)
        predictions = model.eval()([img, ])[0]
        predictions_repr = format_predictions(predictions)
        output_path = output_folder / img_path.with_suffix('.txt').name

        write_predictions(predictions_repr, output_path)


def main():

    input_folder = './private/images'
    output_folder = './output'

    predict_folder(input_folder, output_folder)


if __name__ == '__main__':
    main()
