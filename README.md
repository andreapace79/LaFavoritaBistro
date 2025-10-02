
---

## 🔹 Aggiornamento file
Copia/incolla direttamente con:

```bash
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
- Database Postgres esposto su porta host \`55432\`

## Struttura del progetto

\`\`\`
bistro-gestionale/
├── backend/            # Codice backend FastAPI
│   ├── core/           # Config, db, auth, RBAC
│   ├── modules/        # Moduli funzionali (areas, employees, ecc.)
│   └── Dockerfile      # Dockerfile backend
│
├── frontend/           # Frontend Next.js
│   ├── pages/          # Pagine principali
│   └── Dockerfile      # Dockerfile frontend
│
├── db/                 # Configurazione database
│   ├── init.sql        # Script init/seed DB
│   └── data/           # Volume dati Postgres (ignorato da Git)
│
├── docs/               # Documentazione di progetto
│   └── MEMORANDUM.md   # Stato avanzamento & specifiche
│
├── docker-compose.yml  # Orchestrazione servizi
└── README.md           # Questo file
\`\`\`

## Documentazione di progetto

👉 Per stato avanzamento, TODO e specifiche dettagliate consulta:  
[docs/MEMORANDUM.md](docs/MEMORANDUM.md)
EOF

