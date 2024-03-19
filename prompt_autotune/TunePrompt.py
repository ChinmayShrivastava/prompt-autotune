from typing import List
from llama_index.llms.openai import OpenAI
import logging
from .GenerateExamples import Example, GenerateExamples
from .Evaluation import Response, EvaluatePrompt
from .PROMPTS import TUNE_PROMPT_PROMPT
import tqdm
from dotenv import load_dotenv

load_dotenv()

class TunePrompt:

    def __init__(
        self,
        prompt: str = None,
        task: str = None,
        examples: List[Example] = None,
        powerllm: OpenAI = OpenAI("gpt-4-turbo-preview", max_tokens=2048),
        llm: OpenAI = OpenAI("gpt-4"),
        number_of_examples: int = 10,
        number_of_cycles: int = 3,
        verbose: bool = True
    ) -> None:
        if task is None:
            task = input("Enter task: ")
        if prompt is None:
            prompt = input("Enter prompt: ")
        self.prompt = prompt
        self.task = task
        self.powerllm = powerllm
        self.llm = llm
        self.number_of_examples = number_of_examples
        if examples is None:
            examples = GenerateExamples(task, number_of_examples)(powerllm)
        self.examples = examples
        self.number_of_cycles = number_of_cycles
        self.cycle_tracker = {i: {
            'responses': []
        } for i in range(number_of_cycles)}
        self.verbose = verbose
        if self.verbose:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(logging.StreamHandler())

    def __str__(self) -> str:
        prompt_bit = self.prompt[:15] + "..." if len(self.prompt) > 15 else self.prompt
        task_bit = self.task[:15] + "..." if len(self.task) > 15 else self.task
        return f"TunePrompt(prompt='{prompt_bit}', task='{task_bit}')"
    
    def __call__(self) -> str:
        self.run_prompt_tuning_pipeline()

    def run_prompt_tuning_pipeline(self) -> str:
        self.human_feedback_on_examples()
        for cycle_no in range(self.number_of_cycles):
            self.generate_responses_from_prompt(cycle_no)
            self.evaluate_responses(cycle_no)
            self.tune_prompt(cycle_no)
        return self.prompt
    
    def human_feedback_on_examples(self) -> None:
        # for examples in self.examples ask for human feedback on whether to use the example or not
        for example in self.examples:
            example.print_example()
            feedback = input("Use this example? (y/n): ")
            example.use = feedback == "y"

    def generate_responses_from_prompt(self, cycle_no) -> None:
        # for each example generate a response from the prompt
        self.logger.info(f"Generating responses for cycle {cycle_no}")
        for example in tqdm.tqdm(self.examples):
            if example.use:
                response = self.llm.complete(self.prompt + "\nInput:" + example.input + "\nOutput:").text
                self.cycle_tracker[cycle_no]['responses'].append(Response(prompt=self.prompt, response=response, example=example))

    def evaluate_responses(self, cycle_no) -> None:
        self.logger.info(f"Evaluating responses for cycle {cycle_no}")
        eval = EvaluatePrompt(prompt=self.prompt, task=self.task, responses=self.cycle_tracker[cycle_no]['responses'])
        eval(self.llm)
        self.cycle_tracker[cycle_no]['eval'] = eval

    def tune_prompt(self, cycle_no) -> None:
        self.logger.info(f"Old prompt: {self.prompt[:15]}...")
        scope_of_improvement = self.cycle_tracker[cycle_no]['eval'].scope_of_improvement
        _prompt = TUNE_PROMPT_PROMPT.format(task_description=self.task, prompt=self.prompt, scope_of_improvement=scope_of_improvement)
        new_prompt = self.llm.complete(_prompt).text
        self.cycle_tracker[cycle_no]['old_prompt'] = self.prompt
        self.cycle_tracker[cycle_no]['new_prompt'] = new_prompt
        self.prompt = new_prompt
        self.logger.info(f"New prompt: {new_prompt[:15]}...")