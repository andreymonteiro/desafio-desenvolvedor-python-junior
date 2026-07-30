from snyk_scraper import criar_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = criar_driver(headless=True)
driver.get("https://security.snyk.io/package/pip/requests")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

texto = driver.find_element(By.TAG_NAME, "body").text

with open("diagnostico_snyk.txt", "w", encoding="utf-8") as f:
    f.write(texto)

driver.quit()
print("Texto salvo em diagnostico_snyk.txt")