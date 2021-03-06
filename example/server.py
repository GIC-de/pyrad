#!/usr/bin/python
from __future__ import print_function
from pyrad import dictionary, packet, server
import logging

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")


class FakeServer(server.Server):

    def _HandleAuthPacket(self, pkt):
        server.Server._HandleAuthPacket(self, pkt)

        print("Received an authentication request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt, **{
            "Service-Type": "Framed-User",
            "Framed-IP-Address": '192.168.0.1',
            "Framed-IPv6-Prefix": "fc66::1/64"
        })
        reply.code = packet.AccessAccept
        self.SendReplyPacket(pkt.fd, reply)

    def _HandleAcctPacket(self, pkt):
        server.Server._HandleAcctPacket(self, pkt)

        print("Received an accounting request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)


if __name__ == '__main__':

    # create server and read dictionary
    srv = FakeServer(dict=dictionary.Dictionary("dictionary"))

    # add clients (address, secret, name, authport=1812, acctport=1813)
    srv.hosts["127.0.0.1"] = server.RemoteHost("127.0.0.1", b"Kah3choteereethiejeimaeziecumi", "localhost")
    srv.BindToAddress("")

    # start server
    srv.Run()
