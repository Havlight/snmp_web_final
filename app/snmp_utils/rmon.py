from app.snmp_utils.main import *

target = '10.91.0.27'


def get_etherStatsTable():
    etherStatsEntries = [ObjectType(ObjectIdentity('1.3.6.1.2.1.16.1.1.1.' + str(i))) for i in range(1, 22)]
    return get_cdp_tables(target, etherStatsEntries)


def get_etherHistoryTable(number=1000):
    etherHistoryTableEntries = [ObjectType(ObjectIdentity('1.3.6.1.2.1.16.2.2.1.' + str(i))) for i in range(1, 16)]
    return get_cdp_tables(target, etherHistoryTableEntries, number)


def get_alarmTable():
    alarmEntries = [ObjectType(ObjectIdentity('1.3.6.1.2.1.16.3.1.1.1.' + str(i))) for i in range(1, 13)]
    return get_cdp_tables(target, alarmEntries)


# print(len(get_etherHistoryTable(12)))
