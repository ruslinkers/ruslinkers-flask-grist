import os

from collections import defaultdict

from flask import Flask, render_template, request, redirect, url_for, send_file

from urllib.parse import quote_plus,unquote_plus

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
    app.jinja_env.filters['quote_lnk'] = quote_lnk
    app.jinja_env.filters['unquote_lnk'] = unquote_lnk

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

    # show unit
    @app.route('/units/<string:linker>', methods=['GET'])
    def units(linker: str):
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
        for u in db.linkers.values():
            units_gr[u.form].append(u)
        
        lnkr = unquote_lnk(linker)
        return render_template('units.html',
                            #    sources=db.sources,
                            #    pos_list=pos_uniq,
                            #    edit=False,
                            #    units=dict(sorted(units_gr.items(),key=lambda s: s[0] if s[0][0].isalnum() else 'Ω' + s[0][1:])),
                               units={k:units_gr[k] for k in sorted(units_gr.keys(), key=lambda s: s[0] if s[0].isalnum() else 'ع' + s[1:])},
                               meanings=db.meanings,
                               linker=lnkr,
                               olds=db.diachronic[lnkr] if lnkr in db.diachronic.keys() else None)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        pass

    return app