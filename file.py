import os     # Provides functions for interacting with the operating system (walking directories, path joins)
import hashlib  # Offers hashing algorithms (e.g., SHA-256)
from typing import Iterator  # For type hinting that a function yields an iterator of strings

def scan_files(root: str = "/") -> Iterator[str]:
    """
    Recursively walk through the directory tree starting at `root`,
    yielding the full path of every file found.
    """
    # os.walk will traverse root, subdirectories, and files
    for dirpath, _, filenames in os.walk(root, onerror=lambda e: None):
        # dirpath: current directory path
        # filenames: list of file names in dirpath
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)  # Build full file path
            # Check again that it's indeed a file (not a symlink, etc.)
            if os.path.isfile(file_path):
                yield file_path  # Yield the file path to the caller

def hash_calculator(file_path: str, algorithm: str = 'sha256', buffer_size: int = 524288) -> str:
    """
    Compute and return the hash digest of the beginning chunk of a file.
    
    Parameters:
    - file_path: Path to the file to hash.
    - algorithm: Name of the hashing algorithm (currently unused except for naming).
    - buffer_size: Number of bytes to read from the file for hashing.
    
    Returns:
    - Hexadecimal digest string of the hash.
    """
    try:
        # Open the file in binary mode for reading
        with open(file_path, 'rb') as file:
            # Read up to buffer_size bytes from the file
            data = file.read(buffer_size)
            # Initialize the desired hash object (currently hardcoded to sha256)
            h = hashlib.sha256()
            # Feed the read data into the hash algorithm
            h.update(data)
            # Return the hex representation of the has"h
            return h.hexdigest()

    except PermissionError:
        # If we don’t have permission to read the file, report it
        print(f"PermissionError: Cannot open file {file_path}")
        # Optionally, you could return None or an empty string here
        return ""

# Main execution: scan all files under given path
for file_path in scan_files(r"C:\Users\apurv\OneDrive\Desktop\study materials"):
    file_hash = hash_calculator(file_path)  # Compute hash for the file
    print(f"{file_path}:{file_hash}")       # Output the result

      








 





