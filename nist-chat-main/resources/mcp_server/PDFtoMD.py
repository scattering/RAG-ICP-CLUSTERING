import fitz  # PyMuPDF
import os
from fastmcp import FastMCP

# Initialize FastMCP app
mcp = FastMCP(name="PDFtoMD")

@mcp.tool()
async def pdf_to_markdown(input_folder: str, output_folder: str):
    """
    Converts all PDFs in input_folder to Markdown files saved in output_folder.

    Args:
        input_folder (str): Path to folder containing PDFs.
        output_folder (str): Path to folder where Markdown files will be saved.

    Returns:
        str: Summary message of the conversion.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all PDF files in input folder
    try:
        pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    except FileNotFoundError:
        return f"Input folder '{input_folder}' not found."
    except PermissionError:
        return f"Permission denied to access input folder '{input_folder}'."

    if not pdf_files:
        return f"No PDF files found in '{input_folder}'."

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        md_filename = os.path.splitext(pdf_file)[0] + ".md"
        md_path = os.path.join(output_folder, md_filename)

        # Open PDF and extract text page by page
        doc = fitz.open(pdf_path)
        md_lines = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            md_lines.append(f"# Page {page_num + 1}\n\n{text}\n\n---\n")

        # Write to markdown file
        with open(md_path, "w", encoding="utf-8") as f:
            f.writelines(md_lines)

    return f"Converted {len(pdf_files)} PDFs from '{input_folder}' to Markdown files in '{output_folder}'."

if __name__ == "__main__":
    # Run the FastMCP app server
    mcp.run()
