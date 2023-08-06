import argparse
import os.path

import PIL.Image
import torch
from huggingface_hub import hf_hub_download

from FBA_Matting import build_model, inference

REPO_ID = "leonelhs/FBA-Matting"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
weights = hf_hub_download(repo_id=REPO_ID, filename="FBA.pth")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="", help="Image path")
    parser.add_argument("--trimap", default="", help="Trimap image path")
    parser.add_argument("--output", default="./", help="Output dir")

    args = parser.parse_args()

    model = build_model(weights)
    model.eval().to(device)

    if os.path.exists(args.image):
        if os.path.exists(args.trimap):
            model = build_model(weights)
            results = inference(model, args.image, args.trimap)
            for result, i in zip(results, range(4)):
                PIL.Image.fromarray(result).save(os.path.join(args.output, f"output_{i}.png"))
        else:
            print("Trimap image is required.")
    else:
        print("No input image was given.")


if __name__ == "__main__":
    main()
