from fastapi import FastAPI
from fastmcp import FastMCP
import os
import re

mcp = FastMCP(name="removecredits")

def is_attribution_line(line: str) -> bool:
    line = line.strip()

    # Check for known prefixes
    attribution_prefixes = ("source:", "attribution:", "credit:", "references:")
    if any(line.lower().startswith(prefix) for prefix in attribution_prefixes):
        return True

    # Match initials + last name (e.g., A. B. Smith, J. Doe, M.T. Johnson)
    if re.match(r"^([A-Z]\.? ?){1,3}[A-Z][a-z]+$", line):
        return True

    # Match numbered references (e.g., 1. Some reference)
    if re.match(r"^\d+\.\s+.+", line):
        return True

    return False

def remove_attributions(text: str) -> str:
    # Normalize whitespace to make "References" easier to find
    normalized_text = re.sub(r'\s+', ' ', text)

    # Look for 'References' (case insensitive), followed by anything
    match = re.search(r'\bReferences\b', normalized_text, re.IGNORECASE)
    if match:
        # Cut everything starting from "References"
        cut_index = text.lower().find('references')
        return text[:cut_index].strip()

    return text.strip()

@mcp.tool()
async def clean_text_files_in_folder(folder_path: str) -> str:
    """
    Cleans attributions from the end of all .txt files in the given folder.
    Creates a new folder with '_clean' appended to the name.
    Returns the path to the new folder.
    """
    if not os.path.isdir(folder_path):
        return f"Error: The folder '{folder_path}' does not exist."

    parent_dir, folder_name = os.path.split(folder_path.rstrip("/\\"))
    clean_folder_name = folder_name + "_clean"
    clean_folder_path = os.path.join(parent_dir, clean_folder_name)
    os.makedirs(clean_folder_path, exist_ok=True)

    cleaned_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            cleaned_content = remove_attributions(content)

            new_file_path = os.path.join(clean_folder_path, filename)
            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_content)

            cleaned_files.append(filename)

    return f"Cleaned {len(cleaned_files)} files. Saved to: {clean_folder_path}"

if __name__ == "__main__":
    mcp.run()
