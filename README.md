# CCT Extractor with OpenAI
This repository is a tool that uses the OpenAI API to extract the insurance clauses from CCT files.
CCT's are the Collective Bargaining Agreements, they are the agreements between the employer and the employees, they are used to define the rights and obligations of the employees. Insurance clauses are the clauses that define the insurance benefits that the employees have.

>[!TIP]
> Are you from Brazil? You can see our portuguese version of this README [here](docs/README.pt-br.md)
### Environment variables

- OPENAI_API_KEY : Key from openAI API, you can get it from [here](https://platform.openai.com/api-keys)
- ASSISTANT_ID : If you don't want to generate a new assistant every time, you can use the same assistant by providing the assistant id, you can get it from [here](https://platform.openai.com/assistants)
- CCT_DIRECTORY : This is the directory where the CCT files are stored, the CCT files are the files that contain the aggreements, this repository don't tell you how to get the CCT files.
- ASSISTANT_INSTRUCTIONS : This is the instructions used to create an assistant, they will be used to create a new assistant from scratch if ASSISTANT_ID is not provided.

### How to run

You should install tesseract-ocr to run the script, you can install it following the instructions [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

- Install the dependencies by running `pip install -r requirements.txt`
- Run the script by running `python main.py`
- The script will create a new assistant if ASSISTANT_ID is not provided, and it will use the same assistant if ASSISTANT_ID is provided.
- The script will read the CCT files from the CCT_DIRECTORY and it will extract the CCTs using the openAI API.
- They will be splited between CCTs that have a insurance clause and CCTs that don't have a insurance clause. The CCTs that have a insurance clause will be stored in the `ccts_with_insurance` directory and the CCTs that don't have a insurance clause will be stored in the `ccts_without_insurance` directory.
- For each cct with insurance clause should exists a file that is a summary of important information about the insurance clause, this file will be stored in the `__summary_text_path` directory.

The repository is still in development, so some things may not be working correctly, feel free to open issues and PRs.