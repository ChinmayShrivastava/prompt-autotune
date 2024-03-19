from .TunePrompt import TunePrompt

def main():
    tuner = TunePrompt()
    tuner()
    print("============FINAL PROMPT============")
    print(tuner.prompt)
    print("===================================")