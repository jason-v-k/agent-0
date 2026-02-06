# ICR Image Update Agent

## Overview
This AI agent is intended as a personal / pet project to emulate Renovate Bot. It will help me automate my workflow that I would use if Renovate bot was NOT wired up to my repository. It will leverage GROQ's free API initially, but that is subject to change.  

The overall flow is:
  - Read the `.pipeline-config.yaml` file and analyze the container image currently being used
  - Query ICR to see if there are any updated images available
    - If not, do nothing.
    - If so, determine what that image is, including the image tag AND the full SHA digest.
  - If a new image is available, run the appropriate CLI command to run a Vulnerability Assessment on that container image
  - If the VA scan is not clean, alert me (via some mechanism I haven't worked out / decided yet) about what the CVE(s) is, and the associated severity.
  - If the VA scan is clean, submit a PR to the appropriate repo to update the image in the `.pipeline-config.yaml` file

## Approach
The overall layout of the project is as follows:

| Module | Purpose |               
|:-------:|:--------------:
| `llm.py` | Establish the LLM client and Schema, and define a simple method to make the LLM callable for modularity and testability | 
| `tools.py` | Contains all helper / utility methods at the agent's disposal, such as executing a given command, or submitting a PR |
| `main.py` | Main entrypoint of all other source code | 
