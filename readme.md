About
=====

Connect4 reinforcement learning by [AlphaGo Zero](https://deepmind.com/blog/alphago-zero-learning-scratch/) methods.

This project is based in two main resources:
1) DeepMind's Oct19th publication: [Mastering the Game of Go without Human Knowledge](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ).
2) The <b>great</b> Reversi development of the DeepMind ideas that @mokemokechicken did in his repo: https://github.com/mokemokechicken/reversi-alpha-zero


Environment
-----------

* Python 3.6.13
* tensorflow: 1.14.0
* Keras: 2.3.1

Modules
-------

### Reinforcement Learning

This AlphaGo Zero implementation consists of three worker `self`, `opt` and `eval`.

* `self` is Self-Play to generate training data by self-play using BestModel.
* `opt` is Trainer to train model, and generate next-generation models.
* `eval` is Evaluator to evaluate whether the next-generation model is better than BestModel. If better, replace BestModel.

### Evaluation

For evaluation, you can play chess with the BestModel.

* `play_gui` is Play Game vs BestModel using ASCII character encoding.

Data
-----

* `data/model/model_best_*`: BestModel.
* `data/model/next_generation/*`: next-generation models.
* `data/play_data/play_*.json`: generated training data.
* `logs/main.log`: log file.
  
If you want to train the model from the beginning, delete the above directories.

How to use
==========

Setup
-------
### install libraries
```bash
pyenv virtualenv 3.6.13 connect4
pyenv activate connect4
pip install -r requirements.txt
```

### set environment variables
Create `.env` file and write this.

```text:.env
KERAS_BACKEND=tensorflow
```


Basic Usages
------------

For training model, execute `Self-Play`, `Trainer` and `Evaluator`. 


Self-Play
--------

```bash
python src/connect4_zero/run.py self --new
```

When executed, Self-Play will start using BestModel.
If the BestModel does not exist, new random model will be created and become BestModel.

### options
* `--new`: create new BestModel
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)

Trainer
-------

```bash
python src/connect4_zero/run.py opt
```

When executed, Training will start.
A base model will be loaded from latest saved next-generation model. If not existed, BestModel is used.
Trained model will be saved every 2000 steps(mini-batch) after epoch. 

### options
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)
* `--total-step`: specify total step(mini-batch) numbers. The total step affects learning rate of training. 

Evaluator
---------

```bash
python src/connect4_zero/run.py eval
```

When executed, Evaluation will start.
It evaluates BestModel and the latest next-generation model by playing about 200 games.
If next-generation model wins, it becomes BestModel. 

### options
* `--type mini`: use mini config for testing, (see `src/connect4_zero/configs/mini.py`)

Play Game
---------

```bash
python src/connect4_zero/run.py play_gui
```


When executed, ordinary chess board will be displayed in ASCII code and you can play against BestModel.


Tips and Memo
====

GPU Memory
----------

Usually the lack of memory cause warnings, not error.
If error happens, try to change `per_process_gpu_memory_fraction` in `src/worker/{evaluate.py,optimize.py,self_play.py}`,

```python
tf_util.set_session_config(per_process_gpu_memory_fraction=0.2)
```

Less batch_size will reduce memory usage of `opt`.
Try to change `TrainerConfig#batch_size` in `NormalConfig`.


Model Performance
-------

The following table is records of the best models.

|best model generation|winning percentage to best model|Time Spent(hours)|note|
|-----|-----|-----|-----|
|1|-|-|　|
|2|100%|1| |
|3|84,6%|1| |
|4|78,6%|2| This model is good enough to avoid naive losing movements |
|5|100%|1| The NN learns to play always in the center when it moves first |
|6|100%|4| The model now is able to win any online Connect4 game with classic AI I've found |


