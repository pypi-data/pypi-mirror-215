# free-gpt Library

The `free-gpt` library is a Python client for interacting with the GPT-3.5 language model. It allows you to send messages and receive responses from the GPT-3.5 model using the ChatGPT API.

## Installation

You can install `free-pygpt` using pip:

```
pip install free-pygpt
```

## Usage

To use the `free-pygpt` library, follow these steps:

1. Use the `ClientGPT` class to define your client:
```python
client = ClientGPT()
```

2. Define `client.prompt` for good results in response
```python
client.prompt = "My language is english"
```

3. Use the `send_message` method to interact with the GPT-3.5 model:
```python
response = client.send_message("Hello, how are you?")
print(response)
```

## Example

Here's an example of how you can use the `free-gpt` library:

```python
import free_pygpt

client = free_gpt.ClientGPT()
response = client.send_message("Hello, how are you?")
print(response)
```

This will send the message "Hello, how are you?" to the GPT-3.5 model and print the response.
