from dotenv import load_dotenv
from openai import OpenAI
import os

# Parse auth. mechanisms from .env file
load_dotenv()

# Establish client w/ OpenAI schema
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def call_llm(llm_prompt: str) -> str:
    """
    Call the LLM via API, using OpenAI's Schema
    
    :param llm_prompt: The prompt provided to the LLM at inferencing time
    :type llm_prompt: str
    :return: The response from the LLM
    :rtype: str
    """

    response = client.responses.create(
    # Pass in prompt from `main.py` here
    input=llm_prompt,
    model="openai/gpt-oss-20b",
    )
    # print(response.output_text)
    return response.output_text
   
    