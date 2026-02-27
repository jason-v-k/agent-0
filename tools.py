# =========================================================
# House the utility / helper functions here
# Let the LLM reason how to utilize them, where, and when
# =========================================================

import subprocess
from logger import logger
import yaml
import os
import json
import requests

from constants import(
    REPO_NAME,
    REPO_DIR,
    ICR_ENDPOINT,
    ICR_REPOSITORY
)

def run_cmd(cmd: str, is_sensitive: bool) -> str:
    """
    Run the provided command for the given task. Utilizes Python's 'subprocess' module.\n
    Provides stdout only if no sensitive info is returned.

    Args:
        cmd: Command to be ran / executed
        is_sensitive: If 'cmd' arg. contains sensitive info
    Returns:
        str: stdout resulting from the executed command (provided NO sensitive info is returned.)
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

    Args:
        github_username: User name for GitHub v3 API auth.
        github_pat: Token for GitHub v3 API auth.
    
    Returns:
        str: stdout resulting from clone operation
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
    
    Args:
        file_path: Path to the local '.pipeline-config.yaml' file
    
    Returns:
        str: The image currently being used by the CI Pipeline\n
    """
    seperator = "@"

    try: 
        with open(file_path, 'r') as file:

            logger.info("=== Attempting YAML file assessment ===")
            logger.info(f"File Path: {file_path}")

            # Convert YAML to Dict{} and drill down to 'build-artifact' -> 'image'
            data = yaml.safe_load(file)
            current_image = data["build-artifact"]["image"]
            print(current_image)
            if current_image:
                logger.info("Full image and tag/digest found!")
                logger.info(f"Image being used: {current_image}")
                # Only parse what's after the "@" to compare Hashes
                # Returns a 3-tuple. Discard the "before" and "middle"
                _, _, image_sha = current_image.partition(seperator)
                if image_sha:
                    logger.info("Successfully parsed CI Pipeline YAML!")
                    logger.info(f"Current Image SHA is: '{image_sha}'")
                    return image_sha
                else:
                    logger.debug("Failed to parse config YAML file.")
            else:
                logger.error("Unable to parse 'image' attribute from 'build-artifact' stage of config YAML file")
                
            
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        

def icr_auth(icr_username: str, icr_api_key: str) -> str:
    """
    Authenticate to IBM Container Registry

    Args:
        icr_username: User name for ICR Auth.
        icr_apikey: API key required for ICR Auth.
    
    Returns:
        str: stdout from the underlying 'docker login...' command
    """
    
    logger.info("=== Proceeding with IRC authentication ===")
    # docker login -u iamapikey -p {API_KEY} de.icr.io
    icr_login = f"docker login -u {icr_username} -p {icr_api_key} de.icr.io"
    auth = run_cmd(icr_login, True)
    return auth


def get_bearer_token(api_key: str) -> str:
    """
    Get Bearer Token from a valid IBM Cloud API Key

    Args:
        api_key: A valid IBM Cloud API Key 
        
    Returns:
        str: A current Bearer Token for authenticating to IBM Cloud
        
    Raises:
        requests.RequestException: If the API request fails or response is invalid
    """

    token_url = 'https://iam.cloud.ibm.com/identity/token'
    token_headers = {'cache-control': 'nocache',
                 'content-type': 'application/x-www-form-urlencoded'}

    payload = {
        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
        'response_type': 'cloud_iam',
        'apikey': api_key
    }

    try:
        response = requests.post(
            token_url,
            data = payload,
            headers = token_headers
        )

        # Handle non-2xx HTTP responses
        response.raise_for_status()

        # Parse `access_token` attribute from API response
        token = response.json().get('access_token')
        if token:
            return token
        else:
            # No token = unable to proceed, so throw an Exception and terminate.
            logger.error("[X] - No access token found in API response")
            debug_log = json.dumps(response.json(), indent=4)
            logger.debug("Full API response for gathering bearer token: %s", debug_log)
            raise RuntimeError("Unable to retrieve bearer token from Cloud API Key!")

    # No token = unable to proceed, so throw an Exception and terminate.
    except requests.RequestException as e:
        logger.error("[X] - Failed to get Bearer Token from Cloud API Key: %s", e)
        raise RuntimeError("Unable to retrieve bearer token from Cloud API Key!")


def icr_query(api_key: str, acct_id: str) -> str:
    """
    Query IBM Container Registry (includes auth.) to determine the latest/greatest 'wca-codegen-c2j-build-base-docker' image.\n
    

    Args:
        api_key: IBM IAM API Key required for ICR auth.
        acct_id: Unique ID for the IBM Cloud Account in question

    Returns:
        str: The 'sha256' Hash of the latest/greatest 'wca-codegen-c2j-build-base-docker' image 
    
    """
    target_tag = "latest"
    # def run_cmd(cmd: str) -> str:
    logger.info("=== Attempting query of ICR ===")

    # Leverage ICR API to query rather than parsing stdout / CLI content
    # Image: de.icr.io/wca4z-dev/wca-codegen-c2j-build-base-docker
    token = get_bearer_token(api_key)
    logger.info("Attempting to generate bearer token!")
    logger.info(f"Going to use key starting with... {api_key[:5]}")
    # logger.info(f"TOKEN: {token[:50]}")
    # logger.info(f"Token generated:\n{token}")

    # url = f"{ICR_ENDPOINT}/api/v1/images?includeIBM=false&includePrivate=true&includeManifestLists=true&vulnerabilities=true"
    base_url = f"{ICR_ENDPOINT}/api/v1/images"

    query_params = {
    "includeIBM": "false",
    "includePrivate": "true",
    "includeManifestLists": "true",
    "vulnerabilities": "false",
    "namespace": "wca4z-dev",
    "repository": ICR_REPOSITORY
    }   


    logger.info(f"Firing off HTTP request to {base_url} now...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Account": acct_id,
    }

    response = requests.get(
        base_url,
        headers=headers,
        params=query_params
    )

    # API returns a list of image objects, NOT a single dict!
    data = response.json()
    
    # image["RepoTags"] => # <class 'list'>
    # ":latest" image will have 2 entries in "RepoTags" attribute
    for image in data:
        if len(image["RepoTags"]) > 1:
            for i in image["RepoTags"]:
                if i.endswith(":latest"):
                    logger.info(f"Found the following image in ICR with the 'latest' tag: {image["RepoDigests"]}")
                    return image["Id"]
                    
def write_file(file_path: str, contents: str) -> None:
    """
    Make changes to the current '.pipeline-config.yaml' file (locally) if necessary
    """

def create_branch(github_pat: str) -> None:
    """
    Create a working / feature branch to stage file commits for a subsequent PR
    """
    pass
    

def create_pr(github_pat: str, branch_name: str, pr_title: str) -> None:
    """
    Create Pull Request in appropriate repo via GitHub's v3 API
    """
    pass

