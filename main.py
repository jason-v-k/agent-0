#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from llm import call_llm
from tools import run_cmd, clone_repo, read_file
from constants import(
    TEST_FILE_PATH,
    GITHUB_PAT,
    GITHUB_USERNAME,
    YAML_FILE
)

load_dotenv()


def main(): 

    # Read TXT file for LLM input
    try:
        with open(TEST_FILE_PATH, 'r') as file:
            prompt = file.read()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        exit()

    llm_response = call_llm(prompt)
    print(llm_response)

if __name__ == "__main__":
    clone_repo(GITHUB_USERNAME, GITHUB_PAT)
    read_file(YAML_FILE)

    # main()