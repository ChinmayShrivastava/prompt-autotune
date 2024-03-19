GENERATE_N_EXAMPLES = """As an advanced language model, you are to perform a task of generating examples given the instructions.

You are given a task description.

Based on the task description you need to generate {number_of_examples} input output examples that can then be used to train a model for that specific use case.

Additional Instructions:
1. The generated samples should be diverse
2. Each generated example should have the format-
---
Example 1:
INPUT: input content here
OUTPUT: output content here
---
Example 2:
INPUT: input content here
OUTPUT: output content here
and so on...
---
3. They should effectively capture edge cases for the given task description.
4. Each output should be strictly related to the generated input.

Task Description:
{task_description}"""

EVALUATE_PROMPT = """As an advanced language model, you are to perform an evaluation of a prompt based on it's performance as described by the task description. The evaluation is performed on the responses it generated when passed into an AI model measured against expected output responses.

Instructions:
1. Provide critique of what the prompt did wrong.
2. Provide a constructive list of what needs to change in the prompt to make it better and handle all edge cases effectively.
3. The output should be a list of 5 failures and 5 scope of improvements in the following format:
FAILURES:
1. ...
2. ...
and so on
Scope of Improvement:
1. ...
2. ...
and so on.

Prompt:
{prompt}

Task Description:
{task_description}

Examples:
{examples}

Response:"""

TUNE_PROMPT_PROMPT = """As an advanced language model, you are to improve the performance of a prompt tasked to perform a task as described. The prompt was tested on some training examples and evaluated based on its performance. Use the Scope of Improvement to tune the prompt into performing the task better.

Instructions:
1. Ensure the prompt does the job as described by the task description and remains within scope.
2. Ensure that the prompt can encompass all potential cases and doesn't overfit.
3. Keep the prompt short, which helps the prompt to not overfit.

Task Description:
{task_description}

Prompt:
{prompt}

Scope of Improvement:
{scope_of_improvement}

TUNED PROMPT:"""