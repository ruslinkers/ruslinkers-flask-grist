import os

from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for, send_file

from urllib.parse import quote_plus,unquote_plus

import markdown
# import jinja2
from markupsafe import Markup

import operator

# from ruslinkers.database import db_session, diachronic
# from ruslinkers.models import *
import ruslinkers.database as db

def quote_lnk(u):
    return quote_plus(u.replace('/','$'))
def unquote_lnk(u):
    return unquote_plus(u).replace('$','/')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
        # DATABASE=os.path.join(app.instance_path, 'ruslinkers-new4.db'),
    )

    md = markdown.Markdown(extensions=['meta'])
    app.jinja_env.filters['quote_lnk'] = quote_lnk
    app.jinja_env.filters['unquote_lnk'] = unquote_lnk
    app.jinja_env.filters['markdown'] = lambda text: Markup(md.convert(text))

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/oss-connectors/<path:path>', methods=['GET'])
    def oss_connectors(path):
        # return send_file(url_for('static', filename='oss-connectors-r/_site/' + path))
        return app.send_static_file('oss-connectors-r/_site/' + path)
    
    @app.route('/bezhta-connectors/<path:path>', methods=['GET'])
    def bezhta_connectors(path):
        # return send_file(url_for('static', filename='oss-connectors-r/_site/' + path))
        return app.send_static_file('bezhta-connectors-r/_site/' + path)    
    
    @app.route('/uralic-connectors/<path:path>', methods=['GET'])
    def uralic_connectors(path):
        # return send_file(url_for('static', filename='oss-connectors-r/_site/' + path))
        return app.send_static_file('fu-connectors-r/_site/' + path)    

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route('/participants', methods=['GET'])
    def participants():
        return render_template('participants.html')

    @app.route('/feedback', methods=['GET'])
    def feedback():
        return render_template('feedback.html')
    
    @app.route('/publications', methods=['GET'])
    def publications():
        return render_template('publications.html')    

    # show unit
    @app.route('/units', methods=['GET'])
    def units():
        # # Filter the units according to search request
        # stmt = db.select(Unit)
        # if request.args.get("search-pos") is not None:
        #     stmt = stmt.where(Meaning.pos == request.args.get("search-pos")).where(Meaning.unit_id == Unit.id)
        # if request.args.get("search-dict") is not None:
        #     # stmt = stmt.where(Source.id == request.args.get("search-dict"))
        #     stmt = stmt.where(sources_to_units.c.source_id == request.args.get("search-dict")).where(sources_to_units.c.unit_id == Unit.id)
        # if request.args.get("search-conn") is not None:
        #     stmt = stmt.where(Unit.linker == request.args.get("search-conn"))
        # if request.args.get("search-correl") is not None:
        #     stmt = stmt.where(FormType.keyword == 'correl').where(Form.formtype_id == FormType.id and Form.unit_id == Unit.id)

        units_gr = defaultdict(list)
        for u in db.linkers:
            units_gr[u.form].append(u)

        units_f = list(units_gr.keys())
        filters = dict()

        # Helper function to avoid writing too much code
        def process_filter(us, filter, func):
            if request.args.get(filter) is not None:
                filters[filter] = []
                filtered_values = []
                for f in request.args.getlist(filter):
                    filters[filter].append(f)
                    filtered_values = filtered_values + [k for k in us if func(f,k)]
                return list(dict.fromkeys(filtered_values))
            else: return us

        # Search by POS
        units_f = process_filter(units_f, 'search-pos', 
                        lambda f, k : any(f in x.pos_txt[1:] for x in units_gr[k]))
        # Search by dictionary
        units_f = process_filter(units_f, 'search-dict',
                        lambda f, k : any(int(f) in x.dicts[1:] for x in units_gr[k]))
        # Helper function to fetch meanings
        def get_meanings(l): 
                return [x.meaning for x in db.meanings if x.id in l.meanings[1:]]
        # Search by meaning text (in dict.)
        units_f = process_filter(units_f, 'search-meaning',
                        lambda f, k : any(f in str(x or '') 
                              for x in [z for y in [get_meanings(u) for u in units_gr[k]] for z in y]))
        # Search by linker text
        units_f = process_filter(units_f, 'search-conn',
                        lambda f, k : any(f in x 
                              for x in [y.form for y in units_gr[k]] + [z for y in [u.phonvars[1:] for u in units_gr[k]] for z in y]
                              ))
        # Search by (quasi-)correlate
        units_f = process_filter(units_f, 'search-correl',
                        lambda f, k : any(f in x 
                              for x in [y.correl for y in units_gr[k]]))
        # Search by example

        # Helper function to get all example values for a list of units
        get_examples = lambda l : [v for k,v in l._asdict().items() if 'example' in k and v not in ['','не засвидетельствовано']]

        units_f = process_filter(units_f, 'search-examples',
                        lambda f, k : any(f in x 
                                for x in [z for y in [get_examples(u) for u in units_gr[k]] for z in y]))

        # Search by semfield
        units_f = process_filter(units_f, 'search-semfield',
                        lambda f, k : any((int(f) == x.semfield1 or int(f) == x.semfield2) for x in units_gr[k]))

        # Search by subfield
        units_f = process_filter(units_f, 'search-subfield',
                        lambda f, k : any(int(f) in x.subfield1 for x in units_gr[k] if x.subfield1 is not None) 
                        or any(int(f) in x.subfield2 for x in units_gr[k] if x.subfield2 is not None))
        
        # Convert values to operators
        ops = {
            1: operator.not_,
            0: operator.truth
        }

        # Search inferential
        units_f = process_filter(units_f, 'search-has-inferential',
                                 lambda f, k: ops[int(f)](all(x.inferential_example in ['','не засвидетельствовано'] for x in units_gr[k])))
        
        # Search illocutionary
        units_f = process_filter(units_f, 'search-has-illoc',
                                 lambda f, k: ops[int(f)](all(x.illoc_example in ['','не засвидетельствовано'] for x in units_gr[k])))
        
        # Search metatext
        units_f = process_filter(units_f, 'search-has-metatext',
                                 lambda f, k: ops[int(f)](all(x.metatext_example in ['','не засвидетельствовано'] for x in units_gr[k])))
        
        # Search correl
        units_f = process_filter(units_f, 'search-has-correl',
                                 lambda f, k: ops[int(f)](all(x.correl == '' for x in units_gr[k])))
        
        # Search branching
        units_f = process_filter(units_f, 'search-has-branching',
                                 lambda f, k: ops[int(f)](all(x.expansion == '' for x in units_gr[k])))        
        
        # Helper function for syntactic parameters
        synt_test = lambda p: lambda f, k: any(int(f) in x._asdict()[p] if isinstance(x._asdict()[p],list) else int(f) == x._asdict()[p] for x in units_gr[k])

        # Batch process the parameters
        for filter in request.args.keys():
            prm = filter.removeprefix('search-')
            if prm in db.param_values.keys():
                units_f = process_filter(units_f, filter, synt_test(prm))

        if request.args.get('linker') is not None:
            linker = unquote_lnk(request.args.get('linker'))
        else: 
            linker = unquote_lnk(units_f[0])

        pos_uniq = sorted(list(dict.fromkeys([x.pos for x in db.meanings if x.pos != ''])))

        units_f = sorted(units_f, key=lambda s: s[0] if s[0].isalnum() else 'ع' + s[1:])
        
        # Alphabetic order of filtered values
        alphabetic = dict()
        for k in units_f:
            if k[0].isalpha() and k[0] not in alphabetic.keys():
                alphabetic[k[0]] = k

        return render_template('units.html',
                            #    sources=db.sources,
                               pos_list=pos_uniq,
                               filters=filters,
                            #    edit=False,
                            #    units=dict(sorted(units_gr.items(),key=lambda s: s[0] if s[0][0].isalnum() else 'Ω' + s[0][1:])),
                               units=units_gr, 
                               units_f=units_f,
                               alphabetic=alphabetic,
                               meanings=db.meanings,
                               sources=db.sources,
                               params=db.param_values,
                               semfields=sorted(db.semfields, key = lambda x : x.display_ru),
                               subfields=sorted(db.subfields, key = lambda x : x.display_ru),
                               linker=linker,
                               olds=db.diachronic[linker] if linker in db.diachronic.keys() else None)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        pass

    return app