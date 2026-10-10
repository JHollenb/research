"""E3 step 1 (laptop/CPU): build the shipped payload data for the GPU worker.

Writes ``payload/`` with, per corpus, the first N items in THEIR row order (first 5 x 1024 items is their token
pooling protocol, experiments/token_pooling.py) and the matching stored DINOv2-B and MPNet rows from their Hugging
Face embeddings, so CKA is computed against exactly the image embeddings their paper uses.

Row orders reproduced from modalities/image_captions/datasets.py at the pinned commit:
  coco_train2014               images sorted by id, captions in annotation-file order (we keep caption 0)
  StanfordParagraphCaptioning  paragraphs_v1.json in file order

The raw caption files are downloaded here (the laptop WAN is fast; Beast's is not) and never shipped whole.
"""

from __future__ import annotations

import argparse
import io
import json
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

import torch

from common.rosetta import VISION_B, fetch, storage_root
from unpaired_rosetta.embeddings import load_rows

HERE = Path(__file__).resolve().parent
COCO_ANNOTATIONS = "http://images.cocodataset.org/annotations/annotations_trainval2014.zip"
SPC_PARAGRAPHS = "https://homes.cs.washington.edu/~ranjay/visualgenome/data/dataset/paragraphs_v1.json.zip"


def raw(url: str, member: str) -> bytes:
    cache = storage_root() / "raw" / Path(member).name
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=600).read()))
        cache.write_bytes(archive.read(member))
    return cache.read_bytes()


def coco_first_captions(split: str) -> list[str]:
    data = json.loads(raw(COCO_ANNOTATIONS, f"annotations/captions_{split}.json"))
    captions = defaultdict(list)
    for annotation in data["annotations"]:
        captions[annotation["image_id"]].append(annotation["caption"])
    images = sorted(data["images"], key=lambda image: image["id"])
    return [captions[image["id"]][0].strip() for image in images]


def spc_paragraphs() -> list[str]:
    return [entry["paragraph"].strip() for entry in json.loads(raw(SPC_PARAGRAPHS, "paragraphs_v1.json"))]


CORPORA = {"coco_train2014": lambda: coco_first_captions("train2014"), "StanfordParagraphCaptioning": spc_paragraphs}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", type=int, default=2048)
    parser.add_argument("--out", type=Path, default=HERE / "payload")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = {"items": args.items, "corpora": {}}
    for corpus, texts in CORPORA.items():
        captions = texts()[: args.items]
        indices = torch.arange(len(captions))
        vision = load_rows(fetch(corpus, "vision", VISION_B), indices).half()
        mpnet = load_rows(fetch(corpus, "language", "mpnet"), indices).half()
        (args.out / f"{corpus}.json").write_text(json.dumps(captions))
        torch.save({"vision": vision, "mpnet": mpnet}, args.out / f"{corpus}.pt")
        manifest["corpora"][corpus] = {"num": len(captions), "vision_model": VISION_B, "first_caption": captions[0]}
        print(corpus, len(captions), tuple(vision.shape))
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
