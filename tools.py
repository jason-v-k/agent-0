# =========================================================
# House the utility / helper functions here
# Let the LLM reason how to utilize them, where, and when
# =========================================================

import subprocess
from logger import logger

def run_cmd(cmd: str) -> str:
    """
    Run the provided command for the given task. Utilizes Python's 'subprocess' module
    
    :param cmd: Command to be ran / executed
    :type cmd: str
    :return: Resulting stdout / sterr from the given cmd
    :rtype: str
    """

    execute = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True
    )

    logger.info(f"Executing cmd: {cmd}...")
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
    
    logger.info("=== Attempting clone operation now ===")

    clone_operation = run_cmd(clone_cmd)

    return clone_operation


def create_branch(github_pat: str) -> None:
    """
    Create a working / feature branch to stage file commits for a subsequent PR
    
    :param github_pat: Token for GitHub v3 API auth.
    :type github_pat: str
    """
    pass


def read_file(file_path: str) -> None:
    """
    Read the current (local) '.pipeline-config.yaml' file and determine the image currently used via simple YAML parsing.
    
    :param file_path: File path to local file
    :type file_input: str
    """
    pass


def write_file(file_path: str, contents: str) -> None:
    """
    Make changes to the current '.pipeline-config.yaml' file (locally) if necessary

    :param file_path: File path to local file
    :type file_path: str
    :param content: Changes to be made
    :type content: str
    """
    

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

