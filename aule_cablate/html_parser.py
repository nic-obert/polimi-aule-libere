from bs4 import BeautifulSoup
import os



aule = []

for file_aula in os.listdir("pages"):

    print(f"Parsing {file_aula}...")

    nome_aula = file_aula.removesuffix(".html")

    file_path = f"pages/{file_aula}"
    with open(file_path, 'r') as f:
        html_doc = f.read()


    soup = BeautifulSoup(html_doc, 'html.parser')

    # Find by class
    rows = soup.find_all("tr", class_="normalRow")

    totale_utilizzo = 0

    # Skip the first row of the table, we don't need the header
    skip_next_rows = 0
    for row in rows[1:]:

        if skip_next_rows > 0:
            skip_next_rows -= 1
            continue

        columns = row.contents
        data_column = columns[0]
        rowspan = data_column.get("rowspan")

        if rowspan is not None:
            rowspan = int(rowspan)
            if rowspan > 1:
                skip_next_rows = rowspan - 1


        for column in columns[2:]:
            col_classes = column.get("class")
            if "slot" in col_classes:
                span = int(column.get("colspan")) * 15 # Each slot is 15 minutes long
                totale_utilizzo += span


    aule.append((nome_aula, totale_utilizzo))


# Sort aule by totale_utilizzo in descending order
aule.sort(key=lambda x: x[1], reverse=True)


with open("aule_utilizzo.csv", 'w') as f_out:
    f_out.write("Aula,Totale Utilizzo (ore)\n")
    for nome_aula, totale_utilizzo in aule:
        f_out.write(f"{nome_aula},{totale_utilizzo//60}:{totale_utilizzo%60:0>2}\n")
