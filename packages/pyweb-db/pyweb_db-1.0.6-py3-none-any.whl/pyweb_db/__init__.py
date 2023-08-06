import json, os, aiofiles, asyncio

class async_connection:
    def __init__(self, database_path: str = None):
        if database_path is None:
            raise ValueError('ERROR! INCORRECT DATABASE PATH!')
        self.path = database_path
        if not os.path.isfile(self.path):
            self.create_empty_database()
    
    def create_empty_database(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump({}, file)
    
    async def load_data(self):
        async with aiofiles.open(self.path, 'r', encoding='utf-8') as file:
            return json.loads(await file.read())
    
    async def save_data(self, data):
        async with aiofiles.open(self.path, 'w', encoding='utf-8') as file:
            await file.write(json.dumps(data))
    
    async def create_table(self, table_name: str):
        db_content = await self.load_data()
        if table_name not in db_content:
            db_content[table_name] = []
            await self.save_data(db_content)
    
    async def create_tables(self, table_names: list):
        db_content = await self.load_data()
        if type(table_names) != list:
            print(f'INCORRECT TYPE!\n{table_names}')
            return
        for table_name in table_names:
            if table_name not in db_content:
                db_content[table_name] = []
                await self.save_data(db_content)

    async def insert_into_table(self, table_name: str, data, unique: bool = False):
        db_content = await self.load_data()
        if table_name in db_content:
            if (not data in db_content[table_name] and unique == True):
                db_content[table_name].append(data)
                await self.save_data(db_content)
            elif unique == False:
                db_content[table_name].append(data)
                await self.save_data(db_content)
    
    async def insert_datas_into_table(self, table_name: str, datas: list, unique: bool = False):
        db_content = await self.load_data()
        if not type(datas) == list:
            print(f'INCORRECT TYPE!\n{datas}')
            return
        if table_name in db_content:
            for data in datas:
                if (not data in db_content[table_name] and unique == True):
                    db_content[table_name].append(data)
                elif unique == False:
                    db_content[table_name].append(data)
            await self.save_data(db_content)
    
    async def insert_datas_into_tables(self, table_names: list, datas: list, unique: bool = False):
        db_content = await self.load_data()
        if not type(datas) == list:
            print(f'INCORRECT TYPE!\n{datas}')
            return
        if not type(table_names) == list:
            print(f'INCORRECT TYPE!\n{table_names}')
            return
        for table_name, data in zip(table_names, datas):
            if table_name in db_content:
                if (not data in db_content[table_name] and unique == True):
                    db_content[table_name].append(data)
                elif unique == False:
                    db_content[table_name].append(data)
            await self.save_data(db_content)

    async def delete_from_table(self, table_name: str, data):
        db_content = await self.load_data()
        if table_name in db_content:
            if data in db_content[table_name]:
                db_content[table_name].remove(data)
                await self.save_data(db_content)
    
    async def delete_table(self, table_name: str):
        db_content = await self.load_data()
        if table_name in db_content:
            del db_content[table_name]
            await self.save_data(db_content)
    
    async def delete_tables(self, table_names: list):
        if type(table_names) != list:
            print(f'INCORRECT TYPE!\n{table_names}')
            return
        db_content = await self.load_data()
        for table_name in table_names:
            if table_name in db_content:
                del db_content[table_name]
                await self.save_data(db_content)
    
    async def update_data(self, table_name: str, data, replace_data):
        db_content = await self.load_data()
        if table_name in db_content and data in db_content[table_name]:
            index4replace = db_content[table_name].index(data)
            db_content[table_name][index4replace] = replace_data
            await self.save_data(db_content)
    
    async def get_data(self, table_name: str):
        db_content = await self.load_data()
        if table_name in db_content:
            return db_content[table_name]

class connection:
    def __init__(self, database_path: str = None):
        if database_path is None:
            raise ValueError('ERROR! INCORRECT DATABASE PATH!')
        
        self.path = database_path
        
        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump({}, file)
    
    def create_table(self, table_name: str):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name not in db_content:
                db_content[table_name] = []
                file.seek(0)
                json.dump(db_content, file)
    
    def create_tables(self, table_names: list):
        if type(table_names) != list:
            print(f'INCORRECT TYPE!\n{table_names}')
            return
        with open(self.path, 'r+') as file:
            db_content = json.load(file)
            for table_name in table_names:
                if table_name not in db_content:
                    db_content[table_name] = []
                    file.seek(0)
                    json.dump(db_content, file)

    def insert_into_table(self, table_name: str, data, unique: bool = False):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name in db_content:
                if (not data in db_content[table_name] and unique == True):
                    db_content[table_name].append(data)
                    file.seek(0)
                    json.dump(db_content, file)
                elif unique == False:
                    db_content[table_name].append(data)
                    file.seek(0)
                    json.dump(db_content, file)
    
    def insert_datas_into_table(self, table_name: str, datas: list, unique: bool = False):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if not type(datas) == list:
                print(f'INCORRECT TYPE!\n{datas}')
                return
            if table_name in db_content:
                for data in datas:
                    if (not data in db_content[table_name] and unique == True):
                        db_content[table_name].append(data)
                    elif unique == False:
                        db_content[table_name].append(data)
                file.seek(0)
                json.dump(db_content, file)
    
    def insert_datas_into_tables(self, table_names: list, datas: list, unique: bool = False):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if not type(datas) == list:
                print(f'INCORRECT TYPE!\n{datas}')
                return
            if not type(table_names) == list:
                print(f'INCORRECT TYPE!\n{table_names}')
                return
            for table_name, data in zip(table_names, datas):
                if table_name in db_content:
                    if (not data in db_content[table_name] and unique == True):
                        db_content[table_name].append(data)
                    elif unique == False:
                        db_content[table_name].append(data)
                file.seek(0)
                json.dump(db_content, file)

    def delete_from_table(self, table_name: str, data):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name in db_content:
                if data in db_content[table_name]:
                    db_content[table_name].remove(data)
                    file.seek(0)
                    json.dump(db_content, file)
                    file.truncate()
    
    def delete_table(self, table_name: str):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name in db_content:
                del db_content[table_name]
                file.seek(0)
                json.dump(db_content, file)
                file.truncate()
    
    def delete_tables(self, table_names: list):
        if type(table_names) != list:
            print(f'INCORRECT TYPE!\n{table_names}')
            return
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            for table_name in table_names:
                if table_name in db_content:
                    del db_content[table_name]
                    file.seek(0)
                    json.dump(db_content, file)
                    file.truncate()
    
    def update_data(self, table_name: str, data, replace_data):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name in db_content and data in db_content[table_name]:
                index4replace = db_content[table_name].index(data)
                db_content[table_name][index4replace] = replace_data
                file.seek(0)
                json.dump(db_content, file)
                file.truncate()
    
    def get_data(self, table_name: str):
        with open(self.path, 'r+', encoding='utf-8') as file:
            db_content = json.load(file)
            if table_name in db_content:
                return db_content[table_name]