from ninja_extra import NinjaExtraAPI, api_controller, route
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

from app.schemas import MacTableSchema, GenericMibResultSchema, PortWarningSchema, PortRateSchema, Error, PortError
from app.snmp_utils import mac_table, port_traffic, port_status, rate_limit, rmon, securedClient, test_lost_packet, main

app = NinjaExtraAPI()


@api_controller('/search', tags=['search oid'])
class SearchController:
    @route.get('/walk/{str:oid}', response={200: list[GenericMibResultSchema], 404: Error})
    def walk(self, oid: str):
        r = main.walk_snmp("10.91.0.27", oid)
        if r:
            return r
        else:
            return 404, {"message": "Not found"}

    @route.get('/get/{str:oid}', response={200: GenericMibResultSchema, 404: Error})
    def get(self, oid: str):
        r = main.get_snmp("10.91.0.27", oid)
        if r:
            return r
        else:
            return 404, {"message": "Not found"}

    @route.get('/table/{str:oid}/{int:begin}/{int:end}', response={200: list[list[GenericMibResultSchema]], 404: Error})
    def table(self, oid: str, begin: int, end: int):
        entries = [ObjectType(ObjectIdentity(oid + '.' + str(i))) for i in
                   range(begin, end + 1)]
        r = main.get_cdp_tables("10.91.0.27", entries)
        if r:
            return r
        else:
            return 404, {"message": "Not found"}


@api_controller('/mac', tags=['mac table'])
class MacContorller:
    @route.get('/macTable', response=list[MacTableSchema])
    def get_mac_table(self):
        return mac_table.get_clean_mac_table()


@api_controller('/portStatus', tags=['port status'])
class PortStatusController:
    @route.get('/State', response=list[GenericMibResultSchema])
    def get_port_state(self):
        return port_status.get_port_state()

    @route.get('/expectedState', response=list[GenericMibResultSchema])
    def get_port_expect_state(self):
        return port_status.get_port_expect_state()

    @route.get('/warning', response=list[PortWarningSchema])
    def get_warning(self):
        return port_status.port_error()

    @route.put('/expectedState/{int:port}/{int:value}',
               response={200: GenericMibResultSchema, 304: Error})
    def set_expected_state(self, port: int, value: int):
        r = port_status.set_port_expect_state(port, value)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}


@api_controller('/portTraffic', tags=['port traffic'])
class TrafficController:
    @route.get('/rate', response=list[PortRateSchema])
    def get_rate(self):
        return port_traffic.monitor(1)

    @route.get('/inOctets', response=list[GenericMibResultSchema])
    def get_inOctets(self):
        return port_traffic.get_in_octets()

    @route.get('/outOctets', response=list[GenericMibResultSchema])
    def get_outOctets(self):
        return port_traffic.get_out_octets()


@api_controller('/portLimit', tags=['port limit'])
class LimitController:
    @route.get('/globalState', response=GenericMibResultSchema)
    def get_global_state(self):
        return rate_limit.get_rateLimitState()

    @route.get('/table', response=list[list[GenericMibResultSchema]])
    def get_rateLimitPortTable(self):
        return rate_limit.get_rateLimitPortTable()

    @route.put('/globalState/{int:value}', response={200: GenericMibResultSchema, 304: Error})
    def change_global_state(self, value: int):
        r = rate_limit.enable_all_rate_limit(value)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/table/{int:port}/{int:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_port_rate_limit(self, port: int, value: int):
        r = rate_limit.enable_port_rate_limit(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/inRate/{int:port}/{int:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_inRate(self, port: int, value: int):
        r = rate_limit.set_port_In_rate_limit(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/outRate/{int:port}/{int:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_outRate(self, port: int, value: int):
        r = rate_limit.set_port_Out_rate_limit(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}


@api_controller('/rmon', tags=['rmon'])
class Rmon:
    @route.get('/etherStatsTable', response=list[list[GenericMibResultSchema]])
    def get_etherStatsTable(self):
        return rmon.get_etherStatsTable()

    @route.get('/etherHistoryTable', response=list[list[GenericMibResultSchema]])
    def get_HistoryTable(self):
        return rmon.get_etherHistoryTable()

    @route.get('/etherHistoryTable/{int:number}', response=list[list[GenericMibResultSchema]])
    def get_HistoryTable(self, number: int):
        return rmon.get_etherHistoryTable(number)


@api_controller('/securedClient', tags=['secured client'])
class SecuredClient:
    @route.get('/table', response=list[list[GenericMibResultSchema]])
    def get_securedClientTable(self):
        return securedClient.get_securedClientTable()

    @route.put('/table/{int:port}/{int:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_securedClient(self, port: int, value: int):
        r = securedClient.enable_securedClient(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/startIp/{int:port}/{str:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_ClientStartIp(self, port: int, value: str):
        r = securedClient.set_ClientStartIp(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/endIp/{int:port}/{str:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_ClientEndIp(self, port: int, value: str):
        r = securedClient.set_ClientEndIp(value, port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}

    @route.put('/service/{int:port}/{str:value}', response={200: GenericMibResultSchema, 304: Error})
    def set_service(self, port: int, value: str):
        """
        ff 全開
        00 無
        """
        r = securedClient.set_ClientService(bytes.fromhex(value), port)
        if r:
            return 200, r
        else:
            return 304, {"message": "error"}


@api_controller('/packetLost', tags=['packet lost'])
class PacketLost:
    @route.get('/InDiscards', response=list[PortError])
    def get_InDiscards(self):
        return test_lost_packet.get_InDiscards(1)

    @route.get('/OutDiscards', response=list[PortError])
    def get_OutDiscards(self):
        return test_lost_packet.get_OutDiscards(1)

    @route.get('/InErrors', response=list[PortError])
    def get_InErrors(self):
        return test_lost_packet.get_InErrors(1)

    @route.get('/OutErrors', response=list[PortError])
    def get_OutErrors(self):
        return test_lost_packet.get_OutErrors(1)


app.register_controllers(SearchController, MacContorller, PortStatusController, TrafficController, LimitController,
                         Rmon, SecuredClient,
                         PacketLost)
