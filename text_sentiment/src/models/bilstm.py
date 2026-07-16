import torch
import torch.nn as nn


class BiLSTMClassifier(nn.Module):
    """双向 LSTM 分类器：适合理解序列建模。"""

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 128,
        hidden_dim: int = 128,
        num_layers: int = 1,
        num_classes: int = 2,
        dropout: float = 0.3,
        padding_idx: int = 0,
    ):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=padding_idx)
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, input_ids: torch.Tensor, lengths: torch.Tensor | None = None) -> torch.Tensor:
        x = self.embedding(input_ids)
        if lengths is not None:
            lengths = lengths.cpu().clamp(min=1)
            packed = nn.utils.rnn.pack_padded_sequence(
                x, lengths, batch_first=True, enforce_sorted=False
            )
            packed_out, (h_n, _) = self.lstm(packed)
            # h_n: [num_layers * 2, B, H] -> take last layer fwd/bwd
            forward_last = h_n[-2]
            backward_last = h_n[-1]
            feat = torch.cat([forward_last, backward_last], dim=1)
        else:
            _, (h_n, _) = self.lstm(x)
            feat = torch.cat([h_n[-2], h_n[-1]], dim=1)
        feat = self.dropout(feat)
        return self.fc(feat)
