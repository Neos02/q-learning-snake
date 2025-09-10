# Snake Q-Learning

An implementation of snake using pygame that can be played by a person or an agent using Q-Learning.

## Play it Yourself

Run with `--mode 0` or `-m 0` and use W, A, S, and D to move the snake around. This is the default mode.

## Train from Scratch

Run with `--mode 1` or `-m 1` and watch as the agent learns. A preview will be shown every so often to see how well the agent is doing and the average score and survival rates are printed regularly.

## Load and Train from Existing Model

Run with `--mode 2` or `-m 2` and provide an episode number to load using `--episode {number}` or `-e {number}`. If the model exists it will be loaded from the file and continue training.

## Load and Run from Existing Model

Run with `--mode 3` or `-m 3` and provide an episode number to load using `--episode {number}` or `-e {number}`. If the model exists it will be loaded from the file and will play one game.

## Additional Options

- `--model-dir {directory}`|`-d {directory}`: the directory to store the models in