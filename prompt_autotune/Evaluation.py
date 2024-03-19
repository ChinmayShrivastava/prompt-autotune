import re
from typing import List
from llama_index.llms.openai import OpenAI
from .GenerateExamples import Example
from .PROMPTS import EVALUATE_PROMPT

FORMAT_RESPONSE_TEMPLATE = """Example:

INPUT:
{input}

EXPECTED OUTPUT:
{output}

ACTUAL OUTPUT:
{response}"""

class Response:
    
    def __init__(
        self,
        id: int = None,
        prompt: str = None,
        response: str = None,
        example: Example = None
    ) -> None:
        self.id = id
        self.prompt = prompt
        self.response = response
        self.example = example

    def __str__(self) -> str:
        response_bit = self.response[:15] + "..." if len(self.response) > 15 else self.response
        return f"Response(response='{response_bit}')"
    
    def print_response(self) -> None:
        print(f"Response: {self}")
        print(f"Response: {self.response}")

    def format_response(self) -> str:
        return FORMAT_RESPONSE_TEMPLATE.format(
            input=self.example.input,
            output=self.example.output,
            response=self.response
        )

class EvaluatePrompt:

    def __init__(
        self,
        prompt: str = None,
        task: str = None,
        responses: List[Response] = None,
    ) -> None:
        if prompt is None:
            prompt = input("Enter prompt: ")
        if task is None:
            task = input("Enter task: ")
        self.prompt = prompt
        self.task = task
        self.responses = responses
        self.failures = ''
        self.scope_of_improvement = ''

    def __str__(self) -> str:
        prompt_bit = self.prompt[:15] + "..." if len(self.prompt) > 15 else self.prompt
        task_bit = self.task[:15] + "..." if len(self.task) > 15 else self.task
        return f"EvaluatePrompt(prompt='{prompt_bit}', task='{task_bit}')"
    
    def __call__(self, llm: OpenAI) -> None:
        self.evaluate_prompt(llm)

    def format_examples(self) -> str:
        return "\n\n".join([response.format_response() for response in self.responses])

    def evaluate_prompt(self, llm: OpenAI) -> None:
        prompt = EVALUATE_PROMPT.format(
            prompt=self.prompt,
            task_description=self.task,
            examples=self.format_examples()
        )
        evaluation = llm.complete(prompt).text
        failures, scope_of_improvement = re.split(r"Scope of Improvement:", evaluation)
        self.failures = failures
        self.scope_of_improvement = scope_of_improvement