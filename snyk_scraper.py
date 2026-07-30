import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logger = logging.getLogger(__name__)


def criar_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = "eager"  # não espera imagens/analytics carregarem, só o essencial do DOM
    # ADICIONADO: User-Agent para o Snyk não detectar o Selenium como Robô/Bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)


def consultar_snyk(driver, pacote):
    # Acessa diretamente a URL do pacote no PIP (muito mais rápido e evita a página de busca)
    url = f"https://security.snyk.io/package/pip/{pacote}"
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Em vez de tentar adivinhar a classe CSS exata (que muda com frequência
        # em apps React), busco o padrão de texto "NN/100" que o Snyk sempre mostra.
        texto_pagina = driver.find_element(By.TAG_NAME, "body").text
        texto_normalizado = re.sub(r"\s+", " ", texto_pagina)

        score = None
        match_score = re.search(r"(\d{1,3})\s*/\s*100", texto_normalizado)
        if match_score:
            score = int(match_score.group(1))

        vulnerabilidades = None
        if "No known security issues" in texto_normalizado or "No direct vulnerabilities" in texto_normalizado:
            vulnerabilidades = 0
        else:
            match_vuln = re.search(r"(\d+)\s+vulnerabilit", texto_normalizado, re.IGNORECASE)
            if match_vuln:
                vulnerabilidades = int(match_vuln.group(1))

        if score is None:
            logger.warning(f"Não consegui achar o score de {pacote} no Snyk")
            return {"nome": pacote, "encontrado": False, "score": None, "vulnerabilidades": None}

        return {"nome": pacote, "encontrado": True, "score": score, "vulnerabilidades": vulnerabilidades}

    except TimeoutException:
        logger.error(f"Timeout ao buscar {pacote} no Snyk")
        return {"nome": pacote, "encontrado": False, "score": None, "vulnerabilidades": None}
    except WebDriverException as e:
        logger.error(f"Erro do Selenium para {pacote}: {e}")
        return {"nome": pacote, "encontrado": False, "score": None, "vulnerabilidades": None}