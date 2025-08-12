# NIST Chat

This document explains usage of the NIST chat service, accessible at https://rchat.nist.gov. 

## Basic usage from WebUI

1. Login using a browser to https://rchat.nist.gov. On first login you will be prompted with a disclaimer.
2. Connect using okta authentication.
3. Chat
4. More information about chat and prompt engineering found here: TBD

### WebUI Capabilities
1. Interactive chat, that retains context from previous conversations.
2. Ability to organize your chat history and share chats with others, among other uses.
3. Uploading a PDF and querying about content within the PDF
4. Uploading an image and querying about content in the image (vision model only) 
5. (advanced) Modifying controls for the AI generation options using 
6. ...

### Example interactions

## Basic usage from API

### Setup environment:
0. (OPTIONAL) Setup ssh public/private keys if using "git@gitlab.nist.gov" version in next step: https://docs.gitlab.com/user/ssh/#generate-an-ssh-key-pair 
0. (OPTIONAL) Setup personal access token here: https://gitlab.nist.gov/gitlab/-/user_settings/personal_access_tokens
1. Get the repo:
    * Download zip: https://gitlab.nist.gov/gitlab/isg-ai/nist-chat/-/archive/main/nist-chat-main.zip OR 
    * `git clone https://oauth2:<personal access token>@gitlab.nist.gov/gitlab/isg-ai/nist-chat.git` OR 
    * `git clone git@gitlab.nist.gov:isg-ai/nist-chat.git`
2. `cd nist-chat`
3. Download and install [miniforge](https://github.com/conda-forge/miniforge)
    * If in Windows launch `Miniforge prompt` (Also may require Edge to download installer)
4. `conda create --name nist-rchat python=3.12`
5. `conda activate nist-rchat`
6. `pip install -r requirements.txt`
7. Modify Example 
    * [example python file for text queries](https://gitlab.nist.gov/gitlab/isg-ai/nist-chat/-/blob/main/example_text.py)
    * [example python file for image queries](https://gitlab.nist.gov/gitlab/isg-ai/nist-chat/-/blob/main/example_image.py)

### Updating example script
1. Generate API key in WebUI (Top Right-> Settings -> Account -> Show API Keys -> Generate API Key)
2. Specify model, identified based on name of model or via RESTful query here: https://rchat.nist.gov/api/models
3. Update api_key or set environment variable "RCHAT_API_KEY"
    * `export RCHAT_API_KEY=your_api_key_here` (Linux/Mac OS)
    * `set RCHAT_API_KEY=your_api_key_here` (Windows 11 Command Prompt or PowerShell)
4. Run `python example.py`

