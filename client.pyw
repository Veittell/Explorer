from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory as ClFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from time import sleep
import os


class Client(Protocol):
    def __init__(self):
        self.ind = 0

    def connectionMade(self):
        self.transport.write(f"Pass".encode("utf-8"))

    def dataReceived(self, data):
        data = data.decode("utf-8")
        if data == "1" or data == "3" or data == "4":
            with open("data\\ind_0", "w", encoding="utf-8") as data_out:
                data_out.write(data)
        elif data != "Pass":
            with open("data\\ind_0", "w", encoding="utf-8") as data_out:
                data_out.write("2")
            with open("data\\data_i", "w", encoding="utf-8") as data_out:
                data_out.write(data)
        while True:
            sleep(0.75)
            with open("data\\ind_0", "r", encoding="utf-8") as read_ind:
                check = read_ind.read()
                if check == "6":
                    with open("data\\data_o", "r", encoding="utf-8") as read_data_o:
                        with open("data\\ind_0", "w", encoding="utf-8") as ind:
                            ind.write("5")
                        self.transport.write(f"mftp {read_data_o.read()}".encode("utf-8"))
                        break
                if check == "7":
                    with open("data\\data_o", "r", encoding="utf-8") as read_rftp:
                        with open("data\\ind_0", "w", encoding="utf-8") as ind:
                            ind.write("5")
                        self.transport.write(f"{read_rftp.read()}".encode("utf-8"))
                        break

        # if data != "Pass_0" and data[:5] == "mftp ":
        #     if int(data.split("|")[0].split(":")[3]) == self.ind:
        #         with open("data\\data_o", "w", encoding="utf-8") as write_data_in:
        #             write_data_in.write(data)
        #         with open("data\\ind_0", "w", encoding="utf-8") as write_ind:
        #             write_ind.write("2")
        # elif data != "Pass_0" and data[:19] == "All data save mftp " or data != "Pass_0" and data == "Data update":
        #     if int(data.split("|")[0].split(":")[2]) == self.ind:
        #         with open("data\\data_o", "w", encoding="utf-8") as write_data_in:
        #             write_data_in.write(data)
        #         with open("data\\ind_0", "w", encoding="utf-8") as write_ind:
        #             write_ind.write("2")
        # if data[:5] == "ind: " and self.ind == 0:
        #     self.ind = int(data.split("ind: ")[1])
        # while True:
        #     sleep(0.1)
        #     with open("data\\ind_0", "r", encoding="utf-8") as check_i:
        #         check_0 = check_i.read()
        #     if check_0 == "1":
        #         with open("data\\ind_0", "w", encoding="utf-8") as write_i:
        #             write_i.write("0")
        #         with open("data\\data_i", "r", encoding="utf-8") as read_d_i:
        #             data_all = read_d_i.read()
        #             data_all = data_all.split("|")[0] + f":{self.ind}|" + data_all.partition("|")[2]
        #             data_all_split = data_all.split("|")
        #             for data_0 in data_all_split[2:]:
        #                 with open(data_0, "r", encoding="utf-8") as read_f:
        #                     data_r = read_f.read()
        #                     data_all += f"|{data_r}"
        #             self.transport.write(f"{data_all}|{len(data_all_split[2:])}".encode("utf-8"))
        #             break
        #     elif check_0 == "3":
        #         with open("data\\ind_0", "w", encoding="utf-8") as write_i:
        #             write_i.write("0")
        #         with open("data\\data_i", "r", encoding="utf-8") as read_d_i:
        #             read_d_i = read_d_i.read()
        #         self.transport.write(f"{read_d_i}:{self.ind}".encode("utf-8"))
        #         break


class ClientFactory(ClFactory):
    def buildProtocol(self, addr):
        return Client()


def clear():
    os.system("CLS")


def start():
    if __name__ == "__main__":
        endpoint = TCP4ClientEndpoint(reactor, "localhost", 2105)
        endpoint.connect(ClientFactory())
        reactor.run()


start()
