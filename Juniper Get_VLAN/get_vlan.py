from jnpr.junos import Device
from jnpr.junos import exception

'''
ToDo:
Add trunk support
Add device close
running junos-eznc==2.2.1

'''

class GetVLAN():
    def __init__(self):
        self.i = 1

    def connect(self, usr, pwd, ip):

        try:
            dev = Device(host=ip,
                         user=usr,
                         passwd=pwd,
                         normalize=True,
                         gather_facts=False
                         )
            dev.open()

        except exception.ConnectError as e:
            raise ValueError(f"Error connecting to {ip},\n {e}")

        return dev

    def close_device(self, dev):
        close = f"Closing connection to device {dev.facts['hostname']}"
        dev.close
        return close

    def IntVLAN(self, ip, usr, pwd, intf):

        dev = self.connect(usr, pwd, ip)

        try:
            responce = dev.rpc.get_ethernet_switching_interface_information(interface_name=intf)
        except exception.RpcError as e:
            raise ValueError(f"RPC Responce Error {e}")

        name = responce.find('.//interface-name').text
        status = responce.find('.//interface-state').text
        vlan_id = responce.find('.//interface-vlan-member-tagid').text
        vlan_name = responce.find('.//interface-vlan-name').text
        port_type = responce.find('.//interface-vlan-member-tagness').text

        if port_type == "tagged":
            for x in responce.xpath('.//interface-vlan-member-list/interface-vlan-member'):
               a  = x.findtext('interface-vlan-member-tagid')
               b  = x.findtext('interface-vlan-name')
        else:
            data = f"Name: {name}\nInterface Status: {status}\nVLAN Member: {vlan_id} ({vlan_name} mode {port_type})"
            return data











