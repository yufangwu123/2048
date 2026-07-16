#!/usr/bin/env python3
"""训练入口：python scripts/train.py --config configs/train.yaml"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn as nn

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.datasets.sentiment import build_dataloaders
from src.models.factory import build_model
from src.trainers.trainer import Trainer
from src.utils.config import load_config, resolve_device
from src.utils.seed import set_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="文本情感分类训练")
    parser.add_argument("--config", type=str, default="configs/train.yaml")
    parser.add_argument("--model", type=str, default=None, help="覆盖配置里的模型名")
    parser.add_argument("--epochs", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(ROOT / args.config)
    set_seed(cfg.get("seed", 42))

    device = resolve_device(cfg.get("device", "auto"))
    print(f"device = {device}")

    data_cfg = cfg["data"]
    model_cfg = cfg["model"]
    train_cfg = cfg["train"]
    out_cfg = cfg["output"]

    if args.model:
        model_cfg["name"] = args.model
    if args.epochs is not None:
        train_cfg["epochs"] = args.epochs

    train_loader, val_loader, vocab = build_dataloaders(
        train_path=ROOT / data_cfg["train_path"],
        val_path=ROOT / data_cfg["val_path"],
        tokenize_mode=data_cfg.get("tokenize", "char"),
        max_len=data_cfg.get("max_len", 128),
        min_freq=data_cfg.get("min_freq", 1),
        batch_size=data_cfg.get("batch_size", 32),
        num_workers=data_cfg.get("num_workers", 0),
    )
    print(f"vocab_size = {len(vocab)} | train={len(train_loader.dataset)} | val={len(val_loader.dataset)}")

    vocab_path = ROOT / out_cfg["vocab_file"]
    vocab.save(vocab_path)
    print(f"vocab saved -> {vocab_path}")

    model = build_model(model_cfg["name"], len(vocab), model_cfg)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=train_cfg.get("lr", 1e-3),
        weight_decay=train_cfg.get("weight_decay", 0.0),
    )
    criterion = nn.CrossEntropyLoss()

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        device=device,
        grad_clip=train_cfg.get("grad_clip", 5.0),
    )

    ckpt_path = ROOT / out_cfg["best_model"]
    result = trainer.fit(
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=train_cfg.get("epochs", 8),
        ckpt_path=ckpt_path,
        patience=train_cfg.get("early_stop_patience", 3),
    )

    history_path = ROOT / out_cfg["dir"] / "history.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"训练完成：best_epoch={result['best_epoch']} best_f1={result['best_f1']:.4f}")
    print(f"history -> {history_path}")


if __name__ == "__main__":
    main()
