from bs4 import BeautifulSoup


subfolder = "aule_pages/leo_11_Aprile_2024-15_Aprile_2024"

#file_path = f"{subfolder}/2.0.2_300.html"
#file_path = f"{subfolder}/2.0.1_307.html"
#file_path = f"{subfolder}/26.1.6_167.html"
#file_path = "26.1.6_frombrowser.html"
file_path = "aule_pages/bovisa_5_Aprile_2025-9_Aprile_2025/L.02_112.html"
with open(file_path, 'r') as f:
    html_doc = f.read()


soup = BeautifulSoup(html_doc, 'html.parser')

# Find by class
rows = soup.find_all("tr", class_="normalRow")

skip_next_rows = 0
for i, row in enumerate(rows[1:]):
    print(f"Processing row {i}...")
    if skip_next_rows > 0:
        print(f"Skipping row {i} due to rowspan")
        skip_next_rows -= 1
        continue

    columns = row.contents
    data_column = columns[0]
    rowspan = data_column.get("rowspan")

    if rowspan is not None:
        rowspan = int(rowspan)
        if rowspan > 1:
            skip_next_rows = rowspan - 1
            print(f"Found rowspan of {rowspan} in row {i}, will skip next {skip_next_rows} rows")

    print(f"rowspan: `{rowspan}`, typeof{type(rowspan)}")
    data = data_column.text.strip()

    if data == '':
        print(f"Error: empty data in file {file_path}, row: {row}. Aborting")
        exit()

    #print(columns[2:], len(columns[2:]))

    slots = []

    for column in columns[2:]:
        col_classes = column.get("class")
        if "slot" in col_classes:
            span_15_minutes = column.get("colspan")
            #print((column.text.strip(), span_15_minutes))

            slots.append((column.text.strip(), span_15_minutes))
        else:
            slots.append(("", 1))

    slots_str = ';'.join([f"{evento}%{span}" for evento, span in slots])
    print(f"Slots: {len(slots)}", f"{data};{slots_str}\n")
