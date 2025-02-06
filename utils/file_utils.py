import os
import hashlib
from datetime import datetime
from src.config import OUTPUT_DIR

def generate_folder_name(email_content: str) -> str:
    """Generates a folder name based on the email content."""
    # Use the first 50 characters of the email content for a hash-based folder name
    email_hash = hashlib.md5(email_content.encode('utf-8')).hexdigest()[:10]
    
    # Alternatively, use timestamp for uniqueness
    folder_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{email_hash}"
    
    return folder_name

def write_markdown_file(content: str, filename: str, email_content: str) -> None:
    """Writes content to a markdown file inside a dynamically created folder."""
    # Generate a unique folder name based on the email content
    folder_name = generate_folder_name(email_content)
    
    # Define the path for the new folder
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    
    # Create the folder
    os.makedirs(folder_path, exist_ok=True)
    
    # Write the content to the markdown file inside the newly created folder
    with open(f"{folder_path}/{filename}.md", "w") as f:
        f.write(content)
    
    print(f"Generated response saved in: {folder_path}/{filename}.md")

