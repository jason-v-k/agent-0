# =========================================================
# House the utility functions here
# Let the LLM reason how to utilize them, where, and when
# =========================================================

import subprocess

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

    return execute.stdout.strip()
 
    
#     # Syntax: node main.js <github_access_token> <github_orgName> <artifactory_token> [<github_repoName>]
# encryption_script = subprocess.run(
#     [
#         "node",
#         SCRIPT_PATH,
#         ghe_token,
#         ORG_NAME,
#         secret_value,
#     ],

#     capture_output=True, # capture stdout AND stderr
#     text=True, # get output as strings instead of bytes.
#     check=True # raise exception if cmd fails
# )

# # 'main.js' logs encrypted value to stdout (console.log(encryptedMessage))
# encrypted_token = encryption_script.stdout.strip()


def read_file(file_path: str) -> None:
    """
    Read the current '.pipeline-config.yaml' file (locally) and determine the image currently used
    
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

