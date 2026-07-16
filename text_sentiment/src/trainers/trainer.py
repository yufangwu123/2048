from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score
from tqdm import tqdm


class Trainer:
    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        device: str,
        grad_clip: float = 5.0,
    ):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.grad_clip = grad_clip
        self.history: dict[str, list[float]] = {
            "train_loss": [],
            "val_loss": [],
            "val_acc": [],
            "val_f1": [],
        }

    def _run_epoch(self, loader, train: bool = True) -> dict[str, float]:
        self.model.train(train)
        total_loss = 0.0
        all_preds: list[int] = []
        all_labels: list[int] = []

        context = torch.enable_grad() if train else torch.no_grad()
        with context:
            for batch in tqdm(loader, desc="train" if train else "val", leave=False):
                input_ids = batch["input_ids"].to(self.device)
                labels = batch["label"].to(self.device)
                lengths = batch["length"].to(self.device)

                if train:
                    self.optimizer.zero_grad()

                logits = self.model(input_ids, lengths)
                loss = self.criterion(logits, labels)

                if train:
                    loss.backward()
                    if self.grad_clip > 0:
                        nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
                    self.optimizer.step()

                total_loss += loss.item() * input_ids.size(0)
                preds = logits.argmax(dim=1)
                all_preds.extend(preds.detach().cpu().tolist())
                all_labels.extend(labels.detach().cpu().tolist())

        n = len(loader.dataset)
        return {
            "loss": total_loss / max(n, 1),
            "acc": accuracy_score(all_labels, all_preds),
            "f1": f1_score(all_labels, all_preds, average="macro", zero_division=0),
        }

    def fit(
        self,
        train_loader,
        val_loader,
        epochs: int,
        ckpt_path: str | Path,
        patience: int = 3,
    ) -> dict[str, Any]:
        ckpt_path = Path(ckpt_path)
        ckpt_path.parent.mkdir(parents=True, exist_ok=True)

        best_f1 = -1.0
        best_epoch = -1
        wait = 0

        for epoch in range(1, epochs + 1):
            train_metrics = self._run_epoch(train_loader, train=True)
            val_metrics = self._run_epoch(val_loader, train=False)

            self.history["train_loss"].append(train_metrics["loss"])
            self.history["val_loss"].append(val_metrics["loss"])
            self.history["val_acc"].append(val_metrics["acc"])
            self.history["val_f1"].append(val_metrics["f1"])

            print(
                f"Epoch {epoch:02d}/{epochs} | "
                f"train_loss={train_metrics['loss']:.4f} | "
                f"val_loss={val_metrics['loss']:.4f} | "
                f"val_acc={val_metrics['acc']:.4f} | "
                f"val_f1={val_metrics['f1']:.4f}"
            )

            if val_metrics["f1"] > best_f1:
                best_f1 = val_metrics["f1"]
                best_epoch = epoch
                wait = 0
                torch.save(
                    {
                        "model_state": self.model.state_dict(),
                        "epoch": epoch,
                        "val_f1": best_f1,
                        "val_acc": val_metrics["acc"],
                    },
                    ckpt_path,
                )
                print(f"  -> 保存最优模型到 {ckpt_path} (val_f1={best_f1:.4f})")
            else:
                wait += 1
                if wait >= patience:
                    print(f"早停：连续 {patience} 轮验证集未提升")
                    break

        return {"best_epoch": best_epoch, "best_f1": best_f1, "history": self.history}
