from llama_index.core import SimpleDirectoryReader
from llama_index.core import download_loader
from llama_index.core import Document

import os
import glob
from tqdm import tqdm
import random
from datetime import datetime

from src import config as C
from src import utils as U

### Downloading Loaders:
PyMuPDFReader = download_loader("PyMuPDFReader")
DocxReader = download_loader("DocxReader")
PandasCSVReader = download_loader("PandasCSVReader")
PptxReader = download_loader("PptxReader")


# def custom_directory_data_loader(input_dir, recursive, exclude_hidden, encoding, required_exts, file_extractor):
#     documents = []
    
#     # Function to get file metadata
#     def get_file_metadata(file_path):
#         stat = os.stat(file_path)
#         return {
#             "file_type": os.path.splitext(file_path)[1],
#             "file_name": os.path.basename(file_path),
#             "file_path": file_path,
#             "creation_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
#             "last_modified_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
#             "last_accessed_date": datetime.fromtimestamp(stat.st_atime).isoformat(),
#         }
    
#     # Function to walk through directories and files
#     def process_directory(directory):
#         for root, dirs, files in os.walk(directory):
#             if exclude_hidden:
#                 files = [f for f in files if not f.startswith('.')]
#                 dirs[:] = [d for d in dirs if not d.startswith('.')]
            
#             for file_name in files:
#                 file_path = os.path.join(root, file_name)
#                 file_extension = os.path.splitext(file_name)[1]
                
#                 if file_extension in required_exts:
#                     file_metadata = get_file_metadata(file_path)
#                     reader = file_extractor.get(file_extension)
                    
#                     if reader:
#                         try:
#                             docs = reader.load_data(file_path)
#                             for doc in docs:
#                                 document = Document(text=doc.text, metadata=file_metadata)
#                                 documents.append(document)
#                         except Exception as e:
#                             print(f"Error processing {file_path}: {e}")
            
#             if not recursive:
#                 break
    
#     # Start processing from the input directory
#     process_directory(input_dir)
    
#     return documents


def read_documents_from_directories(folder_path):
    """
    Convert Excel files to CSV, delete the original Excel files,
    and then read and aggregate documents from a list of directories.
    """
    documents_with_metadata = []

    # Construct the pattern to match all .xlsx files recursively
    pattern = os.path.join(folder_path, '**', '*.xlsx')        
    # Use glob.glob with the recursive flag set to True
    xlsx_files = glob.glob(pattern, recursive=True)
    
    # Convert Excel files to CSV and delete the originals
    U.excel_sheets_to_csv(xlsx_files)

    # Now, proceed with reading documents including the newly created CSV files
    dir_reader = SimpleDirectoryReader(input_dir = folder_path,
                                       recursive = True,
                                       exclude_hidden = True,
                                       encoding = 'utf-8',
                                       required_exts = C.REQ_EXTENSIONS,
                                       file_extractor = {
                                            ".docx": DocxReader(),
                                            ".pptx": PptxReader(),
                                            ".csv": PandasCSVReader(),
                                            ".pdf": PyMuPDFReader()
                                            }
                                    )
    documents = dir_reader.load_data()

    # file_extractor = {
    #     ".docx": DocxReader(),
    #     ".pptx": PptxReader(),
    #     ".csv": PandasCSVReader(),
    #     ".pdf": PyMuPDFReader()
    #     }
    
    # documents = custom_directory_data_loader(
    #     input_dir=folder_path,
    #     recursive=True,
    #     exclude_hidden=True,
    #     encoding='utf-8',
    #     required_exts=C.REQ_EXTENSIONS,
    #     file_extractor=file_extractor
    # )

    for doc in documents:
        # Extracting client_name and category from the file path
        path_parts = doc.metadata['file_path'].split('/')
        client_name = path_parts[1] if len(path_parts) > 1 else "Unknown"
        folder = path_parts[2] if len(path_parts) > 2 else "General"
        
        # Generate a list of random user IDs
        read_users = random.sample(range(1, 6), k=random.randint(1, 5))  # Generates a list of unique random user IDs

        # Updating document metadata with new fields
        doc.metadata.update({
            "client_name": client_name,
            "file_type": doc.metadata['file_type'],
            "read_users": read_users,
            "folder": folder,
            "file_name": doc.metadata['file_name'],
            "file_path": doc.metadata['file_path'],
            "creation_date": doc.metadata['creation_date'],
            "last_modified_date": doc.metadata['last_modified_date'],
            "last_accessed_date": doc.metadata['last_accessed_date'],
        })

        # Update metadata, text templates, and separator as per requirements
        doc.metadata_seperator = '\n'
        doc.metadata_template = "{key}=>{value}"
        doc.text_template = "Metadata:\n{metadata_str}\n-----\nContent: {content}"

        doc.excluded_llm_metadata_keys = ["read_users", "file_path", "creation_date", "last_accessed_date"]
        doc.excluded_embed_metadata_keys = ["file_name", "file_type", "read_users", "file_path", "creation_date", "last_modified_date", "last_accessed_date"]

        documents_with_metadata.append(doc)

    return documents_with_metadata
