from __future__ import annotations

from typing import List, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    """经典 TextCNN：多尺度卷积抓 n-gram 特征，适合文本分类入门。"""

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 128,
        num_classes: int = 2,
        kernel_sizes: Optional[List[int]] = None,
        num_filters: int = 64,
        dropout: float = 0.3,
        padding_idx: int = 0,
    ):
        super().__init__()
        kernel_sizes = kernel_sizes or [3, 4, 5]
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=padding_idx)
        self.convs = nn.ModuleList(
            [nn.Conv1d(embed_dim, num_filters, k) for k in kernel_sizes]
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(num_filters * len(kernel_sizes), num_classes)

    def forward(self, input_ids: torch.Tensor, lengths: Optional[torch.Tensor] = None) -> torch.Tensor:
        # [B, L, E] -> [B, E, L] for Conv1d
        x = self.embedding(input_ids).transpose(1, 2)
        feats = [F.relu(conv(x)).max(dim=2).values for conv in self.convs]
        x = torch.cat(feats, dim=1)
        x = self.dropout(x)
        return self.fc(x)
