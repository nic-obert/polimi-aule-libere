from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import os


FROM_DAY = "11"
TO_DAY = "15"
FROM_MESE = "Aprile"
TO_MESE = "Aprile"
FROM_ANNO = "2024"
TO_ANNO = "2024"


URL_RICERCA_LEO = "https://onlineservices.polimi.it/spazi/spazi/controller/RicercaAula.do?spazi___model___formbean___RicercaAvanzataAuleVO___postBack=true&spazi___model___formbean___RicercaAvanzataAuleVO___formMode=FILTER&spazi___model___formbean___RicercaAvanzataAuleVO___sede=MIA&spazi___model___formbean___RicercaAvanzataAuleVO___sigla=&spazi___model___formbean___RicercaAvanzataAuleVO___categoriaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___tipologiaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___iddipScelto=tutti&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseElettriche_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseDiRete_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloAllDidInnovativa_default=N&evn_ricerca_avanzata=Ricerca+aula"
URL_RICERCA_BOVISA = "https://onlineservices.polimi.it/spazi/spazi/controller/RicercaAula.do?spazi___model___formbean___RicercaAvanzataAuleVO___postBack=true&spazi___model___formbean___RicercaAvanzataAuleVO___formMode=FILTER&spazi___model___formbean___RicercaAvanzataAuleVO___sede=MIB&spazi___model___formbean___RicercaAvanzataAuleVO___sigla=&spazi___model___formbean___RicercaAvanzataAuleVO___categoriaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___tipologiaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___iddipScelto=tutti&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseElettriche_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseDiRete_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloAllDidInnovativa_default=N&evn_ricerca_avanzata=Ricerca+aula"

driver = webdriver.Firefox()

driver.get(URL_RICERCA_LEO)

AULE_TABLE_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/div[2]/table/tbody"

aule_table = driver.find_element(By.XPATH, AULE_TABLE_XPATH)

aule_rows = aule_table.find_elements(By.TAG_NAME, "tr")

aule = []

for aula_row in aule_rows:
    columns = aula_row.find_elements(By.TAG_NAME, "td")
    nome_aula = columns[1].text
    dettagli_aula_href = columns[2].find_element(By.TAG_NAME, "a").get_attribute("href")
    #print(nome_aula, dettagli_aula_href)
    aule.append((nome_aula, dettagli_aula_href))

VISUALIZZA_ORARI_BUTTON_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/form/button"

for nome_aula, url_aula in aule:
    driver.get(url_aula)

    # Select the time window

    CAPIENZA_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/div/div[1]/table/tbody/tr[5]/td[1]"
    capienza_str: str = driver.find_element(By.XPATH, CAPIENZA_XPATH).text
    capienza = capienza_str.removeprefix("Capienza").strip()

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

        dir_name = f"html_aule_leo_{FROM_DAY}_{FROM_MESE}_{FROM_ANNO}-{TO_DAY}_{TO_MESE}_{TO_ANNO}"
        file_name = f"{dir_name}/{nome_aula}_{capienza}.html"
        # Create the directory if it doesn't exist
        os.makedirs(dir_name, exist_ok=True)
        print(f"Saving {file_name}...")
        with open(file_name, 'w') as f:
            f.write(driver.page_source)

    except NoSuchElementException:
        print(f"Could not find time window selectors for {nome_aula}, skipping...")



#input("Press enter to close >")

driver.close()
