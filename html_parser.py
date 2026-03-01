from bs4 import BeautifulSoup
import os


for aule_periodo in os.listdir("aule_pages"):

    print(f"Parsing {aule_periodo}...")

    output_dir = f"aule_parsed/{aule_periodo}/"
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    subfolder = f"aule_pages/{aule_periodo}"
    for file_aula in os.listdir(subfolder):

        print(f"Parsing {file_aula}...")

        file_path = f"{subfolder}/{file_aula}"
        with open(file_path, 'r') as f:
            html_doc = f.read()


        soup = BeautifulSoup(html_doc, 'html.parser')

        # Find by class
        rows = soup.find_all("tr", class_="normalRow")

        with open(f"{output_dir}/{file_aula.removesuffix('.html')}.csv", 'w') as f:
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

                #print(f"rowspan: `{rowspan}`, typeof{type(rowspan)}")
                data = data_column.text.strip()

                if data == '':
                    print(f"Error: empty data in file {file_path}, row: {row}. Aborting")
                    exit()

                slots = []

                for column in columns[2:]:
                    col_classes = column.get("class")
                    if "slot" in col_classes:
                        span_15_minutes = column.get("colspan")

                        slots.append((column.text.strip(), span_15_minutes))
                    else:
                        slots.append(("", 1))

                slots_str = '£'.join([f"{evento}%{span}" for evento, span in slots])
                f.write(f"{data}£{slots_str}$")
