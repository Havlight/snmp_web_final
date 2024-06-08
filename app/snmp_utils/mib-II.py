from app.snmp_utils.main import *

target = '10.91.0.27'


def get_systemInfos():
    systemInfos = [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.' + str(i))) for i in range(1, 8)]
    return get_cdp_tables(target, systemInfos)


def get_ifTable():
    ifTableEntries = [ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.' + str(i))) for i in range(1, 23)]
    return get_cdp_tables(target, ifTableEntries)


def get_ipInfos():
    ipInfos = [ObjectType(ObjectIdentity('1.3.6.1.2.1.4.' + str(i))) for i in range(1, 20)]
    return get_cdp_tables(target, ipInfos)


def get_ipAddrTable():
    ipAddrEntries = [ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.' + str(i))) for i in range(1, 6)]
    return get_cdp_tables(target, ipAddrEntries)


def get_ipRouteTable():
    ipRouteEntry = [ObjectType(ObjectIdentity('1.3.6.1.2.1.4.21.1.' + str(i))) for i in range(1, 14)]
    return get_cdp_tables(target, ipRouteEntry)


def get_ipNetToMediaTable():
    ipNetToMediaEntry = [ObjectType(ObjectIdentity('1.3.6.1.2.1.4.22.1.' + str(i))) for i in range(1, 5)]
    return get_cdp_tables(target, ipNetToMediaEntry)


def get_icmpInfos():
    icmpInfos = [ObjectType(ObjectIdentity('1.3.6.1.2.1.5.' + str(i))) for i in range(1, 27)]
    return get_cdp_tables(target, icmpInfos)[0]




