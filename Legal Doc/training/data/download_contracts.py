import requests
import zipfile
from pathlib import Path
import shutil
import os

# Replace this with a real URL for Indian legal datasets
INDIAN_LEGAL_URL = "https://archive.org/download/IndianLegalDocuments/IndianLegalDocuments.zip"

def download_data():
    raw_data_dir = Path("training/data/raw_contracts")
    extracted_data_dir = Path("training/data/extracted_contracts")

    # Ensure directories exist
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    zip_file_path = raw_data_dir / "sample.zip"

    # Download dataset
    response = requests.get(INDIAN_LEGAL_URL, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Downloaded dataset to {zip_file_path}")
    else:
        raise Exception(f"Failed to download data, status code: {response.status_code}")

    # Extract files
    if extracted_data_dir.exists():
        shutil.rmtree(extracted_data_dir)  # Clean old data
    extracted_data_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_data_dir)
        print(f"Extracted dataset to {extracted_data_dir}")

    # Optionally, list files
    print(f"Extracted files: {os.listdir(extracted_data_dir)}")

if __name__ == "__main__":
    download_data()
