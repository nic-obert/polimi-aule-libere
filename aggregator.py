import os
import json


USABLE_SLOT_THRESHOLD_MINUTES = 180
MAX_DURATA_ESAME = 180

SABATO_ORARIO_INIZIO_MINUTES = 9*60
SABATO_ORARIO_FINE_MINUTES = 17*60+15
WEEKDAY_ORARIO_FINE_MINUTES = 18*60+15

MIN_CAPIENZA = 60


output_dir = "aggregated"

summary = {
    'parametri': {
        'MIN_DURATA_ESAME': USABLE_SLOT_THRESHOLD_MINUTES,
        'MAX_DURATA_ESAME': MAX_DURATA_ESAME,
        'ORARIO_SETTIMANA': f"8:00-{WEEKDAY_ORARIO_FINE_MINUTES//60}:{WEEKDAY_ORARIO_FINE_MINUTES%60:0>2}",
        'ORARIO_SABATO': f"{SABATO_ORARIO_INIZIO_MINUTES//60}:{SABATO_ORARIO_INIZIO_MINUTES%60:0>2}-{SABATO_ORARIO_FINE_MINUTES//60}:{SABATO_ORARIO_FINE_MINUTES%60:0>2}",
        'MIN_CAPIENZA': MIN_CAPIENZA
    }
}

for aule_periodo in os.listdir("aule_parsed"):

    print(f"Aggregating {aule_periodo}...")

    if aule_periodo.startswith("leo"):
        campus_name = "leo"
    else:
        campus_name = "bovisa"

    giorni = {}

    subfolder = f"aule_parsed/{aule_periodo}"
    for file_aula in os.listdir(subfolder):


        nome_aula, capienza = file_aula.removesuffix('.csv').split('_')

        if int(capienza) < MIN_CAPIENZA:
            print(f"Skipping {file_aula} due to insufficient capacity ({capienza} < {MIN_CAPIENZA})")
            continue

        print(f"Aggregating {file_aula}...")

        file_path = f"{subfolder}/{file_aula}"
        with open(file_path, 'r') as f:

            for line in f.read().split('$'):
                if line.strip() == '':
                    continue

                columns = line.split('£')
                data = columns[0]

                if data.startswith('Dom'):
                    continue
                if data == '':
                    print(f"Error: empty data in file {subfolder}/{file_aula}, line: {line}")

                slots = []
                # Also merge empty contiguous slots
                current_empty_span = None
                orario_minuti = 8*60
                for slot in columns[1:]:
                    try:

                        evento, span_str = slot.split('%')
                        span = int(span_str) * 15 # Convert from number of 15-minute slots to minutes

                        #slots.append({'evento': evento, 'span': span_15_minutes})
                        if current_empty_span is None:
                            if evento == '':
                                current_empty_span = span
                            else:
                                slots.append({'evento': evento, 'inizio': f"{orario_minuti//60}:{orario_minuti%60:0>2}", 'fine': f"{(orario_minuti+span)//60}:{(orario_minuti+span)%60:0>2}", 'span': span})
                        else:
                            if evento == '':
                                current_empty_span += span
                            else:
                                slots.append({'evento': '', 'inizio': f"{(orario_minuti-current_empty_span)//60}:{(orario_minuti-current_empty_span)%60:0>2}", 'fine': f"{orario_minuti//60}:{orario_minuti%60:0>2}", 'span': current_empty_span})
                                slots.append({'evento': evento, 'inizio': f"{orario_minuti//60}:{orario_minuti%60:0>2}", 'fine': f"{(orario_minuti+span)//60}:{(orario_minuti+span)%60:0>2}", 'span': span})
                                current_empty_span = None

                        orario_minuti += span

                    except ValueError:
                        print(f"Could not parse slot '{slot}' in file {file_aula}, line: {line}, skipping...")

                if current_empty_span is not None:
                    slots.append({'evento': '', 'inizio': f"{(orario_minuti-current_empty_span)//60}:{(orario_minuti-current_empty_span)%60:0>2}", 'fine': f"{orario_minuti//60}:{orario_minuti%60:0>2}", 'span': current_empty_span})


                n_available_slots = 0
                n_good_slots = 0
                for slot in slots:

                    inizio = int(slot['inizio'].split(':')[0]) * 60 + int(slot['inizio'].split(':')[1])
                    fine = int(slot['fine'].split(':')[0]) * 60 + int(slot['fine'].split(':')[1])
                    span: int = slot['span']
                    evento: str = slot['evento']

                    if data.startswith('Sab'):
                        if evento == '' and span >= USABLE_SLOT_THRESHOLD_MINUTES:
                            n_available_slots += span // MAX_DURATA_ESAME
                            if fine - USABLE_SLOT_THRESHOLD_MINUTES >= SABATO_ORARIO_INIZIO_MINUTES and inizio + USABLE_SLOT_THRESHOLD_MINUTES <= SABATO_ORARIO_FINE_MINUTES:
                                n_good_slots += (min(fine, SABATO_ORARIO_FINE_MINUTES) - max(inizio, SABATO_ORARIO_INIZIO_MINUTES)) // MAX_DURATA_ESAME
                    else: # Weekday
                        if evento == '' and span >= USABLE_SLOT_THRESHOLD_MINUTES:
                            n_available_slots += span // MAX_DURATA_ESAME
                            if inizio + USABLE_SLOT_THRESHOLD_MINUTES <= WEEKDAY_ORARIO_FINE_MINUTES:
                                n_good_slots += (min(fine, WEEKDAY_ORARIO_FINE_MINUTES) - inizio) // MAX_DURATA_ESAME


                info_obj = {'aula': nome_aula, 'cap': capienza, f'slot_liberi>={USABLE_SLOT_THRESHOLD_MINUTES}': n_available_slots, 'slot_liberi_preferibili': n_good_slots, 'slots': slots}
                info_giorno = giorni.get(data)
                if info_giorno is not None:
                    info_giorno[f'slot_liberi>={USABLE_SLOT_THRESHOLD_MINUTES}'] += n_available_slots
                    info_giorno['slot_liberi_preferibili'] += n_good_slots
                    info_giorno['aule'].append(info_obj)
                else:
                    giorni[data] = { f'slot_liberi>={USABLE_SLOT_THRESHOLD_MINUTES}': n_available_slots, 'slot_liberi_preferibili': n_good_slots, 'aule': [info_obj] }

    with open(f"{output_dir}/{aule_periodo}.json", 'w') as f:
        f.write(json.dumps(giorni, indent=2))


    for info in giorni.values():
        del info['aule']
    campus_summary = summary.get(campus_name)
    if campus_summary is None:
        summary[campus_name] = giorni
    else:
        campus_summary.update(giorni)


with open(f"{output_dir}/summary.json", 'w') as f:
    f.write(json.dumps(summary, indent=2))
