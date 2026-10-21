# painel-eleicoes-2026-dados

Painel interativo de resultados das Eleições 2026 (TSE). Baixa, agrega e publica dados eleitorais do Tribunal Superior Eleitoral.

## 🚀 Quick start

```bash
# Full cycle: download + aggregate + validate + publish
python pipeline/update.py --ciclo ele2026

# Test flow with mock data (no TSE network)
python pipeline/update.py --mock --no-push
```

## 📦 What it does

1. **Download** — `tse_downloader.py` fetches EA20/EA10 files from the TSE simulator (or production when published)
2. **Aggregate** — `aggregate_2026.py` creates `site/live.json` with votes, candidates, percentages
3. **Validate** — `validar_live.py` checks monotonicity (votes/sections must only increase)
4. **Publish** — `publicar_dados.py` copies JSONs to `pipeline/dados_publicos/` and `git push` to GitHub
5. **Website** — HTML/JS pages read data directly from `raw.githubusercontent.com` (no Netlify deploy per update)

## ⚙️ Configuration

Edit `pipeline/config.json`:
- `dados_publicos_repo` — URL do repo público no GitHub (já configurado)
- `host`/`ambiente` — muda para `resultados.tse.jus.br` / `oficial` quando o TSE publicar o ambiente real
- `eleicoes_por_cargo` — mapeamento de códigos por cargo

## 🛠️ Common commands

| Command | What it does |
|---------|-------------|
| `python pipeline/update.py --ciclo ele2026` | Full cycle (download → publish) |
| `python pipeline/update.py --mock --no-push` | Generate mock data, skip GitHub push |
| `python pipeline/update.py --turno 2` | Second turno: generates `live-2t.json` / `historico-2t.json` |
| `python pipeline/publicar_dados.py --configurar` | First-time: clone empty public repo into `pipeline/dados_publicos/` |
| `python pipeline/update.py --mock` | Run full publish flow with mock data (incl. GitHub push) |

## 📁 Key directories

| Directory | Purpose |
|-----------|---------|
| `pipeline/dados_baixados/` | arquivos brutos baixados do TSE |
| `pipeline/dados_publicos/` | clone do repo público no GitHub (live.json, historicos, status) |
| `pipeline/site/` | cópia de trabalho: `live.json` + `status.json` (alimenta o site) |

## ⚠️ Known notes

- **~110/248 files may 404** when running against the TSE simulator (Sep 2026 window). This is expected — the simulation doesn't have all municipal files yet. 138 of 248 typically succeed.
- **`pipeline/site/` must exist** and contain `live.json`; otherwise `update.py` crashes writing `status.json`. Run `mkdir -p pipeline/site` if fresh setup.
- **`--no-push` only skips the GitHub push** — TSE download and aggregate still run.
- **Second turno (`--turno 2`) is isolated** — only affects `live-2t.json` / `historico-2t.json`; 1st turno files are untouched.
- **Sanidade validation** enforces monotonic votos/sections. Use `--forcar` only after reviewing the reported problemas.

## 🔗 Output

After publishing, pages read data from:
```
https://deniogatha.github.io/painel-eleicoes-2026-dados/
```
(or whatever `netlify_url` is set to in `config.json`).

Dados também disponíveis em `raw.githubusercontent.com/ratitu/painel-eleicoes-2026-dados-dados-publicos/main/live.json`.