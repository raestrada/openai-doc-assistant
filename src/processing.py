import os
from file_utils import get_markdown_files, read_file, write_file, copy_files_to_destination, generate_folder_structure
from openai_client import vectorize_files, process_with_openai
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def process_file_with_openai(assistant, content, instructions):
    """Procesa un archivo usando OpenAI con el contexto vectorizado"""
    prompt = f"Usa estas instrucciones:'{instructions}' y procesa el siguiente archivo tratando de mantener la estructura y el contenido. Es un documento en markdown. Entregalo de tal forma que la repsuesta solo contenga el documento modificado.Este es el contenido:\n{content}"
    print(f"{Fore.CYAN}{Style.BRIGHT}Procesando archivo con OpenAI...")  # Log de progreso con estilo
    return process_with_openai(assistant, prompt)

def process_markdown_files(source_dir, instructions_file, dest_dir, generate_files=False):
    """Procesa todos los archivos markdown en el directorio según las instrucciones y copia al directorio de destino"""
    print(f"{Fore.GREEN}{Style.BRIGHT}Obteniendo archivos markdown desde: {source_dir}...")  # Log de progreso con estilo
    markdown_files = get_markdown_files(source_dir)
    
    print(f"{Fore.MAGENTA}Vectorizando archivos markdown: {markdown_files}...")  # Log de progreso con estilo
    assistant = vectorize_files(markdown_files)
    
    print(f"{Fore.YELLOW}Leyendo archivo de instrucciones: {instructions_file}...")  # Log de progreso con estilo
    instructions = read_file(instructions_file)

    # Procesar cada archivo markdown
    for file in markdown_files:
        print(f"{Fore.BLUE}{Style.BRIGHT}Procesando archivo: {file}...")  # Log de progreso con estilo
        content = read_file(file)
        processed_content = process_file_with_openai(assistant, content, instructions)
        print(f"{Fore.CYAN}Escribiendo contenido procesado en archivo: {file}...")  # Log de progreso con estilo
        write_file(file, processed_content, source_dir, dest_dir)
    
    # Generar archivos adicionales si se solicita
    if generate_files:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Generando archivos adicionales usando OpenAI...")  # Log de progreso con estilo
        generate_additional_files_with_openai(source_dir, dest_dir, assistant)

def generate_additional_files_with_openai(source_dir, dest_dir, assistant):
    """Genera un archivo mkdocs.yml y sobrescribe index.md pidiéndolo a OpenAI"""
    print(f"{Fore.GREEN}{Style.BRIGHT}Generando estructura de carpetas para mkdocs.yml en: {source_dir}...")  # Log de progreso con estilo
    mkdocs_prompt = generate_folder_structure(source_dir)
    mkdocs_content = process_with_openai(assistant, mkdocs_prompt)
    print(f"{Fore.CYAN}Escribiendo mkdocs.yml en: {os.path.join(source_dir, 'mkdocs.yml')}...")  # Log de progreso con estilo
    write_file("mkdocs.yml", mkdocs_content, source_dir, dest_dir)

    print(f"{Fore.YELLOW}Generando contenido para index.md...")  # Log de progreso con estilo
    index_md_prompt = "Generate an index.md file summarizing the contents of the documentation. I want only the markdown on the response"
    index_md_content = process_with_openai(assistant, index_md_prompt)
    print(f"{Fore.BLUE}Escribiendo index.md en: {os.path.join(source_dir, 'index.md')}...")  # Log de progreso con estilo
    write_file("index.md", index_md_content, source_dir, dest_dir)
