from __future__ import annotations

from typing import Any, Dict

import torch.nn as nn

from src.models.bilstm import BiLSTMClassifier
from src.models.textcnn import TextCNN


def build_model(name: str, vocab_size: int, cfg: Dict[str, Any]) -> nn.Module:
    name = name.lower()
    if name == "textcnn":
        return TextCNN(
            vocab_size=vocab_size,
            embed_dim=cfg.get("embed_dim", 128),
            num_classes=cfg.get("num_classes", 2),
            kernel_sizes=cfg.get("kernel_sizes", [3, 4, 5]),
            num_filters=cfg.get("num_filters", 64),
            dropout=cfg.get("dropout", 0.3),
        )
    if name == "bilstm":
        return BiLSTMClassifier(
            vocab_size=vocab_size,
            embed_dim=cfg.get("embed_dim", 128),
            hidden_dim=cfg.get("hidden_dim", 128),
            num_layers=cfg.get("num_layers", 1),
            num_classes=cfg.get("num_classes", 2),
            dropout=cfg.get("dropout", 0.3),
        )
    raise ValueError(f"未知模型: {name}，可选: textcnn, bilstm")
