# 🧭 Git Flow – La Favorita Bistro

Repository: `git@github.com:andreapace79/LaFavoritaBistro.git`

---

## 🌿 Branch principali
| Branch | Descrizione |
|---------|-------------|
| **main** | Versione stabile pronta al deploy |
| **develop** | Integrazione di feature e test prima della release |

---

## 🚀 Branch di lavoro
| Tipo | Prefisso | Esempio |
|------|-----------|---------|
| Feature | `feature/` | `feature/rbac` |
| Fix | `fix/` | `fix/seed-permission-import` |
| Hotfix | `hotfix/` | `hotfix/api-token-expiry` |
| Refactor | `refactor/` | `refactor/auth-handlers` |
| Chore | `chore/` | `chore/update-dockerfiles` |

---

## 🧩 Flusso di sviluppo
1. **Crea branch da `develop`**
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/<nome-feature>
