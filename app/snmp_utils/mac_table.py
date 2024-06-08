from pysnmp.hlapi import *


def get_mac_table(target):
    mac_address_oid = '1.3.6.1.2.1.17.4.3.1.1'  # dot1dTpFdbAddress
    port_oid = '1.3.6.1.2.1.17.4.3.1.2'  # dot1dTpFdbPort
    status_oid = '1.3.6.1.2.1.17.4.3.1.3'  # dot1dTpFdbStatus

    mac_table = []

    for oid in [mac_address_oid, port_oid, status_oid]:
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData('public', mpModel=0),
                                  UdpTransportTarget((target, 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity(oid)),
                                  lexicographicMode=False):

            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    oid, value = varBind
                    mac_table.append((oid, value))

    return mac_table


def parse_mac_table(mac_table):
    mac_addresses = {}
    for oid, value in mac_table:
        oid_str = str(oid)
        if oid_str.startswith('1.3.6.1.2.1.17.4.3.1.1'):
            mac_idx = oid_str.split('.')[-6:]
            mac_address = ':'.join(format(int(x), '02x') for x in mac_idx)
            mac_addresses[mac_address] = {'port': None, 'status': None}
        elif oid_str.startswith('1.3.6.1.2.1.17.4.3.1.2'):
            mac_idx = oid_str.split('.')[-6:]
            mac_address = ':'.join(format(int(x), '02x') for x in mac_idx)
            if mac_address in mac_addresses:
                mac_addresses[mac_address]['port'] = int(value)
        elif oid_str.startswith('1.3.6.1.2.1.17.4.3.1.3'):
            mac_idx = oid_str.split('.')[-6:]
            mac_address = ':'.join(format(int(x), '02x') for x in mac_idx)
            if mac_address in mac_addresses:
                mac_addresses[mac_address]['status'] = int(value)

    return mac_addresses


def get_clean_mac_table():
    target = '10.91.0.27'  # 替換為你的交換機IP
    mac_table = get_mac_table(target)
    parsed_mac_table = parse_mac_table(mac_table)
    result = []
    for mac, info in parsed_mac_table.items():
        r = {}
        r['mac'] = mac
        r['port'] = info['port']
        r['status'] = info['status']
        result.append(r)
        print(f"MAC Address: {mac}, Port: {info['port']}, Status: {info['status']}")
    return result


if __name__ == "__main__":
    print(get_clean_mac_table())
