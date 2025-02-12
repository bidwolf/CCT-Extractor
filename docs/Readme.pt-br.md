# CCT Extractor

Este repositório é uma ferramenta que utiliza a API da OpenAI para extrair informações de cláusulas de seguro de CCTS.

A ideia principal é utilizar a ferramenta para descrever de forma resumida as coberturas de seguro existentes bem como outras informações como vigência, abrangência e etc.

### Variáveis de ambiente


- OPENAI_API_KEY : Chave API da openAI que você pode adquirir [aqui](https://platform.openai.com/api-keys)
- ASSISTANT_ID : Caso deseje criar seu próprio assistente na plataforma da openAI, eu recomendo o uso, ele permite que você reutiliza 'chats' existentes com mais contexto do que sua solução faz e você pode configurar um [aqui](https://platform.openai.com/assistants)
- CCT_DIRECTORY : Esse é o diretório de onde virão os arquivos de CCT, os arquivos de CCT são os arquivos que contém os acordos de convenção coletiva em formato PDF, esse repositório não te ensina como obter os arquivos de CCT.
- ASSISTANT_INSTRUCTIONS : Essas seriam as instruções usadas para criar um assistente, nelas deve conter o contexto de uso do assistente, o que ele deve fazer e como ele deve responder. Não coloquei as instruções que usei nesse repositório, vou definir ainda se vou disponibilizar elas ou não.

### Como rodar

Você deve instalar o tesseract-ocr para poder rodar o script, você pode instalar ele seguindo as instruções [aqui](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- Instale as dependências rodando `pip install -r requirements.txt`
- Rode o script rodando `python main.py`
- O script irá criar um novo assistente se o ASSISTANT_ID não for fornecido, e irá utilizar o mesmo assistente se o ASSISTANT_ID for fornecido.
- O script irá ler os arquivos de CCT do diretório CCT_DIRECTORY e irá extrair as CCTs utilizando a API da openAI.
- Elas serão divididas entre CCTs que possuem cláusula de seguro e CCTs que não possuem cláusula de seguro. As CCTs que possuem cláusula de seguro serão armazenadas no diretório `ccts_with_insurance` e as CCTs que não possuem cláusula de seguro serão armazenadas no diretório `ccts_without_insurance`.
- Para cada CCT com cláusula de seguro deve existir um arquivo que é um resumo de informações importantes sobre a cláusula de seguro, esse arquivo será armazenado no diretório `__summary_text_path`.

O repositório ainda está em desenvolvimento, então algumas coisas podem não estar funcionando corretamente, sinta-se livre para abrir issues e PRs.