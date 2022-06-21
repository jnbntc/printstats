from global_setup import *
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

def __init__ (self):
    self.conn = pymysql.connect(MY_DB_SERVER, MY_DB_USER, MY_DB_PASS, MY_DB_DB, use_unicode=True, charset="utf8")

SYSNAME = '1.3.6.1.2.1.43.10.2.1.4.1.1'

host = '192.168.3.26'
snmp_ro_comm = 'public'

# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
auth = cmdgen.CommunityData(snmp_ro_comm)

# Define the CommandGenerator, which will be used to send SNMP queries
cmdGen = cmdgen.CommandGenerator()

# Query a network device using the getCmd() function, providing the auth object, a UDP transport
# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    auth,
    cmdgen.UdpTransportTarget((host, 161)),
    cmdgen.MibVariable(SYSNAME),
    lookupMib=False,
)

# Check if there was an error querying the device
if errorIndication:
    sys.exit()

# We only expect a single response from the host for sysName, but varBinds is an object
# that we need to iterate over. It provides the OID and the value, both of which have a
# prettyPrint() method so that you can get the actual string data
for oid, val in varBinds:
    print(oid.prettyPrint(), val.prettyPrint())


# Prueba modulo de configuracíon

print(MY_DB_DB)
