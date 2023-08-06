import argparse
import os.path as osp

import optuna
from mmengine.config import Config
from mmengine.config import DictAction
from mmengine.runner import Runner

from mmenot.loops import EpochBasedOptunaLoop  # pylint: disable=unused-import
from mmenot.utils.common import from_cfg
from mmenot.utils.hpo import Objective
from mmenot.utils.hpo import SaveBestTrialCallback

Runner.from_cfg = classmethod(from_cfg)  # type: ignore


def parse_args():  # pylint: disable=missing-function-docstring
    parser = argparse.ArgumentParser(description='Search optimal hyperparameters')
    parser.add_argument('config', help='train config file path')
    parser.add_argument('--checkpoint', type=str, default='', help='path to checkpoint, overrides model config')
    parser.add_argument('--enable-logging', nargs='?', const=True, default=False, help='enable logging')
    parser.add_argument('--work-dir', help='the dir to save logs and models')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.',
    )
    parser.add_argument(
        '--objective-metric',
        type=str,
        default='pascal_voc/mAP',
        help='Target metric for hyperparameters optimization process',
    )
    parser.add_argument(
        '--n-trials',
        type=int,
        default=300,
        help='Number of trials for hyperparameters search',
    )
    parser.add_argument(
        '--lr-range',
        type=float,
        default=[1e-5, 1e-2],
        nargs=2,
        help='Learning rate range',
    )
    parser.add_argument(
        '--optimizers',
        type=str,
        default=['SGD', 'AdamW', 'RAdam'],
        nargs='+',
        help='PyTorch optimizers. SGD, Adam, AdamW and RAdam supported for now.',
    )
    parser.add_argument(
        '--warmup-range',
        type=int,
        default=[500, 1500],
        nargs=2,
        help='Warmup iterations range',
    )

    args = parser.parse_args()
    return args


def search_hyps():  # pylint: disable=missing-function-docstring
    args = parse_args()

    try:
        # pylint: disable=import-outside-toplevel
        from mmdet.utils import setup_cache_size_limit_of_dynamo

        setup_cache_size_limit_of_dynamo()
    except ImportError:
        pass

    # Will be moved to the main import section when logging will be merged into main branch.
    if args.enable_logging:
        # pylint: disable=C0415
        import enot.logging
        from loguru import logger

        enot.logging.enable_logging()
        logger.add('mmenot.log')

    cfg = Config.fromfile(args.config)
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    if args.work_dir is not None:
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        cfg.work_dir = osp.join('./work_dirs', osp.splitext(osp.basename(args.config))[0])

    if args.checkpoint:
        cfg['model'] = args.checkpoint  # replace model config by checkpoint path

    cfg['train_cfg']['type'] = 'EpochBasedOptunaLoop'
    cfg['train_cfg'].pop('max_iters', None)  # remove max_iters for EpochBasedPruningLoop
    cfg['train_cfg']['objective_metric'] = args.objective_metric
    cfg['low_lr'], cfg['high_lr'] = args.lr_range
    cfg['optimizers'] = args.optimizers
    cfg['low_warmup'], cfg['high_warmup'] = args.warmup_range
    cfg['base_work_dir'] = cfg['work_dir']

    max_epochs = cfg['train_cfg']['max_epochs']
    val_begin = cfg['train_cfg'].get('val_begin', 1)
    val_interval = cfg['train_cfg'].get('val_interval', 1)

    if max_epochs < val_begin or max_epochs // val_interval == 0:
        raise ValueError(
            'Validation is required to optimize hyperparameters. Config specifies training without validation. '
            'HPO can not be performed, please specify validation. '
            f'Relevant parameters: max_epochs={max_epochs}, val_begin={val_begin}, val_interval={val_interval}.'
        )

    study = optuna.create_study(
        sampler=optuna.samplers.TPESampler(),
        pruner=optuna.pruners.HyperbandPruner(),
        direction='maximize',
    )
    study.optimize(
        func=Objective(cfg),
        n_trials=args.n_trials,
        callbacks=[SaveBestTrialCallback(cfg['base_work_dir'])],
    )


if __name__ == '__main__':
    search_hyps()
