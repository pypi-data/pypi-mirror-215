import pyweb_db, asyncio

# async example
async def main():
    conn = pyweb_db.async_connection('database') # Create connection
    
    await conn.create_table('uids')  # Create a table named 'uids'
    await conn.create_table('names')  # Create a table named 'names'
    
    await conn.insert_datas_into_table('uids', [9234, 3895345, 4358, 340858340], unique=True)  # Insert multiple data into the 'uids' table
    await conn.insert_datas_into_table('names', ['John', 'Michael', 'Daniel', 'Henry'], unique=True)  # Insert multiple data into the 'names' table
    
    for name, uid in zip(await conn.get_data('names'), await conn.get_data('uids')):  # Iterate over the data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    await conn.delete_from_table('uids', 9234)  # Delete the data '9234' from the 'uids' table
    await conn.delete_from_table('names', 'John')  # Delete the data 'John' from the 'names' table
    
    for name, uid in zip(await conn.get_data('names'), await conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    await conn.update_data('uids', 3895345, 50505)  # Update the data '3895345' to '50505' in the 'uids' table
    await conn.update_data('names', 'Michael', 'Dan')  # Update the data 'Michael' to 'Dan' in the 'names' table
    
    for name, uid in zip(await conn.get_data('names'), await conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    await conn.insert_into_table('uids', 8023)  # Insert a single data '8023' into the 'uids' table
    await conn.insert_into_table('names', 'James')  # Insert a single data 'James' into the 'names' table
    
    for name, uid in zip(await conn.get_data('names'), await conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    await conn.delete_table('uids')  # Delete the 'uids' table
    await conn.delete_table('names')  # Delete the 'names' table
    await conn.create_tables(['test1', 'test2', 'test3']) # Create multiple tables
    await conn.delete_tables(['test1', 'test2', 'test3']) # Delete multiple tables

asyncio.run(main())  # Run the async example

# sync example
def sync_main():
    conn = pyweb_db.connection('database') # Create connection
    
    conn.create_table('uids')  # Create a table named 'uids'
    conn.create_table('names')  # Create a table named 'names'
    
    conn.insert_datas_into_table('uids', [9234, 3895345, 4358, 340858340], unique=True)  # Insert multiple data into the 'uids' table
    conn.insert_datas_into_table('names', ['John', 'Michael', 'Daniel', 'Henry'], unique=True)  # Insert multiple data into the 'names' table
    
    for name, uid in zip(conn.get_data('names'), conn.get_data('uids')):  # Iterate over the data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    conn.delete_from_table('uids', 9234)  # Delete the data '9234' from the 'uids' table
    conn.delete_from_table('names', 'John')  # Delete the data 'John' from the 'names' table
    
    for name, uid in zip(conn.get_data('names'), conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    conn.update_data('uids', 3895345, 50505)  # Update the data '3895345' to '50505' in the 'uids' table
    conn.update_data('names', 'Michael', 'Dan')  # Update the data 'Michael' to 'Dan' in the 'names' table
    
    for name, uid in zip(conn.get_data('names'), conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    conn.insert_into_table('uids', 8023)  # Insert a single data '8023' into the 'uids' table
    conn.insert_into_table('names', 'James')  # Insert a single data 'James' into the 'names' table
    
    for name, uid in zip(conn.get_data('names'), conn.get_data('uids')):  # Iterate over the updated data in both tables
        print(f'{name} - {uid}')  # Print the name and UID
    
    print()
    
    conn.delete_table('uids')  # Delete the 'uids' table
    conn.delete_table('names')  # Delete the 'names' table
    conn.create_tables(['test1', 'test2', 'test3']) # Create multiple tables
    conn.delete_tables(['test1', 'test2', 'test3']) # Delete multiple tables

sync_main()  # Run the sync example