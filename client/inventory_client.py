from __future__ import print_function

import grpc

import library_pb2
import library_pb2_grpc


class InventoryClient:
    def __init__(self, host, port):
        # connect to localhost grpc server
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = library_pb2_grpc.InventoryServiceStub(self.channel)

    def getBook(self, isbn):
        response = self.stub.GetBook(library_pb2.GetBookRequest(ISBN=isbn))
        return response
