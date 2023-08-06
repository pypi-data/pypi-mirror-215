from mmengine.runner import Runner


class Objective:  # pylint: disable=missing-class-docstring
    def __init__(self, config):
        self.config = config

    def __call__(self, trial):
        lr = trial.suggest_float(  # pylint: disable=C0103
            name='lr',
            low=self.config['low_lr'],
            high=self.config['high_lr'],
            log=True,
        )
        warmup = trial.suggest_int(
            name='warmup',
            low=self.config['low_warmup'],
            high=self.config['high_warmup'],
        )
        optimizer = trial.suggest_categorical(name='optimizer', choices=self.config['optimizers'])

        default_optimizer_options = self.config['optim_wrapper']['optimizer']

        opt_kwargs = {}

        if optimizer == 'SGD':
            for parameter in ('momentum', 'weight_decay'):
                if parameter in default_optimizer_options:
                    opt_kwargs[parameter] = default_optimizer_options[parameter]

        if optimizer in ('Adam', 'AdamW', 'RAdam'):
            for parameter in ('betas', 'weight_decay'):
                if parameter in default_optimizer_options:
                    opt_kwargs[parameter] = default_optimizer_options[parameter]

        self.config['optim_wrapper']['optimizer'] = dict(type=optimizer, lr=lr, **opt_kwargs)
        self.config['param_scheduler'][0]['end'] = warmup
        self.config['work_dir'] = self.config['base_work_dir'] + f'/lr={lr:1.7f}_wu={warmup}_opt={optimizer}'
        runner = Runner.from_cfg(self.config)
        runner.trial = trial  # type: ignore
        runner.train()
        return runner.objective


class SaveBestTrialCallback:  # pylint: disable=missing-class-docstring
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.best_trial = None

    def __call__(self, study, trial):
        if self.best_trial is None or self.best_trial.number != study.best_trial.number:
            self.best_trial = trial
            with open(file=f'{self.work_dir}/trials.txt', mode='a+', encoding='utf-8') as file:
                file.write(f'Best trial: {trial.number}, best value: {trial.value}, best params: {trial.params}\n')
