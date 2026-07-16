from __future__ import annotations

from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

from src.datasets.vocab import Vocab, tokenize


class SentimentDataset(Dataset):
    def __init__(self, csv_path: str | Path, vocab: Vocab, max_len: int, tokenize_mode: str):
        df = pd.read_csv(csv_path)
        if not {"text", "label"}.issubset(df.columns):
            raise ValueError(f"{csv_path} 需要包含列: text, label")
        self.texts = df["text"].astype(str).tolist()
        self.labels = df["label"].astype(int).tolist()
        self.vocab = vocab
        self.max_len = max_len
        self.tokenize_mode = tokenize_mode

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        tokens = tokenize(self.texts[idx], self.tokenize_mode)
        ids = self.vocab.encode(tokens, self.max_len)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "label": torch.tensor(self.labels[idx], dtype=torch.long),
            "length": torch.tensor(min(len(tokens), self.max_len), dtype=torch.long),
        }


def build_dataloaders(
    train_path: str | Path,
    val_path: str | Path,
    tokenize_mode: str,
    max_len: int,
    min_freq: int,
    batch_size: int,
    num_workers: int = 0,
) -> tuple[DataLoader, DataLoader, Vocab]:
    train_df = pd.read_csv(train_path)
    vocab = Vocab.build(train_df["text"].astype(str).tolist(), tokenize_mode, min_freq)

    train_ds = SentimentDataset(train_path, vocab, max_len, tokenize_mode)
    val_ds = SentimentDataset(val_path, vocab, max_len, tokenize_mode)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    return train_loader, val_loader, vocab
