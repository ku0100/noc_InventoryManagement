import sqlite3
import pandas as pd

conn = sqlite3.connect('inventory_db.db')
cursor = conn.cursor()

# Create table
cursor.execute('DROP TABLE inventory_db')
cursor.execute("CREATE TABLE inventory_db (tms_code, device_name, device_count, device_type)")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS01', 'Device01', 7, 'Supervisor')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS02', 'Device02', 2, 'Supervisor')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS03', 'Device03', 7, 'Module')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS04', 'Device04', 20, 'Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS05', 'Device05', 2, 'Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS06', 'Device06', 10, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS07', 'Device07', 0, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS08', 'Device08', 10, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS09', 'Device09', 11, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS10', 'Device10', 1, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS11', 'Device11', 1, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS12', 'Device12', 2, 'Power Supply')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS13', 'Device13', 8, 'Fan')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS14', 'Device14', 8, 'Fan')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS15', 'Device15', 1, 'Fan')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS16', 'Device16', 3, ' Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS17', 'Device17', 12, ' Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS18', 'Device18', 1, 'Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS19', 'Device19', 3, 'Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS20', 'Device20', 3, 'Switch')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS21', 'Device21', 1, 'Module')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS22', 'Device22', 1, 'Module')")
cursor.execute("INSERT INTO inventory_db VALUES ('TMS23', 'Device23', 4, 'Power Supply')")

conn.commit()

print('\n')

print(pd.read_sql_query('SELECT * FROM inventory_db', conn))

conn.close()
