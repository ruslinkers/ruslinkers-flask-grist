from grist_api import GristDocAPI

SERVER = "https://grist.cucurri.ru"
DOC_ID = "sPb2VvqpDspMzd7j1ZMtJD"

api = GristDocAPI(DOC_ID, server=SERVER)

# Main table with data
linkers = {x.id : x for x in api.fetch_table('Linkers')}

# Semantic field info
semfields = {x.id : x for x in api.fetch_table('Semfields')}
subfields = {x.id : x for x in api.fetch_table('Subfields')}

# Values for parameters
val_parts_num = {x.id : x for x in api.fetch_table('Parts_num_values')}
val_parts_order = {x.id : x for x in api.fetch_table('Parts_order_values')}
val_linker_position = {x.id : x for x in api.fetch_table('Linker_position_values')}
val_linker_position_exclusivity = {x.id : x for x in api.fetch_table('Linker_position_exclusivity_values')}
val_correl_oblig = {x.id : x for x in api.fetch_table('Correl_oblig_values')}
val_correl_position = {x.id : x for x in api.fetch_table('Correl_position_values')}
val_clause_order = {x.id : x for x in api.fetch_table('Clause_order_values')}
val_indep_sentence = {x.id : x for x in api.fetch_table('Indep_sentence_values')}

# Dictionary stuff
meanings = {x.id : x for x in api.fetch_table('Meanings')}
sources = {x.id : x for x in api.fetch_table('Sources')}

import csv
# Generate the dictionary of lists of dictionaries, for diachronic db
diachronic = { }
with open('ruslinkers-dia-1.0.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        modforms = row['modern_form'].split('; ')
        for form in modforms:
            diachronic.setdefault(form, []).append(row)

# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     Base.metadata.create_all(bind=engine)