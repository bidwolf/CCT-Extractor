"""
Configurações para o uso da API do OpenAI.

Para utilizar a API do OpenAI, é necessário configurar a variável de ambiente OPENAI_API_KEY

"""

import os
from dotenv import load_dotenv
from src.types.config import Config


load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY não configurada no ambiente.")

config = Config(
    {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "assistant_id": os.environ.get("ASSISTANT_ID", ""),
        "assistant_description": "Este modelo é treinado para auxiliar na análise de cláusulas de seguro em convenções coletivas de trabalho.",
        "assistant_model": "gpt-4o-2024-08-06",
        "cct_directory": os.environ.get("CCT_DIRECTORY", "ccts"),
        "assistant_instructions": (
            os.environ.get(
                "ASSISTANT_INSTRUCTIONS",
                "Análise de cláusulas de seguro em convenções coletivas de trabalho.",
            )
        ),
        "response_format": "auto",
        "tools": [{"type": "code_interpreter"}],
        # "tool_resources": {
        #     "code_interpreter": {
        #         "file_ids": []  # Adicione arquivos de jurisprudência, entendimentos do TST, etc., se necessário.
        #     }
        # },
    }
)
