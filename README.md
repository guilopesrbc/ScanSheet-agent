from pydantic.color import ints_to_rgba

# ScanSheet Agent Library 
This library provides a simple interface to interact with the ScanSheet Agent, allowing you to processing form images into formatted JSON with values and columns using OpenAI's models.

## Installation

To install the ScanSheet Agent Library, you need to install all dependencies using pip:

```python
pip install .
```

If you want to install the development dependencies as well, use:
```python
pip install .[dev]
```

## Usage
To use the ScanSheet Agent Library, you can import it in your Python script.
```python
from scansheet_agent import ScanSheetAgent
from scansheet_agent import PromptBuilder
```

### Configuration
#### ScanSheet Agent
After importing, you can create an instance of the `ScanSheetAgent` class and use it to create ScanSheet Agent.

You need to provide your API key and the model you want to use (e.g., "gpt-4").

It's important that the model you choose is compatible with Image inputs, such as "gpt-4".

Check the OpenAI documentation for more details on model capabilities:
https://platform.openai.com/docs/guides/images-vision?api-mode=responses

```python
agent = ScanSheetAgent(api_key="your_api_key", model="gpt-4")
``` 

#### Variables and Inputs
You must to provide the image as a bytestring in variables when creating prompt.
You can also provide additional inputs that will be used in the prompt, available input is the "title" input.
```python
variables = {
    "image_url": "image_bytestring",
}

inputs = {
    "title": "Your document title",
}
```

#### Prompt Builder
You can use the `PromptBuilder` class to create prompts from templates.

It allows you to define user and system templates in a directory called "templates".

You can create a prompt using the `create_prompt` method, specifying the user and system templates along with any variables you want to include.
```python
prompt_builder = PromptBuilder(templates_dir="templates")

prompt = prompt_builder.create_prompt(
    user_template="USER.txt",
    system_template="SYSTEM.txt", 
    variables=variables
)
```

#### Invoke the Agent
Finally, you can invoke the agent using the `run` method, passing in the prompt and any additional inputs.
```python
response = agent.run(prompt=prompt, inputs=inputs)
```