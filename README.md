# prompt-autotune

 A light weight library that takes in a `task description` and a `prompt` and tunes the prompt to perform better.

 Accepting any and all PRs!

## Installation

```bash
pip install prompt-autotune
```

## Usage

### Basic usage

1. Import and initialize TunePrompt

```python
from prompt_autotune import TunePrompt
tuner = TunePrompt(
    task = "your task here",
    prompt = "your prompt here",
    verbose = True # makes it log updates
)
```

2. Call it as a function, the tuner will prompt you through the process through the command line

```python
tuner()
```

3. Once finished, access your tuned prompt

```python
new_prompt = tuner.prompt
```

### Command Line Tool

1. Type the command and press enter.

```bash
tune
```

2. Follow through the process.


3. The final prompt will be printed on the console.

Enjoy!