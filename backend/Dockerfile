FROM python:3.12-slim

# Set working dir
WORKDIR /app/backend

# Copia requirements
COPY backend/requirements.txt /app/backend/requirements.txt

# Installa dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il backend (codice, alembic.ini, ecc.)
COPY backend /app/backend

# Copia documentazione se serve
COPY docs /app/docs

# Espone la porta API
EXPOSE 8000

# Avvio del server FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
