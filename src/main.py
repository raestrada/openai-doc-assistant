import argparse
from processing import process_markdown_files
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃          🌟 Iniciando el procesamiento 🌟        ┃")
    print("┃        de archivos markdown con estilo!        ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    
    parser = argparse.ArgumentParser(description="Process markdown files and generate mkdocs.yml.")
    parser.add_argument("source_dir", type=str, help="Path to the source directory containing markdown files.")
    parser.add_argument("instructions_file", type=str, help="Path to the file containing instructions for processing.")
    parser.add_argument("dest_dir", type=str, help="Path to the destination directory where processed files will be copied.")
    parser.add_argument("--generate_files", action="store_true", help="Generate additional files like mkdocs.yml and index.md")

    print(f"{Fore.YELLOW}🔍 Analizando argumentos de línea de comandos...")  # Log de progreso
    args = parser.parse_args()

    print(f"{Fore.CYAN}📂 Procesando archivos desde: {args.source_dir}")
    print(f"{Fore.CYAN}📑 Usando instrucciones de: {args.instructions_file}")
    print(f"{Fore.CYAN}🚀 Copiando archivos procesados a: {args.dest_dir}")
    print(f"{Fore.CYAN}🛠️ Generar archivos adicionales: {args.generate_files}")

    process_markdown_files(args.source_dir, args.instructions_file, args.dest_dir, generate_files=args.generate_files)

    print(f"{Fore.GREEN}{Style.BRIGHT}")
    print("🎉✨ Procesamiento completado exitosamente! ✨🎉")
    print("Gracias por utilizar nuestro procesador de archivos markdown. ¡Hasta la próxima!")
