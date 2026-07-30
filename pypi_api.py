import logging
import requests

logger = logging.getLogger(__name__)


def consultar_pypi(pacote):
    url = f"https://pypi.org/pypi/{pacote}/json"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            return {"nome": pacote, "encontrado": False}

        resp.raise_for_status()
        data = resp.json()
        info = data.get("info", {})
        versao = info.get("version")
        releases = data.get("releases", {}).get(versao, [])
        data_publicacao = releases[0]["upload_time_iso_8601"] if releases else None

        licenca = info.get("license") or None
        if licenca and len(licenca) > 50:
            licenca = licenca.strip().splitlines()[0][:50] + "..."

        return {
            "nome": pacote,
            "encontrado": True,
            "resumo": info.get("summary"),
            "licenca": licenca,
            "versao": versao,
            "data_publicacao": data_publicacao,
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao consultar PyPI para {pacote}: {e}")
        return {"nome": pacote, "encontrado": False}