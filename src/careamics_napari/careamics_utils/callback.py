from dataclasses import dataclass
from enum import IntEnum
from typing import Any

from psygnal import evented
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import Callback
from typing_extensions import Self


class TrainingState(IntEnum):
    IDLE = 0
    TRAINING = 1
    DONE = 2
    STOPPED = 3
    CRASHED = 4


@evented
@dataclass
class TrainingStatus:
    n_epochs: int = -1
    n_batches: int = -1
    epoch_idx: int = -1
    batch_idx: int = -1
    loss: float = -1
    val_loss: float = -1
    state: TrainingState = TrainingState.IDLE


class UpdaterCallBack(Callback):
    def __init__(self: Self, train_status: TrainingStatus) -> None:
        self.train_status = train_status

    def on_train_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        # compute the number of batches
        self.train_status.n_batches = (
            len(trainer.train_dataloader) / trainer.accumulate_grad_batches
        )

        # register number of epochs
        self.train_status.n_epochs = trainer.max_epochs

    def on_train_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        self.train_status.state = TrainingState.DONE

    def on_train_epoch_start(
        self, trainer: Trainer, pl_module: LightningModule
    ) -> None:
        self.train_status.epoch_idx = trainer.current_epoch

    def on_train_epoch_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        metrics = trainer.progress_bar_metrics

        if "train_loss_epoch" in metrics:
            self.train_status.loss = metrics["train_loss_epoch"]

        if "val_loss" in metrics:
            self.train_status.val_loss = metrics["val_loss"]

    def on_train_batch_start(
        self, trainer: Trainer, pl_module: LightningModule, batch: Any, batch_idx: int
    ) -> None:
        self.train_status.batch_idx = batch_idx
