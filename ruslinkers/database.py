from grist_api import GristDocAPI

SERVER = "https://grist.cucurri.ru"
DOC_ID = "sPb2VvqpDspMzd7j1ZMtJD"

api = GristDocAPI(DOC_ID, server=SERVER)

# Main table with data
linkers = api.fetch_table('Linkers')

# Semantic field info
semfields = api.fetch_table('Semfields')
subfields = api.fetch_table('Subfields')

# Values for parameters
def make_param(param):
    return api.fetch_table(param)

param_values = {
    'parts_num': make_param('Parts_num_values'),
    'parts_order': make_param('Parts_order_values'),
    'linker_position': make_param('Linker_position_values'),
    'linker_position_exclusivity': make_param('Linker_position_exclusivity_values'),
    'correl_oblig': make_param('Correl_oblig_values'),
    'correl_position': make_param('Correl_position_values'),
    'clause_order': make_param('Clause_order_values'),
    'indep_sentence': make_param('Indep_sentence_values')
}

# Dictionary stuff
meanings = api.fetch_table('Meanings')
sources = api.fetch_table('Sources')

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