from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


FROM_DAY = "1"
TO_DAY = "30"
FROM_MESE = "Marzo"
TO_MESE = "Aprile"
FROM_ANNO = "2026"
TO_ANNO = "2026"


URL_RICERCA_LEO = "https://onlineservices.polimi.it/spazi/spazi/controller/RicercaAula.do?spazi___model___formbean___RicercaAvanzataAuleVO___postBack=true&spazi___model___formbean___RicercaAvanzataAuleVO___formMode=FILTER&spazi___model___formbean___RicercaAvanzataAuleVO___sede=MIA&spazi___model___formbean___RicercaAvanzataAuleVO___sigla=&spazi___model___formbean___RicercaAvanzataAuleVO___categoriaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___tipologiaScelta=tutte&spazi___model___formbean___RicercaAvanzataAuleVO___iddipScelto=tutti&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseElettriche_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloPreseDiRete_default=N&spazi___model___formbean___RicercaAvanzataAuleVO___soloAllDidInnovativa_default=N&evn_ricerca_avanzata=Ricerca+aula"

#DETTAGLI_AULA_BASE = "https://onlineservices.polimi.it/spazi/spazi/controller/"

driver = webdriver.Firefox()

driver.get("https://onlineservices.polimi.it/spazi/spazi/controller/Aula.do;jsessionid=aaamVFKF0-EVndVxo65Vz;jsessionid=aaamVFKF0-EVndVxo65Vz?evn_init=event&idaula=32&jaf_currentWFID=main")

CAPIENZA_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/div/div[1]/table/tbody/tr[5]/td[1]"
capienza_str: str = driver.find_element(By.XPATH, CAPIENZA_XPATH).text
capienza = capienza_str.removeprefix("Capienza").strip()
print(f"'{capienza}'")

driver.close()
exit()

# Select the time window

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


VISUALIZZA_ORARI_BUTTON_XPATH = "/html/body/div[1]/table[1]/tbody/tr/td[2]/form/button"

driver.find_element(By.XPATH, VISUALIZZA_ORARI_BUTTON_XPATH).click()

with open("p.html", 'w') as f:
    f.write(driver.page_source)


input("Press enter to close >")

driver.close()
