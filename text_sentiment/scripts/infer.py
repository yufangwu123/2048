#!/usr/bin/env python3
"""推理入口：python scripts/infer.py --text '这部电影太棒了'"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.datasets.vocab import Vocab, tokenize
from src.models.factory import build_model
from src.utils.config import load_config, resolve_device

LABEL_NAMES = {0: "负面", 1: "正面"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="文本情感分类推理")
    parser.add_argument("--config", type=str, default="configs/train.yaml")
    parser.add_argument("--text", type=str, required=True, help="待预测文本")
    parser.add_argument("--ckpt", type=str, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(ROOT / args.config)
    device = resolve_device(cfg.get("device", "auto"))

    data_cfg = cfg["data"]
    model_cfg = cfg["model"]
    out_cfg = cfg["output"]

    vocab = Vocab.load(ROOT / out_cfg["vocab_file"])
    model = build_model(model_cfg["name"], len(vocab), model_cfg)

    ckpt_path = Path(args.ckpt) if args.ckpt else ROOT / out_cfg["best_model"]
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()

    tokens = tokenize(args.text, data_cfg.get("tokenize", "char"))
    ids = vocab.encode(tokens, data_cfg.get("max_len", 128))
    input_ids = torch.tensor([ids], dtype=torch.long, device=device)
    length = torch.tensor([min(len(tokens), data_cfg.get("max_len", 128))], dtype=torch.long, device=device)

    with torch.no_grad():
        logits = model(input_ids, length)
        probs = torch.softmax(logits, dim=1)[0]
        pred = int(probs.argmax().item())

    print(f"文本: {args.text}")
    print(f"预测: {LABEL_NAMES[pred]} (label={pred})")
    print(f"概率: 负面={probs[0].item():.4f} | 正面={probs[1].item():.4f}")


if __name__ == "__main__":
    main()
