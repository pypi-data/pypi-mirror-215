It is a simple JSON-based database library. It can be used both synchronously and asynchronously.

Example of synchronous use:
conn = pyweb_database.connection(database_name) # Creating a database connection
conn.create_table(table_name)  # Create a table
conn.insert_datas_into_table(table_name, [9234, 3895345, 4358, 340858340], unique=True)  # Insert multiple unique data into table
conn.delete_from_table(table_name, 9234)  # Delete the data '9234' from table
conn.update_data(table_name, 3895345, 50505)  # Update the data '3895345' to '50505' in table
conn.get_data(table_name) # Getting content from table
conn.insert_into_table(table_name, 8023)  # Insert a single data '8023' into table
conn.delete_table(table_name)  # Delete table

Example of asynchronous use:
conn = pyweb_database.connection(database_name) # Creating a database connection
await conn.create_table(table_name)  # Create a table
await conn.insert_datas_into_table(table_name, [9234, 3895345, 4358, 340858340], unique=True)  # Insert multiple unique data into table
await conn.delete_from_table(table_name, 9234)  # Delete the data '9234' from table
await conn.update_data(table_name, 3895345, 50505)  # Update the data '3895345' to '50505' in table
await conn.get_data(table_name) # Getting content from table
await conn.insert_into_table(table_name, 8023)  # Insert a single data '8023' into table
await conn.delete_table(table_name)  # Delete table