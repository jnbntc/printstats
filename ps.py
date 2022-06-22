from global_setup import *
import pymysql
import sys
from datetime import datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen

#def __init__ (self):
#conn = pymysql.connect(host=MY_DB_SERVER, user=MY_DB_USER, password=MY_DB_PASS, db=MY_DB_DB, use_unicode=True, charset="utf8")
conn = pymysql.connect(host=MY_DB_SERVER, user=MY_DB_USER, password=MY_DB_PASS, db=MY_DB_DB, charset="utf8")

SYSNAME = '1.3.6.1.2.1.43.10.2.1.4.1.1'

host = '192.168.3.28'
snmp_ro_comm = 'public'

# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)

# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
auth = cmdgen.CommunityData(snmp_ro_comm)

# Define the CommandGenerator, which will be used to send SNMP queries
cmdGen = cmdgen.CommandGenerator()

with conn.cursor() as cursor:
	# En este caso no necesitamos limpiar ningún dato
	cursor.execute("SELECT ip, id_printer FROM equipos;")
	# Con fetchall traemos todas las filas
	data = cursor.fetchall()

	# Recorrer e imprimir
for row in data:
# Query a network device using the getCmd() function, providing the auth object, a UDP transport
# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
      errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        auth,
        cmdgen.UdpTransportTarget((row[0], 161)),
        cmdgen.MibVariable(SYSNAME),
        lookupMib=False,
       )

      for oid, val in varBinds:
        #print(row[1], val.prettyPrint())
        with conn.cursor() as cursor2:
            id_printer = row[1]
            consulta = "UPDATE equipos SET ultima_lectura = %s WHERE id_printer = %s"
            cursor2.execute(consulta, (val.prettyPrint(), id_printer))
            print(consulta, (val.prettyPrint(), id_printer))
            print(row[1], val.prettyPrint())
            conn.commit()