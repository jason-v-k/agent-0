import os

# ===============
# File paths
# ===============
WORK_DIR = os.getcwd()
INPUT_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt_original.txt")
REPO_DIR = os.path.join(WORK_DIR, "wca-codegen-c2j-renovate-preset")
YAML_FILE = os.path.join(REPO_DIR, ".pipeline-config.yaml")


# 'sys_prompt.txt' is the minimal / basic prompt
TEST_FILE_PATH = os.path.join(WORK_DIR, "sys_prompt.txt") 

# ===============
# Github auth.
# ===============
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_PAT = os.environ.get("GITHUB_PAT")


# ==================
# Container Registry
# ==================
ICR_ADDRESS = "de.icr.io"
ICR_USERNAME = "iamapikey"
# docker login -u iamapikey -p FEG8h-D8Z-YS2Wrzc3HMZwBCrIZlB1558kN9PYgQwdyE de.icr.io