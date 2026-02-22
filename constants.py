import os

# ===============
# File paths
# ===============
WORK_DIR = os.getcwd()
INPUT_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt_original.txt")
REPO_DIR = os.path.join(WORK_DIR, "wca-codegen-c2j-renovate-preset")
REPO_NAME = "wca-codegen-c2j-renovate-preset"
YAML_FILE = os.path.join(REPO_DIR, ".pipeline-config.yaml")


# 'sys_prompt.txt' is the minimal / basic prompt
TEST_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt.txt") 

# ===============
# Github auth.
# ===============
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_PAT = os.environ.get("GITHUB_PAT")


# =========================
# Container Registry / ICR
# =========================
ICR_ENDPOINT= "https://de.icr.io"
ICR_USERNAME = "iamapikey"
ICR_API_KEY = os.environ.get("ICR_API_KEY")
ICR_ACCT_ID = os.environ.get("ICR_ACCT_ID")
ICR_REPOSITORY = os.environ.get("ICR_REPOSITORY")

# Sample login:
# docker login -u iamapikey -p {AUTH_KEY} de.icr.io