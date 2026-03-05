import requests as r
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


# Periodo campione
FROM_DAY = "1"
FROM_MESE = "Marzo"
FROM_ANNO = "2026"
TO_DAY = "31"
TO_MESE = "Marzo"
TO_ANNO = "2026"


URL_RICERCA_AULA = "https://onlineservices.polimi.it/spazi/spazi/controller/Aula.do?evn_ricerca_aula=evento&jaf_currentWFID=main"
URL_AULE_DIDATTICA_PLATEA_FRONTALE_LEO = "https://onlineservices.polimi.it/spazi/spazi/controller/RicercaAula.do?spazi___model___formbean___RicercaAvanzataAuleVO___postBack=true&spazi___model___formbean___RicercaAvanzataAuleVO___formMode=FILTER&spazi___model___formbean___RicercaAvanzataAuleVO___sede=MIA&spazi___model___formbean___RicercaAvanzataAuleVO___sigla=&spazi___model___formbean___RicercaAvanzataAuleVO___categoriaScelta=D&spazi___model___formbean___RicercaAvanzataAuleVO___tipologiaScelta=F&spazi___model___formbean___RicercaAvanzataAuleVO___iddipScelto=tutti&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseElettriche_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseDiRete_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloAllDidInnovativa_default=N&evn_ricerca_avanzata=Ricerca+aula"

URL_BASE_AULE_CONTROLLER = "https://onlineservices.polimi.it/spazi/spazi/controller/"

URL_ORARIO_AULA_BASE = "https://onlineservices.polimi.it/spazi/spazi/controller/Aula.do"

VISUALIZZA_ORARI_BUTTON_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/form/button"


res = r.get(URL_AULE_DIDATTICA_PLATEA_FRONTALE_LEO)

page_html = res.text

soup = BeautifulSoup(page_html, 'html.parser')

tabella_aule = soup.find("tbody", class_="TableDati-tbody")

aule = []
for row in tabella_aule.find_all("tr"):
    columns = row.find_all("td")
    nome_aula = columns[1].text.strip()
    href = columns[2].find("a").get("href")
    #print(nome_aula.text, href)
    aule.append((nome_aula, href.strip()))


driver = webdriver.Firefox()


for nome_aula, href in aule:

    url_info_aula = URL_BASE_AULE_CONTROLLER + href

    pquery = urlparse(url_info_aula).query.split("&")
    for param in pquery:
        name, value = param.split("=")
        if name == 'idaula':
            id_aula = value
            break
    else:
        print(f"Error: id aula not found in url {url_info_aula}. Aborting")
        exit()


    #print(f"GET {url_info_aula}")
    driver.get(url_info_aula)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    tabella_allestimenti = soup.select("#aula_xproprietaPubblicabili_auleColl > tbody")[0]

    cablata = False
    for row in tabella_allestimenti.find_all("tr"):
        columns = row.find_all("td")
        nome_allestimento = columns[1].text.strip()
        valore_allestimento = columns[2].text.strip()
        if "presa elettrica" in nome_allestimento and valore_allestimento == "SI":
            cablata = True
            break

    if not cablata:
        try:
            from_day_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___fromData_day"))
            from_day_select.select_by_value(FROM_DAY)

            to_day_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___toData_day"))
            to_day_select.select_by_value(TO_DAY)

            from_mese_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___fromData_month"))
            from_mese_select.select_by_visible_text(FROM_MESE)

            to_mese_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___toData_month"))
            to_mese_select.select_by_visible_text(TO_MESE)

            from_anno_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___fromData_year"))
            from_anno_select.select_by_value(FROM_ANNO)

            to_anno_select = Select(driver.find_element(By.ID, "spazi___model___formbean___DateOccupazForm___toData_year"))
            to_anno_select.select_by_value(TO_ANNO)

            driver.find_element(By.XPATH, VISUALIZZA_ORARI_BUTTON_XPATH).click()

            with open(f"pages/{nome_aula}.html", 'w') as f:
                print(f"Saving {nome_aula}.html...")
                f.write(driver.page_source)

        except NoSuchElementException as e:
            print(f"Could not find time window selectors for {nome_aula}, ({e}) skipping...")


driver.close()
