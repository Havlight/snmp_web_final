from pysnmp.hlapi import *
import time
from app.snmp_utils.main import *

target = '10.91.0.27'  # 替换为你的交换机IP地址
def monitor_error(target, oid_prefix, description, interface_indices, interval):
    error_data = {index: 0 for index in interface_indices}
    results = []

    # 获取初始值
    for index in interface_indices:
        oid = f'{oid_prefix}.{index}'
        initial_error = get_snmp(target, oid)
        if initial_error is None:
            print(f"Failed to get initial SNMP data for interface {index}")
            continue
        error_data[index] = int(initial_error['value'])

    time.sleep(interval)

    # 获取最终值并计算错误率
    for index in interface_indices:
        oid = f'{oid_prefix}.{index}'
        final_error = get_snmp(target, oid)
        if final_error is None:
            print(f"Failed to get final SNMP data for interface {index}")
            continue
        error_diff = int(final_error['value']) - error_data[index]
        error_rate = error_diff / interval
        port_status = {
            "port": index,
            # description: {
            "error_diff": error_diff,
            "error_rate": error_rate
            # }
        }
        results.append(port_status)
    return results


def get_InDiscards(interval):
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]
    return monitor_error(target, '1.3.6.1.2.1.2.2.1.13', 'In_discard', interface_indices, interval)


def get_OutDiscards(interval):
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]
    return monitor_error(target, '1.3.6.1.2.1.2.2.1.19', 'Out_discard', interface_indices, interval)


def get_InErrors(interval):
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]
    return monitor_error(target, '1.3.6.1.2.1.2.2.1.14', 'In_error', interface_indices, interval)


def get_OutErrors(interval):
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]
    return monitor_error(target, '1.3.6.1.2.1.2.2.1.20', 'Out_errors', interface_indices, interval)

if __name__ == "__main__":

    Indiscard = get_InDiscards(1)
    print("In Discard:", Indiscard)

    Outdiscard = get_OutDiscards(1)
    print("Out Discard:", Outdiscard)

    Inerror = get_InErrors(1)
    print("In Error:", Inerror)

    Outerror = get_OutErrors(1)
    print("Our Error:", Outerror)


