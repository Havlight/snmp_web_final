from app.snmp_utils.main import *
from pysnmp.proto import rfc1902


def get_securedClientTable():
    target = '10.91.0.27'  # 替换为你的交换机IP
    table_entries = (
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.15.2.1.1')),  # table idx
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.15.2.1.2')),  #
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.15.2.1.3')),  #
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.15.2.1.4')),  #
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.15.2.1.5')),  #
    )

    return get_cdp_tables(target, table_entries)


def enable_securedClient(value, row=1):
    """
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '	1.3.6.1.4.1.890.1.5.8.18.15.2.1.2.' + str(row)
    # value = 1 if enable else 2  # 1表示启用(enabled)，2表示禁用(disabled)
    return set_snmp(target, oid, value, Integer)


def set_ClientStartIp(value, row=1):
    """
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.15.2.1.3.' + str(row)
    return set_snmp(target, oid, value, rfc1902.IpAddress)


def set_ClientEndIp(value, row=1):
    """
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.15.2.1.4.' + str(row)
    return set_snmp(target, oid, value, rfc1902.IpAddress)


def set_ClientService(value, row=1):
    """
    telnet(0),
    ftp(1),
    http(2),
    icmp(3),
    snmp(4),
    ssh(5),
    https(6)
    ex: set_ClientService(bytes.fromhex('00'), row=2)
    """

    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.15.2.1.5.' + str(row)
    return set_snmp(target, oid, value, rfc1902.Bits)


# rate in Kbit/s.  The range of FE port is between 64 and 100,000. For GE port, the range is between 64 and 1000,000
# 先設定end
if __name__ == "__main__":
    # enable_securedClient(False, 2)
    # set_ClientEndIp('0.0.0.0', 2)
    # set_ClientStartIp('0.0.0.0', 2)
    # set_ClientService(bytes.fromhex('00'), row=2)
    # get_securedClientTable()
    oid = '1.3.6.1.2.1.16.2.1.1'
    entries = [ObjectType(ObjectIdentity(oid + '.' + str(i))) for i in
               range(2, 5 + 1)]
    print(get_cdp_tables('10.91.0.27', entries))
