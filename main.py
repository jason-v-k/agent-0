#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from llm import call_llm
from tools import clone_repo, read_file, icr_query
from constants import(
    TEST_FILE_PATH,
    GITHUB_PAT,
    GITHUB_USERNAME,
    YAML_FILE,
    ICR_API_KEY,
    ICR_ACCT_ID
)
from logger import logger

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
    current_image = read_file(YAML_FILE)
    latest_image = str(icr_query(ICR_API_KEY, ICR_ACCT_ID))
    
    logger.info(f"The image being used by the pipeline currently is: {current_image}")
    logger.info(f"The latest 'wca-codegen-c2j-build-cpd-docker' image in ICR is: {latest_image}")

    if current_image != latest_image:
        logger.info("Image used by pipeline is NOT the latest. Summary:")
        logger.info(f"Image in '.pipeline-config.yaml' file: \n\n{current_image}")
        logger.info(f"Latest 'wca-codegen-c2j-build-cpd-docker' image in ICR: \n\n{latest_image}")

    else:
        logger.info("Image hashes are currently equal. Nothing to do as of now!")

    # main()