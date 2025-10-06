FROM python:3.12-slim

# Dipendenze di sistema minime (opzionale ma utile per psycopg2-binary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia il codice
COPY backend /app/backend
COPY docs /app/docs

# 👇 Punto importante: il package 'backend' sta in /app/backend,
# quindi aggiungo /app a PYTHONPATH per poter importare "backend.*"
ENV PYTHONPATH=/app

# Torno a lavorare nel path che usi tu
WORKDIR /app/backend

EXPOSE 8000

# Avvio coerente con i tuoi import ("from backend.core..."): 
# uso il modulo completo 'backend.main:app' (funziona anche se il WORKDIR è /app/backend)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
