"""This module aims to create a cct assistant in the chat gpt, if it doesn't exist yet."""

import os
import shutil
import json
import re
from openai import AssistantEventHandler, OpenAI, OpenAIError
from openai.resources.beta.assistants import Assistant
from pydantic import ValidationError
from src.config import Config
from src.pdf import extract_text_and_images, extract_text_from_pdf
from src.types.cct_response import CCTResponse


class CCTAssistant:
    """This class creates a CCT assistant in the chat gpt, if it doesn't exist yet."""

    _existent_assistant: Assistant
    __summary_text_path = "resumo_seguro.txt"
    __directory_with_insurance = "CCTs_Com_Seguro"
    __directory_without_insurance = "CCTs_Sem_Seguro"

    def __init__(self, config: Config, event_handler: AssistantEventHandler):
        self._config = config
        self._client = OpenAI(api_key=self._config["api_key"])
        self._cct_assistant = self._get_or_create_assistant()
        self._event_handler = event_handler
        self._cct_with_insurance_dir = os.path.join(
            self._config["cct_directory"], self.__directory_with_insurance
        )
        self._cct_without_insurance_dir = os.path.join(
            self._config["cct_directory"], self.__directory_without_insurance
        )

    def _get_or_create_assistant(self):
        try:
            assistants = self._client.beta.assistants.list()
        except OpenAIError as e:
            print(f"Erro ao listar assistentes: {e}")
            assistants = []

        assistant = None
        for a in assistants:
            if a.description == self._config["assistant_description"]:
                print(f"Assistant encontrado: {a.id}")
                assistant = a
                break

        if not assistant:
            assistant = self._client.beta.assistants.create(
                model=self._config["assistant_model"],
                description=self._config["assistant_description"],
                instructions=self._config["assistant_instructions"],
                response_format={"type": "json_object"},
                tools=self._config["tools"],
            )
            print(f"Assistant criado: {assistant.id}")
        return assistant

    def split_text_sliding_window(self, text: str, overlap: int = 200):
        """Divide o texto em blocos usando janela deslizante para evitar cortes abruptos."""
        words = text.split()
        chunks = []
        total_words = len(words)
        for i in range(0, total_words, total_words // 3 - overlap):
            print(f"Processando chunk {i} de {total_words}")
            start = i
            end = min(i + total_words // 3, total_words)
            new_chunk = " ".join(words[start:end])
            new_chunk = new_chunk + f"\nchunk {i} of {total_words}"
            chunks.append(" ".join(words[start:end]))

        return chunks

    def _analyze_text_with_ai(self, text: str, file_name: str) -> CCTResponse | None:
        """Analyze the text in the text and create a summary of the insurance coverages and conditions of the insurance."""

        insurance_review_thread = self._client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Chunk da CCT {file_name}",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, analise o texto e me dê um resumo das coberturas e condições do seguro.",
                        },
                        {"type": "text", "text": text},
                    ],
                },
            ]
        )
        try:
            run = self._client.beta.threads.runs.create_and_poll(
                thread_id=insurance_review_thread.id,
                assistant_id=self._cct_assistant.id,
            )
        except OpenAIError as e:
            print(f"Erro ao analisar o texto: {e}")
            return None
        if run.status == "completed":
            try:
                all_messages = self._client.beta.threads.messages.list(
                    thread_id=insurance_review_thread.id
                )
                for message in all_messages:

                    if message.role == "assistant":
                        try:
                            for content in message.content:
                                if content.type == "text":
                                    parsed_data = json.loads(content.text.value)
                                    valid_response = CCTResponse(**parsed_data)
                                    if valid_response:
                                        if valid_response.erro:
                                            print(
                                                f"Erro ao listar mensagens: {valid_response.erro}"
                                            )
                                        print(f"Resumo: {valid_response.resumo}")
                                        return valid_response
                        except (ValidationError, json.JSONDecodeError) as e:
                            print(f"Erro ao listar mensagens: {e}")
                            return None
                return None
            except OpenAIError as e:
                print(f"Erro ao listar mensagens: {e}")
                return None
        return None

    def process_ccts(self):
        """Processa todos os arquivos de CCTs no diretório especificado."""
        # Create directories if they don't exist
        os.makedirs(self._cct_with_insurance_dir, exist_ok=True)
        os.makedirs(self._cct_without_insurance_dir, exist_ok=True)
        print("Diretórios criados.")
        for filename in os.listdir(self._config["cct_directory"]):
            print(f"Processando: {filename}")
            file_path = os.path.join(self._config["cct_directory"], filename)
            if filename.endswith(".pdf"):
                file_path = os.path.join(self._config["cct_directory"], filename)
                print(f"Processando: {filename}")

                text = extract_text_from_pdf(file_path)
                if not text or text.isspace():
                    print("Texto não extraído. Tentando extrair com OCR.")
                    extracted_text = extract_text_and_images(file_path)
                    if extracted_text and len(extracted_text) > 0:
                        for line in extracted_text:
                            text += line
                    else:
                        print("Texto não extraído com OCR.")
                        shutil.move(
                            file_path,
                            os.path.join(self._cct_without_insurance_dir, filename),
                        )
                        print(f"{filename} movido para CCTs_Sem_Seguro")
                        return
                text = re.sub(r"\n+", "\n", text)
                chunks = self.split_text_sliding_window(text)
                combined_analysis = CCTResponse(
                    resumo="",
                    abrangencia_territorial="",
                    categoria_profissional="",
                    data_base="",
                    vigencia="",
                    erro="",
                )
                for i, chunk in enumerate(chunks, start=1):
                    print(f"Analisando chunk: {i}")
                    analysis = self._analyze_text_with_ai(chunk, file_name=filename)
                    if analysis:
                        if (
                            analysis.abrangencia_territorial
                            and analysis.abrangencia_territorial.strip()
                        ):
                            combined_analysis.abrangencia_territorial += (
                                analysis.abrangencia_territorial + "\n"
                            )
                        if (
                            analysis.categoria_profissional
                            and analysis.categoria_profissional.strip()
                        ):
                            combined_analysis.categoria_profissional = (
                                analysis.categoria_profissional
                            )
                        if analysis.data_base and analysis.data_base.strip():
                            combined_analysis.data_base = analysis.data_base.strip()
                        if analysis.vigencia and analysis.vigencia.strip():
                            combined_analysis.vigencia = analysis.vigencia.strip()
                        if analysis.resumo and analysis.resumo.strip():
                            combined_analysis.resumo += analysis.resumo + "\n"
                    if (
                        combined_analysis.resumo
                        and combined_analysis.abrangencia_territorial
                        and combined_analysis.categoria_profissional
                        and combined_analysis.data_base
                        and combined_analysis.vigencia
                    ):
                        break
                analysis = (
                    combined_analysis if combined_analysis.resumo.strip() else None
                )
                if not analysis:
                    print("Não foi identificado resumo de seguro.")
                self._move_cct_based_on_analysis(
                    filename,
                    file_path,
                    analysis,
                )

    def _move_cct_based_on_analysis(
        self, filename: str, file_path: str, analysis: CCTResponse | None
    ):
        if not analysis or not analysis.resumo:
            shutil.move(
                file_path, os.path.join(self._cct_without_insurance_dir, filename)
            )
            print(f"{filename} movido para CCTs_Sem_Seguro")
            return

        cct_name = os.path.splitext(filename)[0]
        cct_folder = os.path.join(self._cct_with_insurance_dir, cct_name)
        os.makedirs(cct_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(cct_folder, filename))

        summary_path = os.path.join(cct_folder, self.__summary_text_path)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(analysis.resumo)
            f.write(
                f"Abrangência territorial: {analysis.abrangencia_territorial or "não encontrada"}"
            )
            f.write(
                f"Categoria profissional: {analysis.categoria_profissional or "não encontrada"}\n"
            )
            f.write(f"Data base: {analysis.data_base or "não encontrada"}\n")
            f.write(f"Vigência: {analysis.vigencia or "não encontrada"}")

        print(f"{filename} movido para CCTs_Com_Seguro com resumo criado.")
