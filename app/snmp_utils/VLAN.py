from app.snmp_utils.main import *


def create_vlan(target, vlan_id, vlan_name, ports):
    # VLAN行状态OID
    vlan_row_status_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.5.{vlan_id}'
    set_snmp(target, vlan_row_status_oid, 4, Integer)  # 4 表示 'createAndGo'

    # VLAN名称OID
    vlan_name_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.1.{vlan_id}'
    set_snmp(target, vlan_name_oid, vlan_name, OctetString)

    # 设置 SNMPv2-SMI::mib-2.17.7.1.4.3.1.2.{vlan_id} 为 0xff
    vlan_egress_ports_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.2.{vlan_id}'
    set_snmp(target, vlan_egress_ports_oid, b'\xff', OctetString)

    # VLAN禁止出口端口OID
    vlan_forbidden_egress_ports_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.3.{vlan_id}'
    set_snmp(target, vlan_forbidden_egress_ports_oid, b'\x00\x00\x00\x00', OctetString)

    # VLAN端口配置OID(untag)
    vlan_untagged_ports_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.4.{vlan_id}'
    untagged_bitmap = calculate_port_bitmap(ports)
    print(untagged_bitmap)
    set_snmp(target, vlan_untagged_ports_oid, untagged_bitmap, OctetString)

    return set_snmp(target, vlan_row_status_oid, 1, Integer)  # 1 表示 'active'


def get_vlan_info():
    return walk_snmp('10.91.0.27', '1.3.6.1.2.1.17.7.1.4.3.1')


def delete_vlan(target, vlan_id):
    vlan_row_status_oid = f'1.3.6.1.2.1.17.7.1.4.3.1.5.{vlan_id}'
    return set_snmp(target, vlan_row_status_oid, 6, Integer)  # 6 表示 'destroy


def calculate_port_bitmap(ports):
    bitmap = 0
    for port in ports:
        bitmap |= (1 << (port - 1))  # 将位元设为1，表示这个端口被设置

    # 将位图转换为二进制字符串
    bitmap_str = format(bitmap, '08b')  # 将位图转换为二进制字符串，不足8位的补0
    print(f'Binary string before reversal: {bitmap_str}')

    # 反转二进制字符串
    reversed_bitmap_str = bitmap_str[::-1]
    print(f'Binary string after reversal: {reversed_bitmap_str}')

    # 将反转后的二进制字符串转换回整数
    reversed_bitmap = int(reversed_bitmap_str, 2)

    # 将整数转换为字节
    bitmap_bytes = reversed_bitmap.to_bytes((len(reversed_bitmap_str) + 7) // 8, byteorder='big')
    print(f'Bytes: {bitmap_bytes}')
    return bitmap_bytes


if __name__ == "__main__":
    # 定义交换机的IP地址、VLAN ID和VLAN名称
    target = '10.91.0.27'
    vlan_id = 2
    vlan_name = 'VLAN2'
    ports = [7, 6, 3, 2]  # 假設你想設置這些端口
    #
    # create_vlan(target, vlan_id, vlan_name,ports)
    # delete_vlan('10.91.0.27',2)
    get_vlan_info()
