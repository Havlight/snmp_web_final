from pysnmp.hlapi import *


def split_varBind(varBind):
    varBind = str(varBind)
    parts = varBind.split("::")
    mib = parts[0]
    oid = parts[1].split(" = ")[0]
    value = parts[1].split(" = ")[1]

    result = {
        "mib": mib,
        "oid": oid,
        "value": value
    }

    return result


def get_snmp(target, oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
            r = split_varBind(varBind)
            return r


def walk_snmp(target, oid):
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),  # Replace 'public' with your community string
        UdpTransportTarget((target, 161)),  # Replace with your switch's IP address and port
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lookupMib=True,
        lexicographicMode=False
    )

    result = []
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print("errorIndication", errorIndication)
            break
        elif errorStatus:
            print("errorStatus", '%s at %s' % (errorStatus.prettyPrint(),
                                               errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
                result.append(split_varBind(varBind))
    # print(result)
    return result


def set_snmp(target, oid, value, type_):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(
            SnmpEngine(),
            CommunityData('public', mpModel=0),  # Replace 'private' with your community string with write access
            UdpTransportTarget((target, 161)),  # Replace with your switch's IP address and port
            ContextData(),
            ObjectType(ObjectIdentity(oid), type_(value))
        )
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print("set:")
            print(' = '.join([x.prettyPrint() for x in varBind]))
            print("\n")
            return split_varBind(varBind)


def get_cdp_tables(host, table_entries, number=1000):
    result = []
    start = 0
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData('public'),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              # cdpCacheTable
                              *table_entries,
                              lexicographicMode=False):

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            # with open('cdp.txt', 'a', 1) as cdp_file:
            #     cdp_file.write(host + '\n')
            #     for i in range(len(varBinds)):
            #         cdp_file.write(str(varBinds[i]) + '\n')
            row = []
            for i in range(len(varBinds)):
                print(str(varBinds[i]))
                r = split_varBind(varBinds[i])
                row.append(r)
            print('\n')
            result.append(row)
            start += 1
            if start >= number:
                break
    # print(result)
    return result


def set_table_entry(target, base_oid, row, col, value, type_):
    real_old = base_oid + "." + str(row) + "." + str(col)
    set_snmp(target, real_old, value, type_)


if __name__ == "__main__":
    target = '10.91.0.27'  # 替換為你的交換機IP
    community = 'public'
    oid = '1.3.6.1.4.1.890.1.5.8.18.2.2.1'
    table_entries = (
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.1')),  # table idx
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.2')),  #
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.3')),  #
    )

    # get_snmp(target, oid)
    # walk_snmp(target, oid)
    # set_snmp(target, oid, 1, Integer)
    # set_table_entry(target, oid, 2, 2, 300, Integer)
    print(get_cdp_tables(target, table_entries))
