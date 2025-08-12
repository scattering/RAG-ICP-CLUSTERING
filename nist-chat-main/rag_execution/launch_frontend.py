import subprocess
import os
import shutil
from dotenv import load_dotenv

# SSL checks
def get_package_location(package_name):
    try:
        # Run pip show command
        output = subprocess.check_output(['pip', 'show', package_name]).decode('utf-8', errors='ignore')

        # Parse the output to extract the location
        for line in output.splitlines():
            if line.startswith('Location:'):
                location = line.split(': ')[1].strip()
                return location

        # If location is not found, return None
        return None

    except subprocess.CalledProcessError:
        # Handle the case when the package is not found
        print(f"Package '{package_name}' not found.")
        return None

def compare_files(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_contents = file1.read()
            file2_contents = file2.read()
            return file1_contents == file2_contents
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

def run_ssl_fix():
    webui_package_name = 'open-webui'
    webui_location = get_package_location(webui_package_name)

    open_webui_dirpath = os.path.join(webui_location, 'open_webui')
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    local_openai_filepath = os.path.join(current_script_dir, 'openai.py')
    local_util_filepath = os.path.join(current_script_dir, 'utils.py')

    # Update openai router

    #router_dirpath = os.path.join(open_webui_dirpath, 'routers')
    #openai_router_filepath = os.path.join(router_dirpath, 'openai.py')
    #if not compare_files(local_openai_filepath, openai_router_filepath):
    #    shutil.copy(local_openai_filepath, openai_router_filepath)
    #    print('Finished updating openai router: {}'.format(openai_router_filepath))
    #else:
    #    print('Skipping updating openai router: {}'.format(openai_router_filepath))

    # Update retrieval util
    retrieval_dirpath = os.path.join(open_webui_dirpath, 'retrieval')
    util_filepath = os.path.join(retrieval_dirpath, 'utils.py')
    if not compare_files(local_util_filepath, util_filepath):
        shutil.copy(local_util_filepath, util_filepath)
        print('Finished updating retrieval util: {}'.format(util_filepath))
    else:
        print('Skipping updating retrieval util: {}'.format(util_filepath))

if __name__ == "__main__":
    import argparse
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Launch the frontend')
    parser.add_argument('--port', type=int, help='Port number to use', default=8080)
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Run SSL fix, should not be needed anymore
    # run_ssl_fix()

    # Define the environment variables
    env = os.environ.copy()

    default_env_vars = {
        "OFFLINE_MODE": "False",
        "WEBUI_AUTH": "False",
        "WEBUI_URL": "http://localhost:8080",
        "ENABLE_OLLAMA_API": "False",
        "ENABLE_OPENAI_API": "True",
        "OPENAI_API_BASE_URL": "https://rchat.nist.gov/api",
        "ENABLE_EVALUATION_ARENA_MODELS": "False",
        "ENABLE_COMMUNITY_SHARING": "False",
        "CONTENT_EXTRACTION_ENGINE": "",
        "PDF_EXTRACT_IMAGES": "False",
    }

    for var, value in default_env_vars.items():
        if var not in env:
            env[var] = value
            print(f"Value not set {var}, using default: {value}")
        else:
            print(f"{var} already exists with value {env[var]}")


    if 'OPENAI_API_KEY' not in env:
        print("Environment OPENAI_API_KEY not found in environment variables. Please set it to your OpenAI API key. You can place it in a '.env' file or in your environment variables. ")
        exit(1)



    try:
        subprocess.run(["open-webui", "serve", "--port", str(args.port)], env=env, check=True)
    except FileNotFoundError:
        print("open-webui is not found. Make sure it's installed and available in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running open-webui: {e}")