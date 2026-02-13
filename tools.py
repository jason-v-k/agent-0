# =========================================================
# House the utility / helper functions here
# Let the LLM reason how to utilize them, where, and when
# =========================================================

import subprocess
from logger import logger
import yaml
import os
import json

from constants import(
    REPO_NAME,
    REPO_DIR
)

def run_cmd(cmd: str, is_sensitive: bool) -> str:
    """
    Run the provided command for the given task. Utilizes Python's 'subprocess' module
    
    :param cmd: Command to be ran / executed
    :type cmd: str
    :param is_sensitive: If 'cmd' arg. contains sensitive info
    :type is_sensitive: bool
    :return: Resulting stdout / sterr from the given cmd
    :rtype: str
    """

    execute = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True,
        # Due to process substitution used in 'ibmcloud cr...' cmd 
        executable="/bin/bash"
    )

    if is_sensitive:
        logger.info(execute.stdout.strip())
        return execute.stdout.strip()
    else:
        logger.info(f"Executing cmd: {cmd}...")
        logger.info(execute.stdout.strip())
        return execute.stdout.strip()

def clone_repo(github_username: str, github_pat: str) -> str:
    """
    Clone the required remote GitHub repository
    
    :param github_username: Username for GitHub v3 API auth.
    :param github_username: str
    :param github_pat: Token for GitHub v3 API auth.
    :type github_pat: str
    """

    # Format for auth embedding: 
    # git clone https://<username>:<token>@://github.com<owner>/<repo>.git
    clone_cmd = f"git clone https://{github_username}:{github_pat}@github.ibm.com/code-assistant/wca-codegen-c2j-renovate-preset.git"
    
    logger.info("=== Attempting clone operation ===")

    clone_operation = run_cmd(clone_cmd, False)

    if os.path.exists(REPO_DIR):
        logger.info(f"Successful clone operation...Confirmed that '{REPO_NAME}' exists!")
        return clone_operation
    else:
        raise RuntimeError(f"Clone failed for {REPO_NAME}")
        

def read_file(file_path: str) -> str:
    """
    Read the current (local) '.pipeline-config.yaml' file and determine the image currently used via simple YAML parsing.
    
    :param file_path: File path to local file in cloned repository
    :type file_input: str
    :return: Image being employed in the current repo
    :rtype: str
    """
    
    try: 
        with open(file_path, 'r') as file:

            logger.info("=== Attempting YAML file assessment ===")
            logger.info(f"File Path: {file_path}")

            # Convert YAML to Dict{} and drill down to 'build-artifact' -> 'image'
            data = yaml.safe_load(file)
            current_image = data["build-artifact"]["image"]

            if current_image:
                logger.info("Full image and tag/digest found!")
                logger.info(f"Image being used: {current_image}")
            else:
                logger.error("Unable to parse 'image' attribute from 'build-artifact' stage of config YAML file")
                return current_image
            
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        

def icr_auth(icr_username: str, icr_api_key: str) -> str:
    # Handle ICR auth. and ICR query here...
    # ibmcloud cr image-list --no-trunc --restrict wca4z-dev/wca-codegen-c2j-build-base-docker | grep -F -f <(ibmcloud cr image-list --restrict wca4z-dev/wca-codegen-c2j-build-base-docker | awk '/latest/ {print $3}')
    logger.info("=== Proceeding with IRC authentication ===")
    icr_login = f"docker login -u {icr_username} -p {icr_api_key} de.icr.io"
    auth = run_cmd(icr_login, True)
    return auth
    # docker login -u iamapikey -p {API_KEY} de.icr.io


def icr_query() -> str:
    # def run_cmd(cmd: str) -> str:
    logger.info("=== Attempting query of ICR ===")
    cmd = "ibmcloud cr image-list --no-trunc --restrict wca4z-dev/wca-codegen-c2j-build-base-docker --output json | grep -F -f <(ibmcloud cr image-list --restrict wca4z-dev/wca-codegen-c2j-build-base-docker | awk '/latest/ {print $3}')"
    
    # ================================================================================
    # clone_cmd = f"git clone https://{github_username}:{github_pat}@github.ibm.com/code-assistant/wca-codegen-c2j-renovate-preset.git"
    # clone_operation = run_cmd(clone_cmd)
    # return clone_operation
    # cmd = "ls -l"
    # ================================================================================
    query = run_cmd(cmd, False)
    return query

def write_file(file_path: str, contents: str) -> None:
    """
    Make changes to the current '.pipeline-config.yaml' file (locally) if necessary

    :param file_path: File path to local file
    :type file_path: str
    :param content: Changes to be made
    :type content: str
    """

def create_branch(github_pat: str) -> None:
    """
    Create a working / feature branch to stage file commits for a subsequent PR
    
    :param github_pat: Token for GitHub v3 API auth.
    :type github_pat: str
    """
    pass
    

def create_pr(github_pat: str, branch_name: str, pr_title: str) -> None:
    """
    Create Pull Request in appropriate repo via GitHub's v3 API
    
    :param github_pat: Token for GitHub v3 API auth.
    :type github_pat: str
    :param branch_name: Feature branch name
    :type branch_name: str
    :param pr_title: Title of PR being submitted
    :type pr_title: str
    """
    pass

