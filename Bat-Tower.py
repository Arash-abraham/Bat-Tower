import sys, os, subprocess, re , psycopg2
from flask import Flask, jsonify , request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'database')))
from datetime import datetime, timedelta

from db import *

print(' * Bat Tower Is RUN !')
app = Flask(__name__)

@app.route('/api/programs/all')
def all_programs():
    programs = Programs.objects().all()

    response = {}
    for program in programs:
        response[program.program_name] = {
            'scopes': program.scopes,
            'ooscopes': program.ooscopes,
            'config': program.config,
            'created_date': program.created_date,
            }

    # Return JSON response
    return response

@app.route('/api/subdomains/domain/<domain>')
def subdomains_of_domain(domain):
    obj_subdomains = Subdomains.objects(scope=domain)

    if obj_subdomains:
        # Convert query result to list of dictionaries
        response = ''
        for obj_sub in obj_subdomains:
            response += f"{obj_sub.subdomain}\n"

        return response
    else:
        return 'subdomain not found'

@app.route('/api/subdomains/program/<p_name>')
def subdomains_of_program(p_name):
    obj_subdomains = Subdomains.objects(program_name=p_name)

    if obj_subdomains:
        # Convert query result to list of dictionaries
        response = ''
        for obj_sub in obj_subdomains:
            response += f"{obj_sub.subdomain}\n"

        return response
    else:
        return 'subdomain not found'

# todo: option for json object
@app.route('/api/subdomains/all')
def all_subdomains():
    obj_subdomains = Subdomains.objects().all()

    response = ''
    for obj_sub in obj_subdomains:
        response += f"{obj_sub.subdomain}\n"

    return response

# @app.route('/api/lives/domain/<domain>')
# @app.route('/api/lives/program/<p_name>')

@app.route('/api/lives/all')
def all_lives():
    twelve_hours_ago = datetime.now() - timedelta(hours=12)
    lives_obj = LiveSubdomains.objects(last_update__gte=twelve_hours_ago).all()

    response = ''
    for live_obj in lives_obj:
        response += f"{live_obj.subdomain}\n"

    return response

@app.route('/api/lives/fresh')
def all_lives_fresh():
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    fresh_lives = LiveSubdomains.objects(created_date__gte=twenty_four_hours_ago)
    
    res_array = [f"{fresh_live.subdomain}" for fresh_live in fresh_lives]
    return '\n'.join(res_array)


@app.route('/api/live/subdomain/<live>')
def all_live_single(live):
    
    live_obj = LiveSubdomains.objects(subdomain=live).first()
    subdomain_obj = Subdomains.objects(subdomain=live).first()

    if live_obj and subdomain_obj:

        return {
            "program_name": live_obj.program_name,
            "subdomain": live_obj.subdomain,
            "scope": live_obj.scope,
            "ips": live_obj.ips or [],
            "cdn": live_obj.cdn,
            "providers": subdomain_obj.providers or [],
            "created_date": (
                live_obj.created_date.isoformat()
                if live_obj.created_date
                else None
            ),
            "last_update": (
                live_obj.last_update.isoformat()
                if live_obj.last_update
                else None
            ),
        }
    
    return f"{live} not found"


@app.route('/api/lives/provider/<provider>')
def all_lives_provider(provider):
    twelve_hours_ago = datetime.now() - timedelta(hours=12)

    subs_obj = Subdomains.objects(providers=[provider])

    live_subdomains = []
    for sub_obj in subs_obj:
        live = LiveSubdomains.objects(subdomain=sub_obj.subdomain, last_update__gte=twelve_hours_ago).first()
        if live:
            live_subdomains.append(live.subdomain)

    if not live_subdomains:
        return "No live subdomains found.", 404

    return '\n'.join(live_subdomains)


@app.route('/api/http/fresh')
def all_http_fresh():
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    fresh_https = Http.objects(created_date__gte=twenty_four_hours_ago)
    
    res_array = [f"{fresh_http.url}" for fresh_http in fresh_https]
    return '\n'.join(res_array)

@app.route('/api/http/provider/<provider>')
def all_http_provider(provider):
    twelve_hours_ago = datetime.now() - timedelta(hours=12)

    subs_obj = Subdomains.objects(providers=[provider])

    resp = ''
    for sub_obj in subs_obj:
        http = Http.objects(subdomain=sub_obj.subdomain, last_update__gte=twelve_hours_ago).first()
        if http:
            resp += f"{http.url}\n"

    return resp

@app.route('/api/http/all')
def all_http():
    twelve_hours_ago = datetime.now() - timedelta(hours=12)
    https_obj = Http.objects(last_update__gte=twelve_hours_ago).all()

    response = ''
    for http_obj in https_obj:
        response += f"{http_obj.url}\n"

    return response

@app.route('/')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
