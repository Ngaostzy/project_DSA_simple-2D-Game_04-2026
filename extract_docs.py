import ast
import os

def extract_docstrings_to_markdown(source_dir: str, output_file: str) -> None:
    """
    Scans the specified directory, extracts docstrings from all Python classes
    and methods using an Abstract Syntax Tree (AST), and compiles them into a
    Markdown file for technical documentation.
    
    Args:
        source_dir (str): The root directory containing the source code.
        output_file (str): The destination path for the generated Markdown report.
    """
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("# NAMELESS CAT PROJECT: SOURCE CODE DOCUMENTATION\n\n")

        # Traverse the directory tree
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    
                    # Read the source file
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        file_content = f_in.read()
                    
                    # Parse the source code into an AST node without executing it
                    tree = ast.parse(file_content)
                    
                    f_out.write(f"## File: `{file}`\n")
                    f_out.write("---\n")

                    # Iterate through the AST nodes to find classes and methods
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            f_out.write(f"### Class: `{node.name}`\n")
                            doc = ast.get_docstring(node)
                            if doc:
                                f_out.write(f"**Description:**\n```text\n{doc}\n```\n\n")
                            
                            # Iterate through the class body to find encapsulated methods
                            for sub_node in node.body:
                                if isinstance(sub_node, ast.FunctionDef):
                                    f_out.write(f"#### Method: `{sub_node.name}`\n")
                                    sub_doc = ast.get_docstring(sub_node)
                                    if sub_doc:
                                        f_out.write(f"**Description:**\n```text\n{sub_doc}\n```\n\n")
                    f_out.write("\n")

if __name__ == "__main__":
    # Define the source directory and the output documentation file
    extract_docstrings_to_markdown("src", "DOCS_REPORT.md")
    print("Documentation extraction completed successfully. Output saved to DOCS_REPORT.md")