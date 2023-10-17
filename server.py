from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint


class Server(protocol.Protocol):
    def connectionMade(self):
        print("New user.")

    def dataReceived(self, data):
        data_all = data.decode()
        stoper = 0
        print(data_all)
        if data_all == "Pass":
            self.transport.write(f"Pass".encode("utf-8"))
        if "|" in data_all:
            data_0 = data_all.split(":")[2].split("|")[0]
            with open("data_s\\data_all", "r", encoding="utf-8") as read_data:
                data_ftp = read_data.read()
            if data_ftp != "":
                for ftp in data_ftp.split("\nmftp "):
                    if ftp == "":
                        continue
                    data_1 = ftp.split(":")[2].split("|")[0]
                    if data_0 == data_1:
                        self.transport.write(f"3".encode("utf-8"))
                        stoper = 1
            if stoper == 0:
                with open("data_s\\data_all", "a", encoding="utf-8") as save_data:
                    save_data.write(data_all)
                self.transport.write(f"1".encode("utf-8"))
        elif data_all.lower()[:5] == "rftp ":
            with open("data_s\\data_all", "r", encoding="utf-8") as read_rftp:
                b = 0
                read_rftp = read_rftp.read()
                read_rftp = read_rftp.split("mftp ")
                for i in read_rftp:
                    print(data_all[5:], i.split("|")[0], i)
                    if data_all == "":
                        continue
                    elif str(data_all[5:]) == str(i.split("|")[0]):
                        b = 1
                        self.transport.write(f"{i}".encode("utf-8"))
                        break
                if b == 0:
                    self.transport.write(f"4".encode("utf-8"))

        # if data_all == "Pass":
        #     with open("data_s\\ind_l", "r", encoding="utf-8") as read_i:
        #         read_i = int(read_i.read()) + 1
        #     with open("data_s\\ind_l", "w", encoding="utf-8") as write_i:
        #         write_i.write(str(read_i))
        #         self.transport.write(f"ind: {read_i}".encode("utf-8"))
        # if data_all.lower()[:4] == "mftp":
        #     with open("data_s\\data_all", "r", encoding="utf-8") as read_f:
        #         read_f_0 = read_f.read()
        #     if data_all.split("|")[0] in read_f_0:
        #         with open("data_s\\data_all", "w", encoding="utf-8") as rewrite_ftp:
        #             read_f_0 = read_f_0.split("|FTP|")
        #             data_save: str = ""
        #             for i in read_f_0:
        #                 if data_all.split("|")[0] == i:
        #                     read_f_0.pop(read_f_0.index(i))
        #                 data_save += i
        #             rewrite_ftp.write("|FTP|" + data_all + data_save)
        #             self.transport.write(f"Data update".encode("utf-8"))
        #     else:
        #         with open("data_s\\data_all", "a", encoding="utf-8") as write_f:
        #             write_f.write(f"|FTP|{data_all}")
        #         data_0 = data_all.split("|")[0]
        #         self.transport.write(f"All data save {data_0}".encode("utf-8"))
        # elif data_all.lower()[:4] == "rftp":
        #     with open("data_s\\data_all", "r", encoding="utf-8") as read_rftp:
        #         b = 0
        #         read_rftp = read_rftp.read()
        #         read_rftp = read_rftp.split("|FTP|")[1:]
        #         for i in read_rftp:
        #             if data_all.rpartition(":")[0][5:] == i.split("|")[0][5:]:
        #                 b = 1
        #                 data = i.split("|")[0] + ":" + data_all.split(":")[3].split("|")[0] + "|" + i.partition("|")[2]
        #                 self.transport.write(f"{data}".encode("utf-8"))
        #                 break
        #         if b == 0:
        #             self.transport.write(f"FTP not found.".encode("utf-8"))
        # else:
        #     pass


class ServerFactory(ServFactory):
    def startFactory(self):
        print("Started [OK].")

    def buildProtocol(self, addr):
        return Server()


if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 2105)
    endpoint.listen(ServerFactory())
    reactor.run()
