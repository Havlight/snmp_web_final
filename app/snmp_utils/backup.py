import json
from app.snmp_utils.main import *


def backup_switch(target, backup_oid, filename):
    config = {}
    for oid in backup_oid:
        response = get_snmp(target, oid)
        config[oid] = response['value']

    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)


target = '10.91.0.27'
backup_oid = [
    '1.3.6.1.4.1.890.1.5.8.18.2.1.0',
    # 添加更多的OID以備份更多的配置
    # 注意不能加入唯讀的oid否則無法restore回去
]


def restore_switch(target, filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    try:
        for oid, value in config.items():
            set_snmp(target, oid, value, Integer32)
    except:
        print("確認存檔的oid是否有唯獨的檔案，如果有刪除所有唯獨的oid並重新backup一次")


if __name__ == "__main__":
    pass
    # backup_filename = 'switch_backup.json'
    # backup_switch(target, backup_oid, backup_filename)
    # print(f'Backup completed. Configuration saved to {backup_filename}')
    # set_snmp(target,'1.3.6.1.4.1.890.1.5.8.18.2.1.0',2,Integer32)
    # restore_switch(target,backup_filename)
    # print('Configuration restored.')
    # get_snmp(target,'1.3.6.1.4.1.890.1.5.8.18.2.1.0')
    # set_snmp(target,'1.3.6.1.4.1.890.1.5.8.18.2.1.0',1,Integer32)
