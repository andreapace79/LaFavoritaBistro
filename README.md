cat <<EOF > README.md
# La Favorita Bistro - Gestionale

Gestionale modulare per bar/bistrò.

## Architettura
- **Backend**: FastAPI + SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: Next.js
- **Orchestrazione**: Docker Compose

## Avvio rapido

Clona il repository, entra nella cartella del progetto e lancia:

\`\`\`bash
docker compose up --build -d
\`\`\`

- Backend API → [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)  
- Database Postgres esposto su porta host `55432`

## Documentazione di progetto

👉 Per stato avanzamento, TODO e specifiche dettagliate consulta:  
[docs/MEMORANDUM.md](docs/MEMORANDUM.md)
EOF
