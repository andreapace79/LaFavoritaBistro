# 🧭 Memorandum di Progetto – Gestionale Bistrò (La Favorita)

> Documento vivo per mantenere allineamento, ambito, stato avanzamento e TODO. Aggiorna qui e spunta le attività completate.

---

## 🎯 Visione & Obiettivi

Costruire un gestionale completo e modulare per il bistrò, con moduli attivabili/disattivabili, API-first, sicuro e osservabile, integrabile con registratore fiscale e POS esterni.

---

## 🏗️ Architettura (alto livello)

* **Core condiviso:** Auth, RBAC (ruoli/permessi a tabelle), utenti, audit log, error handling, i18n, configurazioni.
* **Moduli dominio (plug-in):**

  1. **Aree & Tavoli (editable + layout)** – gestione aree, tavoli, oggetti grafici (muro, strada, cespuglio, fioriera, ecc.).
  2. **Comande** – creazione, instradamento a reparti (cucina/bar), stati (in preparazione/servita), priorità.
  3. **Ricette** – distinte base (BOM), ingredienti, resa, allergeni.
  4. **Magazzino** – carichi/scarichi, movimenti, giacenze.
  5. **Consumi & Sprechi** – registrazione scarti, analisi resa, suggerimenti riduzione.
  6. **Fornitori & Sottoscorta** – anagrafiche, listini, riordino, alert low-stock.
  7. **Ordini & Conti** – carrello tavolo, split conto, sconti, tasse (IVA), note.
  8. **Pagamenti (adapters)** – interfacce con POS/registratore esterni; riconciliazione pagamenti.
  9. **Timbrature dipendenti** – presenze, turni, report ore.
  10. **Spese accessorie & Mini bilancio** – costi fissi/variabili, margini, P&L sintetico.
  11. **KPI & Analytics** – dashboard, trend, ABC prodotti, margini, tempi servizio.
  12. **Backup & Restore (locale)** – backup giornalieri automatici di DB e app, retention minima 7 giorni, restore veloce.
* **Integrazioni:** Adapter pattern per POS/registratore (REST/SDK), code di messaggistica per resilienza (eventuale).
* **Distribuzione:** Docker Compose (dev) → Nginx reverse proxy, Postgres, Backend API, Frontend.

---

## 📦 Standard & Convenzioni

* **API-first** (OpenAPI), versioning `/api/v1`.
* **RBAC completo**: tabelle `roles`, `permissions`, `role_permissions`, `user_roles`.
* **Migrazioni DB**: Alembic.
* **.env** gestione sicura + `.env.example`.
* **Audit & Log**: request/response ids, audit azioni sensibili.
* **Osservabilità**: health checks, metrics base.
* **Qualità**: pytest + coverage minimo, pre-commit (black, isort, flake8 opz.).

---

## 🗺️ Roadmap (macro)

* [ ] **Core Base**: Auth JWT, RBAC tabelle, utenti, audit, Alembic, config.
* [ ] **Aree & Tavoli & Layout**: CRUD aree/tavoli, layout objects (muro/strada/cespuglio/fioriera…), API.
* [ ] **Comande**: lifecycle, stampa/esportazione, filtri per reparto.
* [ ] **Ricette**: BOM, resa, allergeni, costo ricetta.
* [ ] **Magazzino & Consumi**: movimenti, giacenze, scarico da comande/ricette.
* [ ] **Fornitori & Sottoscorta**: listini, riordino, alert.
* [ ] **Ordini & Conti & Pagamenti (adapter)**: split conto, sconti, IVA, integrazioni POS/fiscale.
* [ ] **Timbrature**: registrazione, report.
* [ ] **Spese & Mini bilancio**: P&L sintetico.
* [ ] **KPI & Analytics**: dashboard e reportistica.
* [ ] **Backup & Restore**: script automatici, cron, retention 7 giorni.
* [ ] **Infra**: Nginx HTTPS, backup DB, CI basica.

---

## ✅ Definition of Done (per modulo)

* API CRUD + business rules
* Migrazioni Alembic
* Test pytest (unit/integration)
* Documentazione OpenAPI coerente
* Permessi/RBAC applicati
* Log/audit dove sensibile

---

## 🔒 RBAC – Tabelle

* `roles(id, name)`
* `permissions(id, code, description)`
* `role_permissions(role_id, permission_id)`
* `user_roles(user_id, role_id)`

Permessi esempio: `area.read`, `area.write`, `table.write`, `order.close`, `inventory.adjust`, `pay.close`, `kpi.view`, ecc.

---

## 📊 KPI iniziali

* Vendite giornaliere/settimanali/mensili
* Margine per prodotto/categoria
* Tempo medio servizio (ordine→chiusura)
* Sprechi (%) e valore
* Rotazione magazzino, giorni di copertura

---

## 🧩 Backlog dettagliato (checklist)

### Core

* [ ] Auth JWT
* [ ] RBAC tabelle + seeding ruoli/permessi
* [ ] Users CRUD
* [ ] Audit log middleware
* [ ] Alembic setup + prima migrazione

### Aree & Tavoli & Layout

* [ ] Modelli: Area, Table, LayoutObject
* [ ] API: CRUD aree
* [ ] API: CRUD tavoli
* [ ] API: CRUD oggetti layout (muro, strada, cespuglio, fioriera, …)
* [ ] Vincoli: univocità numero tavolo per area

### Comande

* [ ] Stato: draft → sent → in_prep → ready → served → closed/canceled
* [ ] Smistamento per reparto (cucina/bar)
* [ ] Scarico ingredienti da ricette

### Ricette

* [ ] Modelli: Recipe, RecipeItem(ingredient, qty, unit)
* [ ] Costo ricetta e resa
* [ ] Allergeni

### Magazzino & Consumi

* [ ] Modelli: Item, StockMove (in/out/adjust)
* [ ] Giacenze e valorizzazione
* [ ] Sottoscorta: soglie e alert

### Fornitori & Riordino

* [ ] Suppliers, PriceLists
* [ ] Generazione proposta d’ordine

### Ordini & Conti

* [ ] Carrello per tavolo
* [ ] Split conto, sconti, IVA

### Pagamenti (adapter)

* [ ] Interfacce: POS, registratore fiscale (esterni)
* [ ] Riconciliazione pagamenti

### Timbrature

* [ ] Clock-in/out, turni
* [ ] Report ore

### Spese & Mini bilancio

* [ ] Categorie costi
* [ ] P&L sintetico

### KPI & Statistiche

* [ ] Dashboard
* [ ] Report esportabili (CSV/PDF)

### Backup & Restore

* [ ] Script backup DB (cron, retention 7 giorni)
* [ ] Script backup app/config
* [ ] Documentazione restore
* [ ] Test ripristino periodico

### Infra & Qualità

* [ ] HTTPS Nginx (Let’s Encrypt)
* [ ] Backup/restore DB
* [ ] CI base (tests on push)

---

## 🔜 Prossimi passi (operativi)

1. Integrare **RBAC tabelle** e migrazioni Alembic.
2. Consolidare **Aree/Tavoli/Layout** con API protette.
3. Preparare seed iniziale (ruoli, permessi, admin).
4. Implementare **Backup giornaliero** con script cron.
5. Test end-to-end: create area → tavoli → layout → ordine.

---

## 📎 Note e Decision Log

* POS/Registratore: integrazione via adapter per evitare complessità fiscali nel core.
* Moduli attivabili tramite feature flags/config.
* Frontend: editor layout (es. canvas/SVG, libreria Konva.js o simile).
* Backup: locale, giornaliero, retention minima 7 giorni; restore testato periodicamente.

---

*(Aggiorna i checkbox man mano che completi le attività. Questo documento è la base di allineamento tra sessioni.)*
# MEMORANDUM - Gestionale Bistrò

---

## ✅ Stato attuale (2025-10-02)

- **Backend**
  - Avviato con FastAPI + SQLAlchemy + PostgreSQL in Docker.
  - Modulo RBAC: creazione utenti, lettura elenco utenti, aggiornamento (username e password).
  - Testati endpoint via `curl` e Swagger UI → funzionanti.
  - Database gestito in container, con volumi per la persistenza.

- **Frontend**
  - Next.js avviato in container.
  - Pagina `index.js` con logo locale visibile.
  - Pagina `users.js` collegata al backend → mostra elenco utenti, con struttura tabella (ID, username, azioni).
  - UI ancora minimale (stile base, sfondo bianco, font arial).

- **DevOps**
  - Repository GitHub sincronizzato (`main` → stato locale aggiornato con `--force`).
  - Docker Compose funzionante (backend + frontend + db).
  - Struttura pulita (no `.next`, `node_modules`, ecc. nel repo).
  - Backup giornaliero tracciato.

---

## 🔄 TODO prossimi step

- **Frontend**
  - Rifinire interfaccia `users.js`: creazione ed eliminazione utenti, ruoli/permessi.
  - Migliorare design (`tailwindcss` o simile).
  - Routing verso aree/tavoli, comande.

- **Backend**
  - Aree/tavoli editabili con layout grafico.
  - Moduli: comande, ricette, magazzino, fornitori, spese, KPI/statistiche, timbrature dipendenti.
  - Backup DB automatico + restore.
  - Integrazione futura con registratore di cassa/POS esterni.

- **Sistema**
  - Automatizzare backup giornaliero DB e repo.
  - Aggiungere test automatici (pytest).
  - Configurare CI/CD base (GitHub Actions).

---

## 📊 Avanzamento progetto

- **Avanzamento totale:** **25%**  
- **Data stimata di fine lavori:** **2026-01-31**  
  _(la stima tiene conto dell’attuale velocità di sviluppo e dei moduli ancora da completare)_

---

## 📦 Backup giornaliero

- **2025-10-02** — commit `HEAD` su branch `main` — backend RBAC attivo, frontend avviato, logo e pagina utenti base funzionanti.
