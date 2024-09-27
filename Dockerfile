
FROM python:3.11

WORKDIR /app

COPY ./server.py ./Dockerfile ./requirements.txt /app/
COPY ./Llama-3.2-1B-Instruct-Q4_K_M.gguf /app/

RUN mkdir -p /app/hf_cache /app/models
RUN chmod -R 777 /app/hf_cache /app/models

ENV HF_HOME=/app/hf_cache

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "server.py"]
