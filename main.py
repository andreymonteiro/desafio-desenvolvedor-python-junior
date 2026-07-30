import argparse
import logging
import os
from datetime import datetime

from leitor import ler_dependencias
from pypi_api import consultar_pypi
from snyk_scraper import criar_driver, consultar_snyk
from relatorio import gerar_relatorio

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"logs/execucao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Analisa dependências de um projeto Python")
    parser.add_argument("arquivo", help="Caminho do requirements.txt ou pyproject.toml")
    parser.add_argument("--saida", default="relatorio.xlsx", help="Nome do arquivo de saída")
    args = parser.parse_args()

    logger.info(f"Lendo dependências de {args.arquivo}")
    dependencias = ler_dependencias(args.arquivo)
    logger.info(f"{len(dependencias)} dependências encontradas")

    driver = criar_driver()
    resultados = []

    try:
        for dep in dependencias:
            nome = dep["nome"]
            logger.info(f"Consultando {nome}")

            pypi_info = consultar_pypi(nome)
            snyk_info = consultar_snyk(driver, nome)

            resultados.append({
                "nome": nome,
                "versao": dep.get("versao") or pypi_info.get("versao"),
                "licenca": pypi_info.get("licenca"),
                "data_publicacao": pypi_info.get("data_publicacao"),
                "score": snyk_info.get("score"),
                "vulnerabilidades": snyk_info.get("vulnerabilidades"),
            })
    finally:
        driver.quit()

    gerar_relatorio(resultados, args.saida)
    logger.info(f"Relatório salvo em {args.saida}")


if __name__ == "__main__":
    main()
