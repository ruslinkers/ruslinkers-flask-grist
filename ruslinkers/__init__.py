import os

from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for, send_file

from urllib.parse import quote_plus,unquote_plus

import markdown
# import jinja2
from markupsafe import Markup

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

        units_f = sorted(list(units_gr.keys()), key=lambda s: s[0] if s[0].isalnum() else 'ع' + s[1:])
        filters = dict()

        if request.args.get('search-pos') is not None:
            filters['search-pos'] = request.args.get('search-pos')
            units_f = [k for k in units_f if any(filters['search-pos'] in x.pos_txt[1:] for x in units_gr[k])]
        if request.args.get('search-dict') is not None:
            filters['search-dict'] = request.args.get('search-dict')
            units_f = [k for k in units_f if any(int(filters['search-dict']) in x.dicts[1:] for x in units_gr[k])]
        if request.args.get('linker') is not None:
            linker = unquote_lnk(request.args.get('linker'))
        else: 
            linker = unquote_lnk(units_f[0])

        pos_uniq = sorted(list(dict.fromkeys([x.pos for x in db.meanings])))
        
        return render_template('units.html',
                            #    sources=db.sources,
                               pos_list=pos_uniq,
                               filters=filters,
                            #    edit=False,
                            #    units=dict(sorted(units_gr.items(),key=lambda s: s[0] if s[0][0].isalnum() else 'Ω' + s[0][1:])),
                               units=units_gr, 
                               units_f=units_f,
                               meanings=db.meanings,
                               sources=db.sources,
                               params=db.param_values,
                               linker=linker,
                               olds=db.diachronic[linker] if linker in db.diachronic.keys() else None)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        pass

    return app