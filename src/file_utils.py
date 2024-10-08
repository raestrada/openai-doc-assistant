import os
import shutil

def get_markdown_files(directory):
    """Recorre un directorio y obtiene todos los archivos markdown (.md)"""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def read_file(file_path):
    """Lee el contenido de un archivo"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def copy_files_to_destination(source_dir, dest_dir):
    """Copia archivos y carpetas procesadas al directorio de destino"""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        dest_path = os.path.join(dest_dir, relative_path)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dest_file)

def generate_folder_structure(directory):
    """Genera una representación de la estructura de archivos y carpetas"""
    structure = []
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}- {os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            structure.append(f"{sub_indent}- {file}")
    return "\n".join(structure)

def create_mkdocs_prompt(directory):
    """Crea un prompt para OpenAI usando la estructura de archivos"""
    folder_structure = generate_folder_structure(directory)
    prompt = f"""
Based on the following folder structure and the files provided in the vector store, generate a `mkdocs.yml` file suitable for Backstage Tech Docs.

Folder Structure:
{folder_structure}

Please ensure that the generated `mkdocs.yml` reflects this structure, properly organizing the documentation sections and pages as per the files and their respective directories.
"""
    return prompt

def write_file(file, processed_content, source_dir, dest_dir):
    # Obtener la ruta relativa del archivo desde source_dir
    if os.path.dirname(file) == '':
        # No hay directorios, devolver solo el nombre del archivo
        relative_path = file
    else:
        # Hay directorios, calcular la ruta relativa
        relative_path = os.path.relpath(file, source_dir)
    
    # Construir la ruta de destino reemplazando source_dir por dest_dir
    dest_file_path = os.path.join(dest_dir, relative_path)
    
    # Crear los directorios necesarios en la ruta de destino
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    
    # Escribir el contenido procesado en el archivo de destino
    with open(dest_file_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)
