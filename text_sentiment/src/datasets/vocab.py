from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

PAD_TOKEN = "<pad>"
UNK_TOKEN = "<unk>"


def tokenize(text: str, mode: str = "char") -> list[str]:
    text = text.strip().lower()
    if mode == "word":
        # 英文按空格/标点切分；中文若已空格分词也可直接用
        return [t for t in re.findall(r"[\w']+|[^\w\s]", text, re.UNICODE) if t.strip()]
    # 默认按字：中文入门最稳，不依赖额外分词库
    return list(text.replace(" ", ""))


class Vocab:
    def __init__(self, token_to_id: dict[str, int]):
        self.token_to_id = token_to_id
        self.id_to_token = {i: t for t, i in token_to_id.items()}
        self.pad_id = token_to_id[PAD_TOKEN]
        self.unk_id = token_to_id[UNK_TOKEN]

    def __len__(self) -> int:
        return len(self.token_to_id)

    def encode(self, tokens: list[str], max_len: int) -> list[int]:
        ids = [self.token_to_id.get(t, self.unk_id) for t in tokens[:max_len]]
        if len(ids) < max_len:
            ids.extend([self.pad_id] * (max_len - len(ids)))
        return ids

    @classmethod
    def build(cls, texts: Iterable[str], tokenize_mode: str = "char", min_freq: int = 1) -> "Vocab":
        counter: Counter[str] = Counter()
        for text in texts:
            counter.update(tokenize(text, tokenize_mode))

        token_to_id = {PAD_TOKEN: 0, UNK_TOKEN: 1}
        for token, freq in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
            if freq < min_freq:
                continue
            if token not in token_to_id:
                token_to_id[token] = len(token_to_id)
        return cls(token_to_id)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.token_to_id, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "Vocab":
        with open(path, "r", encoding="utf-8") as f:
            token_to_id = json.load(f)
        return cls(token_to_id)
