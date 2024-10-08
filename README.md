# openai-doc-assistans

## Introduction

**openai-doc-assistans** is a tool designed to iteratively refine and process all the documents in a folder by using the knowledge contained within those documents. It utilizes the OpenAI API, employing behaviors and instructions to ensure the most accurate and contextual retrieval of information. This is particularly useful when dealing with token limitations in OpenAI models, allowing the system to progressively improve its outputs as more knowledge is processed and refined through retrieval.

## Key Features

- **Iterative Document Processing**: Automatically processes all files in a folder, using the knowledge from the entire folder to refine the output.
- **Behavior-Driven Processing**: Customizable behaviors and instructions guide how the documents are processed, enabling context-aware responses.
- **Retrieval-Based Refinement**: As knowledge is generated, the system refines previous results by leveraging retrieval, overcoming token limitations and improving accuracy.
- **Seamless Integration with OpenAI API**: Utilizes OpenAI's language models to process and analyze content effectively.
- **Modular Design**: Easy to integrate into existing workflows and adaptable to various document types.

## Installation

1. Install `Poetry` if you haven’t done so already. You can follow [the official Poetry installation instructions](https://python-poetry.org/docs/#installation).

2. Clone this repository or download the files.

3. Install the required dependencies by running:

   ```bash
   poetry install
   ```

4. Set up your OpenAI API key as an environment variable. Create a `.env` file at the root of the project and add the following:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

## How It Works

**openai-doc-assistans** operates by iterating over all the files in a specified folder, processing the content using OpenAI’s language models while considering the entire folder's knowledge to improve results. Here's the process:

1. **Initial Document Ingestion**: All files in the specified folder are loaded and prepared for processing. The tool identifies each file’s content to understand the knowledge base it will work with.

2. **Behavior and Instructions**: The processing is guided by a predefined set of behaviors and instructions. These determine how the content should be handled, what kind of output is expected, and how the agent should interpret the information.

3. **First Pass Processing**: The system processes each document using OpenAI’s API, taking into account the token limits. Initial knowledge is generated and saved.

4. **Retrieval and Refinement**: After the first pass, the generated knowledge is reprocessed through a retrieval system. This allows **openai-doc-assistans** to refine previous outputs based on the growing body of knowledge from the folder, effectively improving the content while staying within token limits.

5. **Continuous Improvement**: As more content is processed and refined, the system continuously enhances its understanding and outputs, providing more accurate and context-aware results with each iteration.

## Usage

This script processes markdown files in a directory and can generate a `mkdocs.yml` file and an `index.md`. The processed and generated files will be copied to a destination directory.

### Syntax

```bash
poetry run python src/main.py <source_dir> <instructions_file> <dest_dir> [--generate_files]
```

- `<source_dir>`: The path to the directory containing the original markdown files.
- `<instructions_file>`: The path to the file that contains the instructions for processing the markdown files.
- `<dest_dir>`: The path to the directory where the processed and generated files will be copied.
- `--generate_files`: (Optional) Include this option to generate additional files such as `mkdocs.yml` and `index.md`.

### Example

Let's assume you have a `docs/` directory containing your markdown files, an instructions file called `instructions.txt`, and you want the processed files to be copied to an `output/` directory:

```bash
poetry run python src/main.py docs/ instructions.txt output/ --generate_files
```

## Project Structure

- `main.py`: The entry point for processing all documents within a folder.
- `openai_client.py`: Manages queries and interactions with the OpenAI API after the documents have been processed.
- `processing.py`: Contains the core logic for document processing and knowledge refinement.
- `file_utils.py`: Utility functions for handling file I/O and managing the document folder.

## Contributions

Feel free to fork this repository and submit pull requests for improvements or additional features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
