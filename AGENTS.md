# AGENTS: painel-eleicoes-2026-dados

This repo tracks Brazilian electoral data (TSE) for 2026 elections. The main workflow is driven by `update.py`.

## 🔑 Core entrypoint

```bash
# Full cycle: download → aggregate → validate → publish
python pipeline/update.py --ciclo ele2026
```

## 📦 Common sub-commands (from update.py)

| Flag | Purpose |
|------|---------|
| `--mock` | Uses `pipeline/mock_data.py` instead of TSE download. Good for testing the full publish flow without network. |
| `--mock --no-push` | Generates local data only, skips GitHub push. |
| `--zerado` | Uses real candidate registry with all votes zeroed. |
| `--turno 2` | Generates `live-2t.json` / `historico-2t.json` for second turno. Does NOT touch `live.json` of 1st turno. |
| `--forcar` | Bypasses sanity validation refusal (use only after reviewing problemas). |
| `--eleicoes-json <file>` | Override election codes from a JSON file. |

## ⚙️ One-time setup

### GitHub publishing (first time only)

```bash
# 1. Create empty public repo on GitHub: ratitu/painel-eleicoes-2026-dados-dados-publicos
# 2. Set the repo URL in config.json (already set to https://github.com/ratitu/painel-eleicoes-2026-dados-dados-publicos.git)
python pipeline/publicar_dados.py --configurar
```

This clones the empty repo into `pipeline/dados_publicos/`. After this, every `update.py` run will commit+push new data there.

### Site directory

The `pipeline/site/` directory must exist and contain `live.json` for `update.py` to write `status.json`. If missing, create it:

```bash
mkdir -p pipeline/site
```

## 🚫 Gotchas & pitfalls

- **110/248 files may 404** when running `--ciclo ele2026` against the TSE simulator. This is expected — the Sep 2026 simulation doesn't have all municipal files. 138 of 248 typically succeed.
- **`status.json` crash if `pipeline/site/` is missing** — always ensure the dir exists before running `update.py`.
- **`--no-push` only skips GitHub push** — it does NOT skip the TSE download or aggregate steps.
- **Turno 2 is isolated** — running `--turno 2` only affects `live-2t.json` / `historico-2t.json`; the 1st turno files remain untouched.
- **Sanidade validation** refuses to publish if valid/votos sections decreased (monotonicity check). Use `--forcar` only after confirming with the team.

## 🔄 Full pipeline flow

```
update.py --ciclo ele2026
  → tse_downloader.py --update  (downloads from TSE simulator, may have 404s)
  → aggregate_2026.py           (generates site/live.json)
  → validar_live.py             (sanity check: votos/monotonic sections)
  → publicar_dados.py           (copies JSONs to dados_publicos/ + git commit + push)
  → raw.githubusercontent.com     (site HTML/JS reads data directly, no Netlify deploy needed)
```

## 📁 Key directory ownership

| Directory | Purpose | Owner |
|-----------|---------|-------|
| `pipeline/dados_baixados/` | Downloaded EA20 files from TSE | tse_downloader.py |
| `pipeline/dados_publicos/` | Public GitHub repo clone (live.json, historicos, status) | publicar_dados.py |
| `pipeline/site/` | Working copy with live.json + status.json (feeds the website) | update.py |
| `site/` (repo root) | Static HTML/JS that reads from raw.githubusercontent.com | Frontend (separate from this code) |

## 🛠️ Verified commands

```bash
# Test full publish flow with mock data (no TSE)
python pipeline/update.py --mock --no-push

# Verify dados_publicos was updated
ls pipeline/dados_publicos/

# Create site dir if missing
mkdir -p pipeline/site

# Run full cycle (may have ~110/248 404s from simulator)
python pipeline/update.py --ciclo ele2026
```