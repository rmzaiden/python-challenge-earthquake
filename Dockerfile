FROM python:3.9

WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt requirements-dev.txt ./
COPY .env ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copie o conteúdo do diretório src para o diretório de trabalho atual (/app)
COPY src/ ./

# Verifique a estrutura de diretório (apenas para diagnóstico, remover depois)
RUN ls -la

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

