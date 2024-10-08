import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Cargar variables de entorno
print(f"{Fore.GREEN}{Style.BRIGHT}Cargando variables de entorno...")
load_dotenv()

# Configurar el cliente de OpenAI
print(f"{Fore.YELLOW}{Style.BRIGHT}Configurando el cliente de OpenAI...")
client = OpenAI()

def vectorize_files(markdown_files):
    name = "Karasu Docs"
    """Vectoriza los archivos y los carga en el vector store"""
    
    print(f"{Fore.CYAN}Iniciando la vectorización de archivos: {markdown_files}...")
    file_streams = [open(file, "rb") for file in markdown_files]

    print(f"{Fore.MAGENTA}Creando un vector store con el nombre '{name}'...")
    vector_store = client.beta.vector_stores.create(name=name)
    
    print(f"{Fore.BLUE}Listando asistentes existentes...")
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        if assistant.name == name:
            print(f"{Fore.YELLOW}Assistant {name} already exists.")
            print(f"{Fore.RED}Deleting assistant {name}...")
            client.beta.assistants.delete(assistant_id=assistant.id)
            print(f"{Fore.RED}Assistant {name} deleted.")
            break


    print(f"{Fore.YELLOW}Subiendo archivos al vector store y esperando el procesamiento...")
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    while file_batch.status == "queued" or file_batch.status == "in_progress":
        print(f"{Fore.CYAN}Estado de la carga de archivos: {file_batch.status}")
        time.sleep(1)
    
    print(f"{Fore.GREEN}{Style.BRIGHT}Archivos subidos y procesados con éxito.")

    print(f"{Fore.YELLOW}Leyendo instrucciones desde 'src/behaviors/default.txt'...")
    with open('src/behaviors/default.txt', 'r') as file:
        instructions = file.read()

    print(f"{Fore.MAGENTA}Creando asistente con el nombre '{name}'...")
    assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
        model="gpt-4o",
    )

    print(f"{Fore.CYAN}Actualizando el asistente con los recursos de herramientas...")
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    print(f"{Fore.GREEN}{Style.BRIGHT}Asistente creado y actualizado exitosamente.")
    return assistant

def process_with_openai(assistant, prompt):
    """Envía un mensaje a OpenAI, espera la respuesta y devuelve el contenido del mensaje"""
    
    print(f"{Fore.MAGENTA}Creando un nuevo thread...")
    thread = client.beta.threads.create()

    print(f"{Fore.BLUE}Enviando mensaje al thread...")
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    print(f"{Fore.CYAN}Ejecutando el thread...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    print(f"{Fore.YELLOW}Esperando la finalización del run...")
    while run.status == "queued" or run.status == "in_progress":
        print(f"{Fore.CYAN}Estado del run: {run.status}")
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)

    print(f"{Fore.GREEN}{Style.BRIGHT}El run ha completado. Recuperando mensajes...")
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print(f"{Fore.YELLOW}Mensaje recibido de OpenAI.")
    return messages.data[0].content[0].text.value
