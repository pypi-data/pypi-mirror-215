from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import optuna
import torch
from mmengine.registry import LOOPS
from mmengine.runner.loops import EpochBasedTrainLoop
from torch.utils.data import DataLoader


@LOOPS.register_module()
class EpochBasedOptunaLoop(EpochBasedTrainLoop):
    """Loop for epoch-based training in optuna hyperparameter search."""

    def __init__(
        self,
        runner,
        dataloader: Union[DataLoader, Dict],
        objective_metric: str,
        max_epochs: int = 1,
        val_begin: int = 1,
        val_interval: int = 1,
        dynamic_intervals: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        """
        Parameters
        ----------
        runner : Runner
            A reference of runner.
        dataloader : Union[Dataloader, Dict]
            A dataloader object or a dict to build a dataloader.
        objective_metric : str
            Target metric for hyperparameters optimization.
        max_epochs : int
            Total training epochs.
        val_begin : int
            The epoch at which model validation begins. Default value is 1.
        val_interval : int
            Validation interval. Default value is 1.
        dynamic_intervals : Optional[List[Tuple[int, int]]]
            The first element in the tuple is a milestone and the second
            element is an interval. The interval is used after the
            corresponding milestone. Default value is None.
        """
        super().__init__(
            runner=runner,
            dataloader=dataloader,
            max_epochs=max_epochs,
            val_begin=val_begin,
            val_interval=val_interval,
            dynamic_intervals=dynamic_intervals,
        )
        self._objective_metric = objective_metric

    def run(self) -> torch.nn.Module:
        """Launch training."""
        self.runner.call_hook('before_train')

        while self._epoch < self._max_epochs and not self.stop_training:
            self.run_epoch()

            self._decide_current_val_interval()
            if (
                self.runner.val_loop is not None
                and self._epoch >= self.val_begin
                and self._epoch % self.val_interval == 0
            ):
                metrics = self.runner.val_loop.run()
                self.runner.trial.report(metrics[self._objective_metric], self.epoch)
                self.runner.objective = metrics[self._objective_metric]
                if self.runner.trial.should_prune():
                    raise optuna.TrialPruned()

        self.runner.call_hook('after_train')
        return self.runner.model
