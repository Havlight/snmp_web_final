import time
from .main import *

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
            return
        error_data[index] = int(initial_error['value'])
    time.sleep(interval)
    # 获取最终值并计算错误率
    for index in interface_indices:
        oid = f'{oid_prefix}.{index}'
        final_error = get_snmp(target, oid)
        if final_error is None:
            print(f"Failed to get final SNMP data for interface {index}")
            return
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


def get_monitor_alignment_errors(interval):  # 接收到的封包不是4bit或8bit
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 替换为你要监控的接口索引
    return monitor_error(target, '1.3.6.1.2.1.10.7.2.1.2', 'alignment_errors', interface_indices, interval)


def get_monitor_fcs_errors(interval):  # 驗算結果與發送方傳來的不一樣
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 替换为你要监控的接口索引
    return monitor_error(target, '1.3.6.1.2.1.10.7.2.1.3', 'fcs_errors', interface_indices, interval)


def get_monitor_frame_too_longs(interval):  # bit超過了一次傳輸的最大上限
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 替换为你要监控的接口索引
    return monitor_error(target, '1.3.6.1.2.1.10.7.2.1.6', 'frame_too_longs', interface_indices, interval)


def get_monitor_carrier_sense_errors(interval):  # 未能檢測到預期的載波信號。這種錯誤通常由線路噪聲或其他物理層問題引起
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 替换为你要监控的接口索引
    return monitor_error(target, '1.3.6.1.2.1.10.7.2.1.9', 'carrier_sense_errors', interface_indices, interval)


def get_monitor_late_collisions(interval):  # 在64bit之後發生了碰撞(正常來說碰撞會在前64bit)
    interface_indices = [1, 2, 3, 4, 5, 6, 7, 8]  # 替换为你要监控的接口索引
    return monitor_error(target, '1.3.6.1.2.1.10.7.2.1.13', 'late_collisions', interface_indices, interval)


if __name__ == "__main__":
    alignment_results = get_monitor_alignment_errors(1)
    # fcs_results = get_monitor_fcs_errors()
    # frame_too_long_results = get_monitor_frame_too_longs()
    # carrier_sense_error_results = get_monitor_carrier_sense_errors()
    # late_collision_results = get_monitor_late_collisions()

    print("Alignment Errors:", alignment_results)
    # print("FCS Errors:", fcs_results)
    # print("Frame Too Longs:", frame_too_long_results)
    # print("Carrier Sense Errors:", carrier_sense_error_results)
    # print("Late Collisions:", late_collision_results)
