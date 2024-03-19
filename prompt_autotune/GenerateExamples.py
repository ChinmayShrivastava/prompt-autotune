from .PROMPTS import GENERATE_N_EXAMPLES
from llama_index.llms.openai import OpenAI
import re
from typing import List
import logging

class Example:

    def __init__(
        self,
        id = None,
        input = None,
        output = None,
    ):
        self.id = id
        self.input = input
        self.output = output
        self.use = False

    def __str__(self):
        input_bit = self.input[:15] + "..." if len(self.input) > 15 else self.input
        output_bit = self.output[:15] + "..." if len(self.output) > 15 else self.output
        return f"Example(input='{input_bit}', output='{output_bit}')"
    
    def print_example(self):
        print(f"Example: {self.id}")
        print(f"Input: {self.input}")
        print(f"Output: {self.output}")

class GenerateExamples:

    def __init__(
        self
        ,task_description: str
        ,number_of_examples: int
    ) -> None:
        self.task_description = task_description
        self.number_of_examples = number_of_examples
        self.prompt = GENERATE_N_EXAMPLES.format(
            task_description=task_description,
            number_of_examples=number_of_examples
        )

    def __call__(self, llm: OpenAI) -> List[Example]:
        logging.info(f"Generating {self.number_of_examples} examples for task: {self.task_description[:15]}...")
        response = llm.complete(self.prompt).text
        logging.info("Completed")
        parsed_examples = self._parse_examples(response)
        return parsed_examples

    def _parse_examples(self, response: str) -> List[Example]:
        # add "\n\n" to the end of the response to make sure the last example is parsed
        response += "\n\n"
        example_regex = re.compile(r'Example (\d+):\nINPUT: (.+?)\n\nOUTPUT: (.+?)\n\n', re.DOTALL)
        examples = example_regex.findall(response)
        return [Example(id=i, input=inp, output=out) for i, (inp, out) in enumerate(examples)]
    
    def __str__(self) -> str:
        task_bit = self.task_description[:15] + "..." if len(self.task_description) > 15 else self.task_description
        return f"GenerateExamples(task_description='{task_bit}', number_of_examples={self.number_of_examples})"