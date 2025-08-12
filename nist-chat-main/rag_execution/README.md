

# Setting up your personal RAG Python Execution
1. Clone nist-chat repo somewhere to get the launch_frontend.py codebase
2. Download and install [Linux/Mac-miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#unix-like-platforms-macos-linux--wsl), [Windows-miniforge](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe) (This may require you to use the Edge or another browser besides Chrome if you are getting errors in Chrome)
3. Launch terminal with miniforge environment, Windows: Launch "Miniforge prompt" from start menu
4. Run `conda create --name webui python=3.11`
5. Run `conda activate webui`
6. Run `pip install --upgrade pip`
7. Run `pip install uv`
8. Run `uv pip install ffmpeg`
9. Run `uv pip install open-webui`
10. Create `.env` file (see `.env_example`) and copy/paste your API key from https://rchat.nist.gov into OPENAI_API_KEY
11. Run `python launch_frontend.py` (optional parameter, --port, default=8080)
12. Connect using browser to http://localhost:8080


## About this setup
By running `launch_frontend.py`, we streamline getting connected to rchat and a high quality embedding model (`e5-mistral-7b-instruct`). Once the front-end is running on localhost, all files uploaded into your knowledge or prompts is local to you only. Any interaction with rchat will only keep track of how many tokens were input and generated. No chat history will be saved on rchat, only stored in your localhost instance. 

## More information
For details about customizing the RAG, please see TBD presentation or TBD wiki.