from typing import Any
from queue import Queue

from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import Callback
from typing_extensions import Self

from careamics_napari.signals.training_status import TrainUpdateType, TrainUpdate, TrainingState

class UpdaterCallBack(Callback):
    def __init__(self: Self, queue: Queue) -> None:
        self.queue = queue

    def on_train_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        # compute the number of batches
        self.queue.put(
            TrainUpdate(
                TrainUpdateType.MAX_BATCH,
                int(len(trainer.train_dataloader) / trainer.accumulate_grad_batches)
            )
        )

        # register number of epochs
        self.queue.put(
            TrainUpdate(
                TrainUpdateType.MAX_EPOCH,
                trainer.max_epochs
            )
        )

    def on_train_epoch_start(
        self, trainer: Trainer, pl_module: LightningModule
    ) -> None:
        self.queue.put(
            TrainUpdate(
                TrainUpdateType.EPOCH,
                trainer.current_epoch
            )
        )

    def on_train_epoch_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        metrics = trainer.progress_bar_metrics

        if "train_loss_epoch" in metrics:
            self.queue.put(
                TrainUpdate(
                    TrainUpdateType.LOSS,
                    metrics["train_loss_epoch"]
                )
            )

        if "val_loss" in metrics:
            self.queue.put(
                TrainUpdate(
                    TrainUpdateType.VAL_LOSS,
                    metrics["val_loss"]
                )
            )

    def on_train_batch_start(
        self, trainer: Trainer, pl_module: LightningModule, batch: Any, batch_idx: int
    ) -> None:
        self.queue.put(
            TrainUpdate(
                TrainUpdateType.BATCH,
                batch_idx
            )
        )
