
class PortScanResponse:
    def __init__(self, port_number, status):
        self.port_number = port_number
        self.port_status = status

    def pretty_print(self):
        if self.port_status:
            print("Port {}:         Open".format(self.port_number))
        else:
            print("Port {}:       Closed".format(self.port_number))