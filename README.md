# ScanSheet Agent Library 
This library provides a simple interface to interact with the ScanSheet Agent, allowing you to processing form images into formatted JSON with values and columns using OpenAI's models.

## Installation
To install the ScanSheet Agent Library, you need to install the library using pip:
```bash
pip install git+https://github.com/guilopesrbc/ScanSheet-agent.git@<version>
```

If you want to install it from the local source code, you can clone the repository and run the following command in the root directory of the project:
```bash
pip install .
```

If you want to install the development dependencies as well, use:
```bash
pip install .[dev]
```

## Usage

To use the ScanSheet Agent Library, you can import it in your Python script.
```python
from scansheet_agent.agent import ScanSheetAgent
from scansheet_agent.prompt import PromptBuilder
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
You must to provide the image as a bytestring in variables and a valid ```scansheet_agent.schemas.DocumentTypeEnum``` when creating prompt.
You can also provide additional inputs that will be used in the prompt, check project prompts to use availables input.
```python
variables = {
    "image_base64": "Your image as a base64 encoded string",
    "title": "Your document type title",
}

inputs = {
    'some_input': "Some input value",
}
```

#### Prompt Builder
You can use the `PromptBuilder` class to create prompts from templates.

It allows you to define user and system templates in a directory called "templates".

You can create a prompt using the `create_prompt` method, specifying the system templates available and with your variables.
```python
prompt_builder = PromptBuilder(templates_dir="templates")

prompt = prompt_builder.create_prompt(
    system_template="Sytem template available, default is 'SYSTEM.txt'", 
    variables=variables
)
```

#### Invoke the Agent
Finally, you can invoke the agent using the `run` method, passing in the prompt and any additional inputs.
```python
response = agent.run(prompt=prompt, inputs=inputs) 
# inputs is optional, you can pass it if you want to use additional inputs in the prompt
# check project prompts to use availables input.
```

## Tests

The ScanSheet Agent Library includes a comprehensive test suite to ensure its functionality. The tests are located in the `tests` directory.

### Running Tests

You can run all tests using the provided script:

```bash
python tests/run_tests.py
```

Or run individual test files:

```bash
python -m unittest tests/test_agent.py
python -m unittest tests/test_prompt.py
python -m unittest tests/test_model.py
```

### Test Coverage

The tests cover all major components of the library:
- ScanSheetAgent: Tests for initialization, model response validation, and execution
- PromptBuilder: Tests for template reading and prompt creation
- AIMessageModel: Tests for model validation and serialization