import base64
import requests
import hashlib
import os

import pandas as pd


## File Handling

# def encode_sharing_url(sharing_url):
#     # Base64 encode the sharing URL directly (without URL-encoding it first)
#     base64_encoded_url = base64.b64encode(sharing_url.encode()).decode()
#     # Make the base64 result URL-safe
#     base64_url_safe = base64_encoded_url.replace('/', '_').replace('+', '-').rstrip('=')
#     # Prefix with "u!" to form a valid shareId for Microsoft Graph API
#     share_id = "u!" + base64_url_safe
    
#     return share_id

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


def read_auth_code_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the refresh token from the file
            refresh_token = file.read().strip()  # .strip() removes any leading/trailing whitespace
        return refresh_token
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def download_file(file_url, file_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        # print(f"Downloaded {file_path}")
    else:
        print(f"Failed to download {file_path}")


def create_directory_if_not_exists(directory):
    """
    Create a directory if it doesn't exist.

    Args:
    - directory: The path to the directory to be created.

    Returns:
    - True if the directory was created or already exists, False otherwise.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        # print(f"Directory '{directory}' created.")
        return True
    else:
        # print(f"Directory '{directory}' already exists.")
        return False
    

def update_env_file(var_name, var_value):
    # This function updates or adds a variable to the .env file
    with open('.env', 'r') as file:
        lines = file.readlines()

    with open('.env', 'w') as file:
        var_found = False
        for line in lines:
            if line.startswith(var_name + '='):
                file.write(f"{var_name}={var_value}\n")
                var_found = True
            else:
                file.write(line)
        if not var_found:
            file.write(f"\n{var_name}={var_value}\n")


def generate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def extract_parent_name(path):
    # Split the path by "/" and filter out any empty strings
    parts = [part for part in path.split('/') if part]
    
    # Check if there are enough parts to extract the parent name
    if len(parts) >= 3:
        parent_name = parts[2]  # Take the second value as the parent name
    else:
        parent_name = None  # Default value if the path doesn't have a second part
    
    return parent_name


def remove_null_characters(input_string):
    return input_string.replace('\x00', '')

## RAG and Vetoriziing

def collect_subdirectories_with_files(root_dir):
    """Recursively collect all directories under the given root directory
    that directly contain at least one file with .docx or .pdf extension."""
    directories_with_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter the list of filenames to only include .docx or .pdf files
        filtered_files = [f for f in filenames if f.endswith('.docx') or f.endswith('.pdf')]
        # Add directory if it contains .docx or .pdf files
        if filtered_files:  # This list is non-empty if such files are present
            directories_with_files.append(dirpath)
    return directories_with_files



def excel_sheets_to_csv(excel_files):
    """
    Reads each sheet from each Excel file, writes them to separate CSV files
    in the same directory as the Excel file, and deletes the Excel file after conversion.
    """
    import pandas as pd
    import os
    import os.path

    for file_path in excel_files:
        xls = pd.ExcelFile(file_path)
        directory = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            csv_file_name = f"{file_name_without_ext}_{sheet_name}.csv"
            csv_file_path = os.path.join(directory, csv_file_name)
            df.to_csv(csv_file_path, index=False)
            print(f"Sheet {sheet_name} from {file_path} written to {csv_file_path}")

        # Delete the Excel file after conversion
        os.remove(file_path)
        print(f"Deleted Excel file: {file_path}")
