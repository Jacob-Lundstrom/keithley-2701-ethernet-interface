import socket

# NOTE Computer must be configured as follows:
# IP ASSIGNMENT - MANUAL
# IPV4
# IP ADDRESS  - 192.168.0.4
# SUBNET MASK - 254.254.254.0

class Keithley2701:
    def __init__(self, ip_address: str, port: int = 1394):
        self.ip_address = ip_address
        self.port = port
        self.socket = None

    def connect(self):
        """Establish a socket connection to the instrument."""
        try:
            self.socket = socket.create_connection((self.ip_address, self.port), timeout=5)
            print("Connected to Keithley 2701.")

            # Test the connection by sending *IDN?
            idn = self.query("*IDN?")
            print("Instrument ID:", idn)
        except socket.timeout:
            print("Connection timed out.")
        except socket.error as e:
            print(f"Socket error: {e}")

    def send(self, command: str):
        """Send a SCPI command to the instrument."""
        if self.socket:
            self.socket.sendall(f'{command}\n'.encode())
        else:
            raise ConnectionError("Socket is not connected.")

    def receive(self) -> str:
        """Receive data from the instrument."""
        if self.socket:
            return self.socket.recv(1024).decode().strip()
        else:
            raise ConnectionError("Socket is not connected.")

    def query(self, command: str) -> str:
        """Send a command and immediately return the response."""
        self.send(command)
        return self.receive()

    def close(self):
        """Close the socket connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Connection closed.")

    def scpi_MEASure(self, function: str, rang: str = "", res = "", clist:list = []) -> str:
        if function not in ["VOLT", "VOLTage",          # DCV
                            "VOLT:DC", "VOLTage:DC",    # DCV
                            "VOLT:AC", "VOLTage:AC",    # ACV
                            "CURR", "CURRent",          # DCI
                            "CURR:DC", "CURRent:DC",    # DCI
                            "CURR:AC", "CURRent:AC",    # ACI
                            "RES", "RESistance",        # 2-wire Resistance
                            "FRES", "FRESistance",      # 4-wire Resistance
                            "FREQ", "FREQuency",        # Frequency
                            "PER", "PERiod",            # Period
                            "TEMP", "TEMPerature",      # Temperature
                            "CONT", "CONTinuity"]:      # Continuity
            return
        
        query = ""
        
        if function in ["VOLT", "VOLTage", "VOLT:DC", "VOLTage:DC"]:
            query = "MEASure:VOLTage:DC?"
        
        if function in ["VOLT:AC", "VOLTage:AC"]:
            query = "MEASure:VOLTage:AC?"

        if function in ["CURR", "CURRent", "CURR:DC", "CURRent:DC"]:
            query = "MEASure:CURRent:DC?"

        if function in ["CURR:AC", "CURRent:AC"]:
            query = "MEASure:CURRent:AC?"

        if function in ["RES", "RESistance"]:
            query = "MEASure:RESistance?"

        if function in ["FRES", "FRESistance"]:
            query = "MEASure:FRESistance?"
        
        if function in ["FREQ", "FREQuency"]:
            query = "MEASure:FREQuency?"

        if rang != "":
            query += f" {rang}"
            if res != "":
                query += f", {res}"
        print(query)
        return self.query(query)
    
    def measure_voltage_dc(self):
        return
    
    def measure_voltage_ac(self):
        return
    
    def measure_current_dc(self):
        return
    
    def measure_current_ac(self):
        return
    
    def measure_resistance_2_wire(self):
        return
    
    def measure_resistance_4_wire(self):
        return

    def measure_frequency(self):
        return
    
    def measure_period(self):
        return
    
    def measure_temperature(self):
        return
    
    def measure_continuity(self):
        return


# Example usage
if __name__ == "__main__":
    kei = Keithley2701("192.168.0.2")
    kei.connect()
    print(kei.scpi_MEASure(function="VOLT:AC", rang="1e-1", res="0.000001"))
    kei.close()
