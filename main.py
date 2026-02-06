#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from llm import call_llm
from tools import run_cmd

WORK_DIR = os.getcwd()
# 'sys_prompt.txt' is the minimal / basic prompt
TEST_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt.txt")
INPUT_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt_original.txt")

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
    main()