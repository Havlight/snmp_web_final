from app.snmp_utils.main import *


def get_rateLimitState():
    target = '10.91.0.27'  # 替换为你的交换机IP
    return get_snmp(target, '1.3.6.1.4.1.890.1.5.8.18.2.1.0')


def enable_all_rate_limit(value):
    """
    启用或禁用交换机的速率限制
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.2.1.0'
    # value = 1 if enable else 2  # 1表示启用(enabled)，2表示禁用(disabled)
    return set_snmp(target, oid, value, Integer)


def get_rateLimitPortTable():
    target = '10.91.0.27'  # 替换为你的交换机IP
    table_entries = (
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.1')),  # table idx
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.2')),  #
        ObjectType(ObjectIdentity('1.3.6.1.4.1.890.1.5.8.18.2.2.1.3')),  #
    )

    return get_cdp_tables(target, table_entries)


def enable_port_rate_limit(value, row=1):
    """
    启用或禁用指定port交换机的速率限制
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '	1.3.6.1.4.1.890.1.5.8.18.2.2.1.1.' + str(row)
    # value = 1 if enable else 2  # 1表示启用(enabled)，2表示禁用(disabled)
    return set_snmp(target, oid, value, Integer)


def set_port_In_rate_limit(value, row=1):
    """
    启用或禁用指定port交换机的速率限制
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.2.2.1.2.' + str(row)
    if not 64 <= value <= 100000:
        print("fail")
        print("range of FE port is between 64 and 100,000")
        return
    return set_snmp(target, oid, value, Integer)


def set_port_Out_rate_limit(value, row=1):
    """
    启用或禁用指定port交换机的速率限制
    """
    target = '10.91.0.27'  # 替换为你的交换机IP
    oid = '1.3.6.1.4.1.890.1.5.8.18.2.2.1.3.' + str(row)
    if not 64 <= value <= 100000:
        print("fail")
        print("range of FE port is between 64 and 100,000")
        return
    return set_snmp(target, oid, value, Integer)


# rate in Kbit/s.  The range of FE port is between 64 and 100,000. For GE port, the range is between 64 and 1000,000

if __name__ == "__main__":
    port_number = 1  # 端口编号
    ingress_rate = 64000  # 入口速率限制，单位为Kbit/s
    egress_rate = 128000  # 出口速率限制，单位为Kbit/s
    target = '10.91.0.27'  # 替换为你的交换机IP

    # set_port_Out_rate_limit(64)
    # get_rateLimitPortTable()
    # get_rateLimitPortTable()
    get_rateLimitState()
