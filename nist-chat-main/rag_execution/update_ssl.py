import os
import subprocess
import shutil

def get_package_location(package_name):
    try:
        # Run pip show command
        output = subprocess.check_output(['pip', 'show', package_name]).decode('utf-8')

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

if __name__ == '__main__':
    webui_package_name = 'open-webui'
    webui_location = get_package_location(webui_package_name)

    open_webui_dirpath = os.path.join(webui_location, 'open_webui')
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    local_openai_filepath = os.path.join(current_script_dir, 'openai.py')
    local_util_filepath = os.path.join(current_script_dir, 'utils.py')

    # Update openai router
    router_dirpath = os.path.join(open_webui_dirpath, 'routers')
    openai_router_filepath = os.path.join(router_dirpath, 'openai.py')
    shutil.copy(local_openai_filepath, openai_router_filepath)
    print('Finished updating openai router: {}'.format(openai_router_filepath))


    # Update retrieval util
    retrieval_dirpath = os.path.join(open_webui_dirpath, 'retrieval')
    util_filepath = os.path.join(retrieval_dirpath, 'utils.py')
    shutil.copy(local_util_filepath, util_filepath)
    print('Finished updating retrieval util: {}'.format(util_filepath))

    print('Finished updating router and utils for SSL fix.')
