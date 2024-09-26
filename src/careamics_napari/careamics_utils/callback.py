from typing import Any
from queue import Queue

from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import Callback
from typing_extensions import Self

from careamics_napari.signals import (
    TrainUpdateType, 
    TrainUpdate,
    PredictionUpdate,
    PredictionUpdateType
)

class UpdaterCallBack(Callback):
    def __init__(self: Self, training_queue: Queue, prediction_queue: Queue) -> None:
        self.training_queue = training_queue
        self.prediction_queue = prediction_queue

    def get_train_queue(self) -> Queue:
        return self.training_queue
    
    def get_predict_queue(self) -> Queue:
        return self.prediction_queue

    def on_train_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        # compute the number of batches
        self.training_queue.put(
            TrainUpdate(
                TrainUpdateType.MAX_BATCH,
                int(len(trainer.train_dataloader) / trainer.accumulate_grad_batches)
            )
        )

        # register number of epochs
        self.training_queue.put(
            TrainUpdate(
                TrainUpdateType.MAX_EPOCH,
                trainer.max_epochs
            )
        )

    def on_train_epoch_start(
        self, trainer: Trainer, pl_module: LightningModule
    ) -> None:
        self.training_queue.put(
            TrainUpdate(
                TrainUpdateType.EPOCH,
                trainer.current_epoch
            )
        )

    def on_train_epoch_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        metrics = trainer.progress_bar_metrics

        if "train_loss_epoch" in metrics:
            self.training_queue.put(
                TrainUpdate(
                    TrainUpdateType.LOSS,
                    metrics["train_loss_epoch"]
                )
            )

        if "val_loss" in metrics:
            self.training_queue.put(
                TrainUpdate(
                    TrainUpdateType.VAL_LOSS,
                    metrics["val_loss"]
                )
            )

    def on_train_batch_start(
        self, trainer: Trainer, pl_module: LightningModule, batch: Any, batch_idx: int
    ) -> None:
        self.training_queue.put(
            TrainUpdate(
                TrainUpdateType.BATCH,
                batch_idx
            )
        )


    def on_predict_start(
            self, trainer: Trainer, pl_module: LightningModule
    ) -> None:
        self.prediction_queue.put(
            TrainUpdate(
                PredictionUpdateType.MAX_SAMPLES,
                trainer.num_predict_batches
            )
        )


    def on_predict_batch_start(
            self, 
            trainer: Trainer, 
            pl_module: LightningModule, 
            batch: Any, 
            batch_idx: int, 
            dataloader_idx: int = 0
    ) -> None:
        self.prediction_queue.put(
            PredictionUpdate(
                PredictionUpdateType.SAMPLE,
                batch_idx
            )
        )
        
