import base64
import os
import requests


def refresh_access_token(client_id, client_secret, refresh_token, tenant_id):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        response_data = response.json()
        new_access_token = response_data.get('access_token')
        # Refresh token can also be updated in this step, as new one may be returned
        new_refresh_token = response_data.get('refresh_token', refresh_token)  # Fallback to old if not provided
        return new_access_token, new_refresh_token
    else:
        raise Exception(f"Failed to refresh access token: {response.text}")


def encode_sharing_url(shared_folder_url):
    # Remove 'https://' from the URL
    stripped_url = shared_folder_url.replace('https://', '')
    # Base64 encode the stripped URL
    base64_encoded_url = base64.b64encode(stripped_url.encode()).decode('utf-8')
    # Convert to base64url format
    base64url_encoded_url = base64_encoded_url.replace('/', '_').replace('+', '-').rstrip('=')
    # Prepend 'u!' to the encoded URL
    encoded_url = f"u!{base64url_encoded_url}"
    return encoded_url



def list_files_in_shared_folder(access_token, encoded_sharing_url):
    url = f"https://graph.microsoft.com/v1.0/shares/{encoded_sharing_url}/driveItem/children"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['value']
    else:
        print(f"Failed to list files: {response.json()}")
        return []


def download_file(access_token, download_url, local_path):
    response = requests.get(download_url, headers={"Authorization": f"Bearer {access_token}"}, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def download_files_and_folders(access_token, items, local_download_path, required_exts):
    for item in items:
        # Construct the local path for the item
        local_item_path = os.path.join(local_download_path, item['name'])

        if 'folder' in item:
            # Create the directory if it doesn't exist
            if not os.path.exists(local_item_path):
                os.makedirs(local_item_path)
            # List contents of the folder
            folder_contents = list_files_in_shared_folder(access_token, encode_sharing_url(item['@microsoft.graph.downloadUrl']))
            # Recursively download contents
            download_files_and_folders(access_token, folder_contents, local_item_path, required_exts)
        elif any(item['name'].lower().endswith(ext) for ext in required_exts):
            # Download the file
            print(f"Downloading {item['name']} to {local_item_path}")
            download_file(access_token, item['@microsoft.graph.downloadUrl'], local_item_path)


SHARED_FOLDER_URL = "https://farpointhq-my.sharepoint.com/:f:/p/tyler/En-z8LCIgc5KkJqxOWJrshcBhCQkR9psOMlhFEScr4A2lQ"

access_token, new_refresh_token = refresh_access_token(client_id, client_secret, refresh_token, tenant_id)

# Update the refresh token environment variable if a new refresh token was obtained
if new_refresh_token != refresh_token:
    os.environ['REFRESH_TOKEN'] = refresh_token
    U.update_env_file('REFRESH_TOKEN', refresh_token)

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
LOCAL_DOWNLOAD_PATH = "/path/to/download"
REQUIRED_EXTS = ['.pdf', '.docx']  # Add more extensions as needed

encoded_url = encode_sharing_url(SHARED_FOLDER_URL)
shared_items = list_files_in_shared_folder(ACCESS_TOKEN, encoded_url)
download_files_and_folders(ACCESS_TOKEN, shared_items, LOCAL_DOWNLOAD_PATH, REQUIRED_EXTS)
