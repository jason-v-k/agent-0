#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from llm import call_llm
from tools import clone_repo, read_file, icr_auth, icr_query
from constants import(
    TEST_FILE_PATH,
    GITHUB_PAT,
    GITHUB_USERNAME,
    YAML_FILE,
    ICR_USERNAME,
    ICR_API_KEY,
    ICR_ACCT_ID
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
    icr_auth(ICR_USERNAME, ICR_API_KEY)
    icr_query(ICR_API_KEY, ICR_ACCT_ID)
    # main()