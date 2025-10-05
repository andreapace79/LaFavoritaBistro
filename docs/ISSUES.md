# 📌 Gestionale Bistrò – Issue Tracking

Questo file raccoglie le issue da trasformare in task su GitHub.  
Ogni sezione corrisponde a un’issue con titolo, descrizione e checklist.  

---

## 1. Allineamento migrazioni Alembic e test DB
**Descrizione:**  
Verificare la consistenza delle migrazioni e stabilizzare lo schema DB con la nuova tabella `audit_logs`.

**Checklist:**  
- [ ] Controllare `alembic history`  
- [ ] Eliminare revisioni orfane  
- [ ] Test con `alembic downgrade -1 && alembic upgrade head`  
- [ ] Verifica presenza tabella `audit_logs` in DB  

---

## 2. Implementazione tabella e repository Audit Logs
**Descrizione:**  
Definire e implementare la tabella `audit_logs` e collegarla agli eventi principali del sistema.  

**Checklist:**  
- [ ] Definizione schema tabella (`id`, `user_id`, `action`, `entity_type`, `entity_id`, `timestamp`)  
- [ ] Creazione modello SQLAlchemy  
- [ ] Implementazione repository per inserimento log  
- [ ] Hook per eventi: login/logout, creazione comanda, modifica stock  

---

## 3. Aggiornamento Docker Compose (healthcheck & network)
**Descrizione:**  
Aggiungere controlli e migliorare l’infrastruttura Docker.  

**Checklist:**  
- [ ] Healthcheck su container `backend` (endpoint `/health`)  
- [ ] Verifica network dedicato per DB  
- [ ] Test esecuzione `docker compose up` su ambiente pulito  

---

## 4. Schema e API base per aree, tavoli e comande
**Descrizione:**  
Implementare il primo modulo applicativo con gestione aree, tavoli e comande.  

**Checklist:**  
- [ ] Creazione tabelle `areas`, `tables`, `orders`  
- [ ] Implementazione repository per entità  
- [ ] API CRUD aree/tavoli  
- [ ] API apertura/chiusura comanda  

---

## 5. Review repository e aggiornamento README
**Descrizione:**  
Pulizia repo e aggiornamento documentazione minima per sviluppo.  

**Checklist:**  
- [ ] Controllo file temporanei e `.pyc`  
- [ ] Aggiornamento `README.md` con istruzioni:  
  - run docker  
  - apply migrations  
  - healthcheck backend  

---
