from mongoengine import Document, StringField, DateTimeField, ListField, DictField, IntField, connect
from datetime import datetime
import tldextract, requests
from config import config

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_domain_name(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def send_discord_message(message):
    data = {
        "content": message
    }

    response = requests.post(config().get('WEBHOOK_URL'), json=data)

    if response.status_code == 204:
        pass
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Connect to MongoDB
connect(db='watch', host='mongodb://127.0.0.1:27017/watch')

# Define the Programs model
class Programs(Document):
    program_name = StringField(required=True)
    created_date = DateTimeField(default=datetime.now())
    config = DictField()
    scopes = ListField(StringField(), default=[])
    ooscopes = ListField(StringField(), default=[])

    meta = {
        'indexes': [
            {'fields': ['program_name'], 'unique': True}  # Create a unique index on 'name'
        ]
    }

# Define the Subdomains model
class Subdomains(Document):
    program_name = StringField(required=True)
    subdomain = StringField(required=True)
    scope = StringField(required=True)
    providers = ListField(StringField())
    created_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            {'fields': ['program_name', 'subdomain'], 'unique': True}  # Create a unique index on 'program_name' and 'subdomain'
        ]
    }

# Define the LiveSubdomains model
# todo: extend the model to store CNMAE, TXT, etc
class LiveSubdomains(Document):
    program_name = StringField(required=True)
    subdomain = StringField(required=True)
    scope = StringField(required=True)
    ips = ListField(StringField())
    cdn = StringField()
    created_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            {'fields': ['program_name', 'subdomain'], 'unique': True}  # Create a unique index on 'program_name' and 'subdomain'
        ]
    }

# Define the LiveSubdomains model
# todo: extend the model to store CNMAE, TXT, etc
class Http(Document):
    program_name = StringField(required=True)
    subdomain = StringField(required=True)
    scope = StringField(required=True)
    ips = ListField(StringField())
    tech = ListField(StringField())
    title = StringField()
    status_code = IntField()
    headers = DictField()
    url = StringField()
    final_url = StringField()
    favicon = StringField()
    created_date = DateTimeField(default=datetime.now())
    last_update = DateTimeField(default=datetime.now())

    meta = {
        'indexes': [
            {'fields': ['program_name', 'subdomain'], 'unique': True}  # Create a unique index on 'program_name' and 'subdomain'
        ]
    }

'''
1. http service to work on (general)
2. http fresh services to work on
3. searching through HTTP headers
4. changes of techs or status codes or etc
'''



# Upsert Programs
def upsert_program(program_name, scopes, ooscopes, config):
    program = Programs.objects(program_name=program_name).first()
    
    if program:
        # Update existing program fields
        program.config = config
        program.scopes = scopes
        program.ooscopes = ooscopes
        program.save()
        print(f"[{current_time()}] Updated program: {program.program_name}")
    else:
        # Create new program
        new_program = Programs(
            program_name=program_name,
            created_date=datetime.now(),
            config=config,
            scopes=scopes,
            ooscopes=ooscopes
        )
        new_program.save()
        print(f"[{current_time()}] Inserted new program: {new_program.program_name}")

def upsert_lives(obj):
    # obj: {'subdomain': 'account.web.superbet.ro', 'domain': 'superbet.ro', 'ips': ['18.245.253.35', '18.245.253.54', '18.245.253.9', '18.245.253.27']}

    program = Programs.objects(scopes=obj.get('domain')).first()
    # program.program_name

    existing = LiveSubdomains.objects(subdomain=obj.get('subdomain')).first()
    if existing:
        existing.ips.sort()
        obj.get('ips').sort()
        
        if obj.get('ips') != existing.ips:
            existing.ips = obj.get('ips')
            print(f"[{current_time()}] Updated liev subdomain: {obj.get('subdomain')}")
        
        existing.last_update = datetime.now()
        existing.save()

    else:
        new_live_subdomain = LiveSubdomains(
            program_name=program.program_name,
            subdomain=obj.get('subdomain'),
            scope=obj.get('domain'),
            ips=obj.get('ips'),
            cdn=obj.get('cdn'),
            created_date=datetime.now(),
            last_update=datetime.now()
        )
        new_live_subdomain.save()

        # todo: notify if new live subdomain is added!
        send_discord_message(f"```'{obj.get('subdomain')}' (fresh live) has been added to '{program.program_name}' program```")
        print(f"[{current_time()}] Inserted new live subdomain: {obj.get('subdomain')}")

    return True

def upsert_http(obj):
    # {'subdomain': 'dl-api.voorivex.academy', 'scope': 'voorivex.academy', 'ips': ['185.166.104.4', '185.166.104.3'], 'tech': ['HSTS'], 'title': '', 'status_code': 403, 'headers': {'accept_ranges': 'bytes', 'cache_control': 'no-store', 'content_length': '15', 'content_type': 'text/html; charset=utf-8', 'date': 'Thu, 15 Aug 2024 12:45:17 GMT', 'server': 'Delivery', 'strict_transport_security': 'max-age=31536000', 'x_zrk_sn': '2001'}, 'url': 'https://dl-api.voorivex.academy:443', 'final_url': ''}

    program = Programs.objects(scopes=obj.get('scope')).first()
    # program.program_name

    # already existed http service
    existing = Http.objects(subdomain=obj.get('subdomain')).first()
    if existing:

        if existing.title != obj.get('title'):
            send_discord_message(f"```'{obj.get('subdomain')}' title has been changed from '{existing.title}' to '{obj.get('title')}'```")
            print(f"[{current_time()}] changes title for subdomain: {obj.get('subdomain')}")
            existing.title = obj.get('title')

        if existing.status_code != obj.get('status_code'):
            send_discord_message(f"```'{obj.get('subdomain')}' status code has been changed from '{existing.status_code}' to '{obj.get('status_code')}'```")
            print(f"[{current_time()}] changes status code for subdmoain: {obj.get('subdomain')}")
            existing.status_code = obj.get('status_code')

        
        if existing.favicon != obj.get('favicon'):
            send_discord_message(f"```'{obj.get('subdomain')}' favhash has been changed from '{existing.favicon}' to '{obj.get('favicon')}'```")
            print(f"[{current_time()}] changes favhash for subdomain: {obj.get('subdomain')}")
            existing.favicon = obj.get('favicon')

        existing.ips = obj.get('ips')
        existing.tech = obj.get('tech')
        existing.headers = obj.get('headers')
        existing.url = obj.get('url')
        existing.final_url = obj.get('final_url')
        existing.last_update = datetime.now()
        existing.save()

    else:
        new_http = Http(
            program_name = program.program_name,
            subdomain = obj.get('subdomain'),
            scope = obj.get('scope'),
            ips = obj.get('ips'),
            tech = obj.get('tech'),
            title = obj.get('title'),
            status_code = obj.get('status_code'),
            headers = obj.get('headers'),
            url = obj.get('url'),
            final_url = obj.get('final_url'),
            favicon = obj.get('favicon'),
            created_date = datetime.now(),
            last_update = datetime.now()
        )
        new_http.save()

        # todo: notify if new live subdomain is added!
        send_discord_message(f"```'{obj.get('subdomain')}' (fresh http) has been added to '{program.program_name}' program```")
        print(f"[{current_time()}] Inserted new http service: {obj.get('subdomain')}")

    return True

# Check if subdomain exists, if not insert, if yes update providers
def upsert_subdomain(program_name, subdomain_name, provider):

    program = Programs.objects(program_name=program_name).first()
    if get_domain_name(subdomain_name) not in program.scopes or subdomain_name in program.ooscopes:
        print(f"[{current_time()}] subdomain is not in scope: {subdomain_name}")
        return True
    
    # todo: check if subdomain exists or not, filter: domain.tld or *.domain.tld
    
    existing = Subdomains.objects(program_name=program_name, subdomain=subdomain_name).first()
    
    if existing:
        if provider not in existing.providers:
            existing.providers.append(provider)
            existing.last_update = datetime.now()
            existing.save()
            print(f"[{current_time()}] Updated subdomain: {subdomain_name}")
        else:
            pass
    else:
        new_subdomain = Subdomains(
            program_name=program_name,
            subdomain=subdomain_name,
            scope=get_domain_name(subdomain_name),
            providers=[provider],
            created_date=datetime.now(),
            last_update=datetime.now()
        )
        new_subdomain.save()
        print(f"[{current_time()}] Inserted new subdomain: {subdomain_name}")