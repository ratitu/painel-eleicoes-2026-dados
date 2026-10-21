# -*- coding: utf-8 -*-
"""
Mock data generator for testing the painel eleicoes 2026 pipeline.
Generates fictional election data for the TSE simulator environment.
"""
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "dados_baixados")
LIVE_OUT = os.path.join(HERE, "site", "live.json")

def main():
    """Gera dados mock para teste do pipeline."""
    import hashlib
    import json as _json
    from datetime import datetime, timezone

    HERE = os.path.dirname(os.path.abspath(__file__))
    SRC = os.path.join(HERE, "dados_baixados")
    LIVE_OUT = os.path.join(HERE, "site", "live.json")

    # Garante que o diretorio site existe
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)

    # Le os cargos e UFs do config.json
    try:
        with open(os.path.join(HERE, "config.json"), encoding="utf-8") as f:
            cfg = _json.load(f)
        eleicoes_por_cargo = cfg.get("eleicoes_por_cargo", {
            "0001": "6257", "0003": "6259", "0005": "6259",
            "0006": "6259", "0007": "6259", "0008": "6259"
        })
    except Exception:
        eleicoes_por_cargo = {
            "0001": "6257", "0003": "6259", "0005": "6259",
            "0006": "6259", "0007": "6259", "0008": "6259"
        }

    # UFs disponiveis
    ufs = cfg.get("ufs", [
        "ac","al","am","ap","ba","ce","df","es","go","ma","mg","ms","mt","pa",
        "pb","pe","pi","pr","rj","rn","ro","rr","rs","sc","se","sp","to"
    ])

    # Gera dados mock para cada cargo
    bundle = {
        "meta": {
            "geradoEm": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fonte": "mock_data (ver tse_downloader.py)",
            "turno": 1
        },
        "ufNomes": {},
        "cargoNomes": {
            "0001": "Presidente",
            "0003": "Governador",
            "0005": "Senador",
            "0006": "Deputado Federal",
            "0007": "Deputado Estadual",
            "0008": "Deputado Distrital",
            "0025": "Conselheiro Distrital"
        },
        "partidoNomes": {
            "PL": "PARTIDO LIBERAL", "PSD": "PARTIDO SOCIAL DEMOCRÁTICO",
            "PT": "PARTIDO DOS TRABALHADORES", "DC": "DEMOCRACIA CRISTÃ",
            "PCB": "PARTIDO COMUNISTA BRASILEIRO", "PSTU": "PARTIDO SOCIALISTA DOS TRABALHADORES UNIFICADO",
            "AVANTE": "AVANTE", "NOVO": "Partido Novo", "UP": "UNIDADE POPULAR",
            "DEMOCRATA": "DEMOCRATA", "MISSÃO": "PARTIDO MISSÃO", "PCO": "PARTIDO DA CAUSA OPERÁRIA",
            "PP": "PROGRESSISTAS", "AGIR": "AGIR", "REPUBLICANOS": "REPUBLICANOS",
            "PSB": "PARTIDO SOCIALISTA BRASILEIRO", "PSDB": "PARTIDO DA SOCIAL DEMOCRACIA BRASILEIRA",
            "MDB": "MOVIMENTO DEMOCRÁTICO BRASILEIRO", "UNIÃO": "UNIÃO BRASIL",
            "REDE": "REDE SUSTENTABILIDADE", "MOBILIZA": "MOBILIZAÇÃO NACIONAL",
            "PSOL": "PARTIDO SOCIALISMO E LIBERDADE", "PRTB": "PARTIDO RENOVADOR TRABALHISTA BRASILEIRO",
            "PDT": "PARTIDO DEMOCRÁTICO TRABALHISTA", "PRD": "PARTIDO DEMOCRACIA DEMOCRÁTICA",
            "PODE": "PODEMOS", "SOLIDARIEDADE": "SOLIDARIEDADE", "CIDADANIA": "CIDADANIA",
            "PV": "PARTIDO VERDE", "PCDOB": "PARTIDO COMUNISTA DO BRASIL", "S/PARTIDO": "S/PARTIDO"
        },
        "partidoList": list(set([
            "PL", "PSD", "PT", "DC", "PCB", "PSTU", "AVANTE", "NOVO", "UP",
            "DEMOCRATA", "MISSÃO", "PCO", "PP", "AGIR", "REPUBLICANOS",
            "PSB", "PSDB", "MDB", "UNIÃO", "REDE", "MOBILIZA", "PSOL",
            "PRTB", "PDT", "PRD", "PODE", "SOLIDARIEDADE", "CIDADANIA", "PV",
            "PCDOB", "S/PARTIDO"
        ])),
        "scopeStats": {}
    }

    # Preencher ufNomes
    uf_nomes_map = {
        "ac": "Acre", "al": "Alagoas", "am": "Amazonas", "ap": "Amapá",
        "ba": "Bahia", "ce": "Ceará", "df": "Distrito Federal",
        "es": "Espírito Santo", "go": "Goiás", "ma": "Maranhão",
        "mg": "Minas Gerais", "ms": "Mato Grosso do Sul", "mt": "Mato Grosso",
        "pa": "Pará", "pb": "Paraíba", "pe": "Pernambuco", "pi": "Piauí",
        "pr": "Paraná", "rj": "Rio de Janeiro", "rn": "Rio Grande do Norte",
        "ro": "Rondônia", "rr": "Roraima", "rs": "Rio Grande do Sul",
        "sc": "Santa Catarina", "se": "Sergipe", "sp": "São Paulo", "to": "Tocantins"
    }
    bundle["ufNomes"] = uf_nomes_map

    # Adicionar estatísticas de scope (seções e votos) para cada cargo
    import random
    random.seed(42)  # Reprodutível
    for cargo_cod in eleicoes_por_cargo:
        cargo_nome = cfg.get("cargos_interesse", {}).get(cargo_cod, cargo_cod)
        bundle["cargoNomes"][cargo_cod] = cargo_nome
        scope_stats = {}
        for uf in ufs:
            n_secoes = random.randint(200, 8000)
            n_votos_validos = random.randint(max(1, n_secoes - 100), n_secoes)
            pst = round(random.uniform(40, 92), 1)
            scope_stats[uf] = {
                "st": n_secoes,
                "vv": n_votos_validos,
                "pst": pst
            }
        bundle["scopeStats"][cargo_cod] = scope_stats

    # Escreve live.json
    LIVE_OUT = os.path.join(HERE, "site", "live.json")
    with open(LIVE_OUT, "w", encoding="utf-8") as fh:
        _json.dump(bundle, fh, ensure_ascii=False, separators=(",", ":"))

    print("live.json gerado em:", LIVE_OUT)
    mb = os.path.getsize(LIVE_OUT) / 1e6
    print(" (%.2f MB)" % mb)

    # Print summary por cargo
    for cargo_cod in eleicoes_por_cargo:
        n = len(bundle.get("scopeStats", {}).get(cargo_cod, {}))
        print("  ", cargo_nome, "-", n, "areas")

    return 0


if __name__ == "__main__":
    sys.exit(main())