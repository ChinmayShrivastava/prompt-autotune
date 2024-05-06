from prompt_autotune.TunePrompt import TunePrompt
import logging

logging.basicConfig(level=logging.INFO)

def main(
	task,
	prompt
):

	# Create a new TunePrompt object
	tuner = TunePrompt(
		task=task,
		prompt=prompt
	)

	# Run the tuning pipeline
	tuner()

	# Return the tuned prompt
	return tuner.prompt

if __name__ == "__main__":
	task = "Translate English to French"
	prompt = "Translate the following English text to French:"
	prompt = main(
		task=task,
		prompt=prompt
	)
	print(prompt)