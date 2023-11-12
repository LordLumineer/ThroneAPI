import base64
import re
import requests
import semantic_version
import re
import pytest

from ThroneAPI import get_api_version

def get_api_version_from_file(file_content):
    # Using regular expression to find the API_VERSION value
    match = re.search(r'API_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', file_content)
    if match:
        return match.group(1)
    else:
        raise ValueError("API_VERSION not found in the FastAPI.py file")

def get_api_version_from_main_branch():
    # GitHub repository information
    owner = "LordLumineer"
    repo = "testtest"
    branch = "main"

    # GitHub API endpoint to get the content of FastAPI.py from the main branch
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/ThroneAPI.py?ref={branch}"

    # Make a GET request to the GitHub API
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the content of the file and extract the version
        content = response.json().get('content', '')
        decoded_content = base64.b64decode(content).decode('utf-8')
        return get_api_version_from_file(decoded_content)
    else:
        # Handle the case where the request to GitHub fails
        raise Exception(f"Failed to fetch file from GitHub. Status code: {response.status_code}")

def compare_versions(current_version, previous_version):
    current = semantic_version.Version(current_version)
    previous = semantic_version.Version(previous_version)
    
    return current > previous

@pytest.mark.run(order=1)
def test_version_comparison():
    current_version = get_api_version()
    previous_version = get_api_version_from_main_branch()
    
    assert compare_versions(current_version, previous_version), f"Current version {current_version} is not superior to {previous_version}"