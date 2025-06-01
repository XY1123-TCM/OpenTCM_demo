"""
LLM Utility Functions
Note: To use OpenAI API, please export OPENAI_API_KEY in your environment variables in ~/.bashrc or ~/.bash_profile.
"""

import boto3
import json
import sqlite3
import logging
from langchain_openai import ChatOpenAI

# New connection to the SQLite database to store the QA pairs
conn = sqlite3.connect('../db/qa_pairs.db')

# if the table does not exist, create it
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS qa_pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
''')
conn.commit()


def get_bedrock_response(user_message, region_name="us-east-1", model_id="meta.llama3-70b-instruct-v1:0",
                         max_gen_len=2048, temperature=0.5, top_p=0.9):
    """
    Uses an LLM to process the text data from Traditional Chinese Medicine (TCM) and generate a response.

    Parameters:
    user_message (str): The input message to process.
    region_name (str): The AWS region where the Bedrock Runtime client is located. Default is 'us-east-1'.
    model_id (str): The ID of the model to use. Default is 'meta.llama3-70b-instruct-v1:0'.
    max_gen_len (int): The maximum length of the generated response. Default is 512.
    temperature (float): The temperature parameter for the model. Default is 0.5.
    top_p (float): The top_p parameter for the model. Default is 0.9.

    Returns:
    str: The generated response text from the model.
    """
    # Create a Bedrock Runtime client in the specified AWS Region.
    client = boto3.client("bedrock-runtime", region_name=region_name)

    # Embed the message in Llama 3's prompt format.
    prompt = f"""
<|begin_of_text|>
<|start_header_id|>user<|end_header_id|>
{user_message}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

    # Format the request payload using the model's native structure.
    request = {
        "prompt": prompt,
        "max_gen_len": max_gen_len,
        "temperature": temperature,
        "top_p": top_p,
    }

    # Encode and send the request.
    response = client.invoke_model(body=json.dumps(request), modelId=model_id)

    # Decode the native response body.
    model_response = json.loads(response["body"].read())

    # Extract and return the generated text.
    response_text = model_response["generation"]

    # Save the QA pair to the SQLite database
    cursor.execute('''
    INSERT INTO qa_pairs (question, answer) VALUES (?, ?)
    ''', (user_message, response_text))
    conn.commit()

    return response_text


def get_chatgpt_response(user_message, model_name="gpt-3.5-turbo", response_raw=False, max_tokens=4096):
    """
    Uses an OpenAI ChatGPT model to process the text data from Traditional Chinese Medicine (TCM) and generate a response.

    Parameters:
    user_message (str): The input message to process.

    Returns:
    str: The generated response text from the model.
    """
    # Initialize the OpenAI ChatGPT model
    llm = ChatOpenAI(temperature=0, model=model_name, max_tokens=max_tokens)

    if response_raw:
        # Generate the raw response using the ChatGPT model
        response_text = llm.invoke(user_message)
        return response_text
    else:
        # Generate a response using the ChatGPT model
        response_text = llm.invoke(user_message)
        response_text = response_text.content
        return response_text


def llm_post_processor(text):
    """
    Process the generated text from the LLM model.
    :param text:
    :return: JSON object
    """
    # Check if the text contains 2 or more ``` (triple backticks)
    if text.count('```') >= 2:
        # Extract the JSON content between the triple backticks
        start_index = text.find('```')
        end_index = text.rfind('```')
        json_text = text[start_index + 3:end_index].strip()
        return json.loads(json_text)
    # if only one ``` is found, remove it and try to load the JSON content
    elif text.count('```') == 1:
        text = text.replace('```', '')
        text = text.strip()
        return llm_post_processor(text)
    # Check if the text is empty
    if not text:
        logging.warning("The text is empty.")
        return []

    # Check if the text is JSON
    try:
        response_json = json.loads(text)
        return response_json
    except json.JSONDecodeError:
        # Warn the user that the text is not in JSON format
        logging.warning("The text is not in JSON format.")
        return []


if __name__ == '__main__':
    def test_bedrock():
        user_message = "帮我将以下文言文翻译成现代汉语，用中文回复，只回复翻译结果：內經日虛實之要九針最妙者為其各有所宜也。"
        response_text = get_bedrock_response(user_message)
        print(f'Bedrock Response: {response_text}')


    # test_bedrock()


    def test_openai():
        user_message = "test: 帮我将以下文言文翻译成现代汉语，用中文回复，只回复翻译结果：內經日虛實之要九針最妙者為其各有所宜也。"
        response_text = get_chatgpt_response(user_message)
        print(f'OpenAI Response: {response_text}')


    test_openai()
