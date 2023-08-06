import json
import os
import uuid
import hashlib
import datetime
import shutil
import zipfile
from pprint import pprint
import time
from urllib.parse import urlparse, parse_qs

class NexusClient:
    def __init__(self, db_folder):
        self.db_folder = db_folder
        self.authenticated = False
        self.db_path = os.path.join('database', self.db_folder)
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        
        self.logs_path = os.path.join(self.db_path, 'logs', 'logs.json')
        logs_dir = os.path.join(self.db_path, 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        self.config = {}
       
    def set_app(self, mode):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if mode.lower() not in ["production", "development"]:
            raise ValueError(f"{BOLD_RED}Invalid app mode. Choose either 'Production' or 'Development'.{RESET_COLOR}")
        self.config['APP_MODE'] = mode.lower()

        if mode.lower() == "production":
            # Change permissions for all folders (Example: Read, Write, Execute for all)
            for root, dirs, files in os.walk(self.db_path):
                os.chmod(root, 0o444)
                for file in files:
                    os.chmod(os.path.join(root, file), 0o444)
                for dir in dirs:
                    os.chmod(os.path.join(root, dir), 0o444)
        elif mode.lower() == "development":
            BOLD_RED = "\033[91m"
            BOLD_YELLOW = "\033[93m"
            RESET_COLOR = "\033[0m"
            BOLD_WHITE = "\033[97m"
            current_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"{BOLD_WHITE}Development mode enabled - 127.0.0.1:3717 [{current_date_time}] \n"
            message += f"{BOLD_RED}* NexusClient['production'] -- Restart with stat{RESET_COLOR} \n"
            message += f"{BOLD_YELLOW}* DEBUGGER ID: {uuid.uuid4()} {RESET_COLOR}\n"
            message += f"{BOLD_WHITE}* CONNECTION: 127.0.0.1:3717 connected{RESET_COLOR}\n"
            message += f"{BOLD_RED}Note: For production usage use db.config['APP_MODE'] == 'production' v.2.1.1 {RESET_COLOR}\n"
            message += f"{BOLD_YELLOW}Version control by NexusDB @2023 JsonComponents{RESET_COLOR}\n"
            message += f"{BOLD_WHITE}output: {RESET_COLOR}"
            print(message)
               
    def connect(self, connection_url):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        parsed_url = urlparse(connection_url)

        if parsed_url.scheme != "nexus":
            raise ValueError(f"{BOLD_RED}Invalid connection URL. Scheme must be 'nexus'.{RESET_COLOR}")

        if parsed_url.netloc != "localhost:3717":
            raise ValueError(f"{BOLD_RED}Invalid connection URL. invalid host and port use deafult host 'localhost' and port '3717'.{RESET_COLOR}")

        query_params = parse_qs(parsed_url.query)
        if "rsa_id" not in query_params or "encryption" not in query_params:
            raise ValueError(f"{BOLD_RED}Invalid connection URL. 'rsa_id' and 'encryption' query parameters are required.{RESET_COLOR}")

        email, password = self._extract_email_password(parsed_url.path)
        rsa_id = query_params["rsa_id"][0]
        encryption_format = query_params["encryption"][0]

        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}Users collection does not exist{RESET_COLOR}')

        with open(users_path, 'r') as f:
            users = json.load(f)
            for user in users:
                if user['status'] == "blocked":
                    raise ValueError(f"{BOLD_RED}User blocked! Contact admin for more details{RESET_COLOR}")
                else:
                    if user['role'] not in ['admin', 'devops']:
                        raise ValueError(f"{BOLD_RED}Access denied! Contact admin for more details{RESET_COLOR}")
                    else:
                        if user['email'] == email:
                            salt = bytes.fromhex(user['salt'])
                            hashed_password = hashlib.pbkdf2_hmac(
                                'sha256',
                                password.encode('utf-8'),
                                salt,
                                100000
                            )
                            if user['password'] == hashed_password.hex():
                                self.authenticated = True
                                return user
                            else:
                                raise ValueError(f'{BOLD_RED}Incorrect password{RESET_COLOR}')
        raise ValueError(f'{BOLD_RED}User not found{RESET_COLOR}')
    
    def disconnect(self):
        GREEN = "\033[32m"
        RESET_COLOR = "\033[0m"

        self.authenticated = False
        print(f"{GREEN}nexusdb disconnected!{RESET_COLOR}")

    def _extract_email_password(self, path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if not path.startswith("/"):
            raise ValueError(f"{BOLD_RED}Invalid connection URL. Email and password must be specified in the path.{RESET_COLOR}")

        path = path[1:]  # Remove the leading slash
        if ":" not in path:
            raise ValueError(f"{BOLD_RED}Invalid connection URL. Email and password must be separated by ':' in the path.{RESET_COLOR}")

        email, password = path.split(":", 1)
        return email, password
    
    def check_authentication(func):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        def wrapper(self, *args, **kwargs):
            if not self.authenticated:
                raise Exception(f"{BOLD_RED}nexus connection isn't established pass your connection string for more details visit, {RESET_COLOR} http://nexusdb.vvfin.in/docs/connect?uri=True&method=nexusPY&verison=control1.2.1")
            return func(self, *args, **kwargs)
        return wrapper
    
    @check_authentication
    def create_collection(self, collection_name):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        BOLD_YELLOW = "\033[93m"
        if collection_name == 'users':
            print(f"{BOLD_RED}Root folder can be override,{RESET_COLOR}", f'{BOLD_YELLOW}collection_name{RESET_COLOR}', f'{BOLD_RED}already assigned as root directory.{RESET_COLOR}')
        else:
            collection_path = os.path.join(self.db_path, collection_name + '.json')
            if os.path.exists(collection_path):
                raise ValueError(f'{BOLD_RED}Collection already exists{RESET_COLOR}')
            with open(collection_path, 'w') as f:
                json.dump([], f, indent=4)
                f.write('\n')
            self._log_action('create_collection', collection_name)
        
    @check_authentication
    def insert(self, collection_name, document):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r+') as f:
            data = json.load(f)
            document['_id'] = str(uuid.uuid4().hex)
            data.append(document)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        pprint(document, indent=4)
        self._log_action('insert_document', collection_name, document)
        
    @check_authentication 
    def find_one(self, collection_name, query):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            results = [doc for doc in data if self._match_query(doc, query)]
            self._log_action('find_documents', collection_name, query, results)
            if results:
                return results[0]  # Return the first matching document
            else:
                return None 
        
    @check_authentication 
    def remove(self, collection_name, query):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r') as f:
            data = json.load(f)
        filtered_data = [doc for doc in data if not all(doc.get(key) == value for key, value in query.items())]
        if len(data) == len(filtered_data):
            raise ValueError(f'{BOLD_RED}Document does not exist in the collection{RESET_COLOR}')
        with open(collection_path, 'w') as f:
            json.dump(filtered_data, f, indent=4)
        self._log_action('remove', collection_name, str(query))



    def create_user(self, name, email, password, role):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            os.makedirs(os.path.join(self.db_path, 'users'))
            with open(users_path, 'w') as f:
                json.dump([], f, indent=4)
                f.write('\n')

        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['email'] == email:
                    raise ValueError( f"{BOLD_RED}Error: Email already exists.{RESET_COLOR}")
            salt = os.urandom(16)
            hashed_password = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            user = {
                '_id': str(uuid.uuid4().hex),
                'name': name,
                'email': email,
                'password': hashed_password.hex(),
                'role': role,
                'status': 'active',
                'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'salt': salt.hex()
            }
            users.append(user)
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        pprint(user, indent=4)
        self._log_action('create_user', name, email, role)
        
    @check_authentication 
    def remove_user(self, user_id):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}Users collection does not exist{RESET_COLOR}')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            filtered_users = [user for user in users if user['_id'] != user_id]
            f.seek(0)
            json.dump(filtered_users, f, indent=4)
            f.truncate()
        self._log_action('remove_user', user_id)
        
    @check_authentication 
    def block_user(self, user_id):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}Users collection does not exist{RESET_COLOR}')

        current_time = time.time()
        time_limit = 24 * 60 * 60  # 24 hours in seconds
        expiration_time = current_time + time_limit

        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    user['status'] = 'blocked'
                    user['expiration_time'] = expiration_time
                    break
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()

        self._log_action('block_user', user_id)

        # Check for expired users and change status back to "active"
        expired_users = [user for user in users if user.get('expiration_time', 0) < current_time]
        if expired_users:
            for user in expired_users:
                user['status'] = 'active'

            with open(users_path, 'w') as f:
                json.dump(users, f, indent=4)
        
    @check_authentication 
    def revoke_user(self, user_id):
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError('Users collection does not exist')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    user['status'] = 'revoked'
                    break
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        self._log_action('revoke_user', user_id)
        
    @check_authentication 
    def update(self, collection_name, document_id, update_data):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r+') as f:
            data = json.load(f)
            updated = False
            for doc in data:
                if doc['_id'] == document_id:
                    doc.update(update_data)
                    updated = True
                    break
            if updated:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print('Document updated successfully.')
            else:
                print(f'{BOLD_RED}Document not found.{RESET_COLOR}')
        self._log_action('update_document', collection_name, document_id, update_data)
        
    @check_authentication 
    def fetch_all(self, collection_name):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            self._log_action('get_all_documents', collection_name)
            return data
        
    @check_authentication 
    def count(self, collection_name):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            self._log_action('count_documents', collection_name)
            return len(data)
        
    @check_authentication 
    def drop_collection(self, collection_name):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        os.remove(collection_path)
        print(f'Collection {collection_name} dropped successfully.')
        self._log_action('drop_collection', collection_name)
        
    @check_authentication 
    def drop_database(self):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
            print(f'Database {self.db_folder} dropped successfully.')
        else:
            raise ValueError(f'{BOLD_RED}Database does not exist.{RESET_COLOR}')
        self._log_action('drop_database', self.db_folder)
        
    @check_authentication 
    def import_database(self, zip_path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if not zipfile.is_zipfile(zip_path):
            raise ValueError('Invalid zip file')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.db_path)
        print('Database imported successfully.')
        self._log_action('import_database', zip_path)
        
    @check_authentication 
    def import_collection(self, collection_name, zip_path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f'{BOLD_RED}Invalid zip file{RESET_COLOR}')
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(collection_path))
        print(f'Collection {collection_name} imported successfully.')
        self._log_action('import_collection', collection_name, zip_path)
         
    @check_authentication 
    def export_database(self, export_path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(self.db_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_ref.write(file_path, os.path.relpath(file_path, self.db_path))
        print('Database exported successfully.')
        self._log_action('export_database', export_path)
        
    @check_authentication 
    def export_collection(self, collection_name, export_path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            zip_ref.write(collection_path, os.path.basename(collection_path))
        print(f'Collection {collection_name} exported successfully.')
        self._log_action('export_collection', collection_name, export_path)
        
    @check_authentication 
    def _match_query(self, document, query):
        for key, value in query.items():
            if key not in document or document[key] != value:
                return False
        return True
    
    def _log_action(self, function_name, *args):
        logs = []
        if os.path.exists(self.logs_path):
            with open(self.logs_path, 'r') as f:
                logs = json.load(f)
        log_entry = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'function_name': function_name,
            'args': args
        }
        logs.append(log_entry)
        with open(self.logs_path, 'w') as f:
            json.dump(logs, f, indent=4)
        print(f'Logged action: {function_name} {args}')
        
    @check_authentication 
    def create_index(self, collection_name, field):
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError('Collection does not exist')
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if os.path.exists(index_path):
            raise ValueError('Index already exists')
        with open(collection_path, 'r') as f:
            data = json.load(f)
            index_data = {}
            for doc in data:
                if field in doc:
                    value = doc[field]
                    if value not in index_data:
                        index_data[value] = []
                    index_data[value].append(doc['_id'])
        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=4)
            f.write('\n')
        pprint(index_data, indent=4)
        self._log_action('create_index', collection_name, field)
        
    @check_authentication 
    def drop_index(self, collection_name, field):
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if not os.path.exists(index_path):
            raise ValueError('Index does not exist')
        os.remove(index_path)
        print(f'Index {collection_name}_{field}_index dropped successfully.')
        self._log_action('drop_index', collection_name, field)
        
    @check_authentication 
    def get_index(self, collection_name, field):
        index_path = os.path.join(self.db_path, collection_name + '_' + field + '_index.json')
        if not os.path.exists(index_path):
            raise ValueError('Index does not exist')
        with open(index_path, 'r') as f:
            index_data = json.load(f)
            self._log_action('get_index', collection_name, field)
            return index_data
        
    @check_authentication 
    def backup_database(self, backup_path):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        GREEN = "\033[32m"
        if os.path.exists(backup_path):
            raise ValueError(f'{BOLD_RED}Backup path already exists{RESET_COLOR}')
        shutil.copytree(self.db_path, backup_path)
        print(f'{GREEN}Database backup created successfully in,{RESET_COLOR}', backup_path)
        self._log_action('backup_database', backup_path)
        
    @check_authentication 
    def restore_database(self, backup_path):
        GREEN = "\033[32m"
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        if not os.path.exists(backup_path):
            raise ValueError(f'{BOLD_RED}Backup path does not exist{RESET_COLOR}')
        shutil.rmtree(self.db_path)
        shutil.copytree(backup_path, self.db_path)
        print(f'{GREEN}Database restored successfully.{RESET_COLOR}')
        self._log_action('restore_database', backup_path)
        
    @check_authentication     
    def view_logs(self):
        with open(self.logs_path, 'r') as f:
            logs = f.read()
            print(logs)
            
    @check_authentication    
    def change_password(self, user_id, current_password, new_password):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}No users found{RESET_COLOR}')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    hashed_password = hashlib.pbkdf2_hmac(
                        'sha256',
                        current_password.encode('utf-8'),
                        bytes.fromhex(user['password']),
                        100000
                    )
                    if hashed_password.hex() == user['password']:
                        salt = os.urandom(16)
                        hashed_new_password = hashlib.pbkdf2_hmac(
                            'sha256',
                            new_password.encode('utf-8'),
                            salt,
                            100000
                        )
                        user['password'] = hashed_new_password.hex()
                        f.seek(0)
                        json.dump(users, f, indent=4)
                        f.truncate()
                        self._log_action('change_password', user_id)
                        return
                    else:
                        raise ValueError(f'{BOLD_RED}Incorrect password{RESET_COLOR}')
        raise ValueError(f'{BOLD_RED}User not found{RESET_COLOR}')
    
    @check_authentication 
    def update_user(self, user_id, update_data):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}No users found{RESET_COLOR}')
        with open(users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user['_id'] == user_id:
                    for key, value in update_data.items():
                        if key in user:
                            user[key] = value
                    f.seek(0)
                    json.dump(users, f, indent=4)
                    f.truncate()
                    self._log_action('update_user', user_id, update_data)
                    return
        raise ValueError(f'{BOLD_RED}User not found{RESET_COLOR}')
    
    @check_authentication 
    def get_user_by_email(self, email):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        users_path = os.path.join(self.db_path, 'users', 'users.json')
        if not os.path.exists(users_path):
            raise ValueError(f'{BOLD_RED}No users found{RESET_COLOR}')
        with open(users_path, 'r') as f:
            users = json.load(f)
            for user in users:
                if user['email'] == email:
                    return user
        raise ValueError(f'{BOLD_RED}User not found{RESET_COLOR}')
    
    @check_authentication 
    def compact_database(self):
        compact_db_path = os.path.join(self.db_path, 'compact')
        if os.path.exists(compact_db_path):
            shutil.rmtree(compact_db_path)
        os.makedirs(compact_db_path)

        for root, dirs, files in os.walk(self.db_path):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    compact_file_path = os.path.join(compact_db_path, file)
                    with open(compact_file_path, 'w') as f:
                        json.dump(data, f, separators=(',', ':'))
        shutil.rmtree(self.db_path)
        shutil.move(compact_db_path, self.db_path)
        print('Database compacted successfully.')
        self._log_action('compact_database')
        
    @check_authentication 
    def insert_many(self, collection_name, documents):
        for document in documents:
            self.insert(collection_name, document)

    @check_authentication 
    def update_many(self, collection_name, query, update_data):
        collection_path = os.path.join(self.db_path, collection_name)
        for filename in os.listdir(collection_path):
            if filename.endswith('.json'):
                document_path = os.path.join(collection_path, filename)
                with open(document_path, 'r') as f:
                    document = json.load(f)
                    if all(item in document.items() for item in query.items()):
                        document.update(update_data)
                        with open(document_path, 'w') as f:
                            json.dump(document, f)

    @check_authentication 
    def delete_many(self, collection_name, query):
        collection_path = os.path.join(self.db_path, collection_name)
        for filename in os.listdir(collection_path):
            if filename.endswith('.json'):
                document_path = os.path.join(collection_path, filename)
                with open(document_path, 'r') as f:
                    document = json.load(f)
                    if all(item in document.items() for item in query.items()):
                        os.remove(document_path)

    @check_authentication 
    def aggregate(self, collection_name, pipeline):
        collection_path = os.path.join(self.db_path, collection_name)
        documents = []
        for filename in os.listdir(collection_path):
            if filename.endswith('.json'):
                document_path = os.path.join(collection_path, filename)
                with open(document_path, 'r') as f:
                    document = json.load(f)
                    documents.append(document)

        for stage in pipeline:
            if stage.get('$match'):
                match_query = stage['$match']
                documents = [doc for doc in documents if all(item in doc.items() for item in match_query.items())]
            elif stage.get('$sort'):
                sort_query = stage['$sort']
                key = list(sort_query.keys())[0]
                reverse = sort_query[key] == -1
                documents = sorted(documents, key=lambda doc: doc.get(key), reverse=reverse)
            elif stage.get('$limit'):
                limit = stage['$limit']
                documents = documents[:limit]

        return documents

    @check_authentication 
    def distinct(self, collection_name, field):
        collection_path = os.path.join(self.db_path, collection_name)
        values = set()
        for filename in os.listdir(collection_path):
            if filename.endswith('.json'):
                document_path = os.path.join(collection_path, filename)
                with open(document_path, 'r') as f:
                    document = json.load(f)
                    value = document.get(field)
                    if value:
                        values.add(value)
        return list(values)

    @check_authentication 
    def find_one_and_update(self, collection_name, query, update_data):
        document = self.find_one(collection_name, query)
        if document:
            document.update(update_data)
            return document

    @check_authentication 
    def find_one_and_delete(self, collection_name, query):
        document = self.find_one(collection_name, query)
        if document:
            collection_path = os.path.join(self.db_path, collection_name)
            document_path = os.path.join(collection_path, f"{document['document_id']}.json")
            os.remove(document_path)
            return document

    @check_authentication 
    def bulk_write(self, collection_name, operations):
        for operation in operations:
            if operation['type'] == 'insert':
                document = operation['document']
                self.insert(collection_name, document)
            elif operation['type'] == 'update':
                query = operation['query']
                update_data = operation['update_data']
                self.update_many(collection_name, query, update_data)
            elif operation['type'] == 'delete':
                query = operation['query']
                self.delete_many(collection_name, query)

    @check_authentication
    def create_view(self, view_name, collection_name, pipeline):
        view_path = os.path.join(self.db_path, 'views', view_name)
        
        try:
            os.makedirs(view_path, exist_ok=True)
            
            view_pipeline_path = os.path.join(view_path, 'pipeline.json')
            with open(view_pipeline_path, 'w') as f:
                json.dump(pipeline, f)
            
            print(f"View '{view_name}' has been created successfully.")
        except FileExistsError:
            print(f"View '{view_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create view '{view_name}'.")
        except Exception as e:
            print(f"An error occurred while creating view '{view_name}': {str(e)}")

    @check_authentication
    def rename_collection(self, collection_name, new_collection_name):
        collection_path = os.path.join(self.db_path, collection_name + ".json")
        new_collection_path = os.path.join(self.db_path, new_collection_name + ".json")

        try:
            os.rename(collection_path, new_collection_path)
            print(f"Collection '{collection_name}' has been renamed to '{new_collection_name}' successfully.")
        except FileNotFoundError:
            print(f"Collection '{collection_name}' does not exist.")
        except FileExistsError:
            print(f"Collection '{new_collection_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to rename collection '{collection_name}'.")
        except Exception as e:
            print(f"An error occurred while renaming collection '{collection_name}': {str(e)}")

    @check_authentication 
    def aggregate_cursor(self, collection_name, pipeline):
        collection_path = os.path.join(self.db_path, collection_name)
        documents = []
        for filename in os.listdir(collection_path):
            if filename.endswith('.json'):
                document_path = os.path.join(collection_path, filename)
                with open(document_path, 'r') as f:
                    document = json.load(f)
                    documents.append(document)

        for stage in pipeline:
            if stage.get('$match'):
                match_query = stage['$match']
                documents = [doc for doc in documents if all(item in doc.items() for item in match_query.items())]
            elif stage.get('$sort'):
                sort_query = stage['$sort']
                key = list(sort_query.keys())[0]
                reverse = sort_query[key] == -1
                documents = sorted(documents, key=lambda doc: doc.get(key), reverse=reverse)
            elif stage.get('$limit'):
                limit = stage['$limit']
                documents = documents[:limit]

        for document in documents:
            yield document
     
    @check_authentication        
    def is_capped(self, collection_name):
        BOLD_RED = "\033[91m"
        RESET_COLOR = "\033[0m"
        collection_path = os.path.join(self.db_path, collection_name + '.json')
        if not os.path.exists(collection_path):
            raise ValueError(f'{BOLD_RED}Collection does not exist{RESET_COLOR}')
        
        with open(collection_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return False
        elif isinstance(data, dict):
            return True
        else:
            raise ValueError(f'{BOLD_RED}Invalid collection format{RESET_COLOR}')
        
    @check_authentication
    def list_collections(self):
        collections = []
        for root, dirs, files in os.walk(self.db_path):
            for file in files:
                if file.endswith('.json'):
                    collection_name = file[:-5]  # Remove the '.json' extension
                    collections.append(collection_name)
                    for name in collections:
                        print (name)
    
    @check_authentication
    def list_databases(self):
        database_names = os.listdir('database')
        for name in database_names:
            print(name)
      