
from concurrent import futures
import logging

import grpc
import library_pb2
import library_pb2_grpc

# Creating dummy database at start
books = []
inventory = []

book1 = library_pb2.Book()
book1.ISBN = "1"
book1.title = "girl on a blue train"
book1.author = "Agatha Christie"
book1.genre = library_pb2.MURDER_MYSTERY
book1.publishing_year = 1965

books.append(book1)
inventory1 = library_pb2.InventoryItem()
inventory1.inventory_number = "1"
inventory1.book.CopyFrom(book1)
inventory1.status = library_pb2.AVAILABLE
inventory.append(inventory1)

book2 = library_pb2.Book()
book2.ISBN = "2"
book2.title = "The royals"
book2.author = "M Bashir"
book2.genre = library_pb2.HISTORY
book2.publishing_year = 1982

books.append(book2)
inventory2 = library_pb2.InventoryItem()
inventory2.inventory_number = "2"
inventory2.book.CopyFrom(book2)
inventory2.status = library_pb2.AVAILABLE
inventory.append(inventory2)

# Library class that subclasses the inventory service servicer
class Library(library_pb2_grpc.InventoryServiceServicer):

    # Implementation of the create book function
    def CreateBook(self, request, context):
        # get book details from the request
        isbn = request.ISBN
        title = request.title
        author = request.author
        genre = request.genre
        year = request.publishing_year

        # empty arguments
        if isbn == "" or title == "":
            resp = library_pb2.CreateBookResponse()
            resp.ISBN = ""
            resp.error_message_1 = "ISBN or Title can not be blank"
            return resp

        # check if the isbn is already present
        for book in books:
            if book.ISBN == isbn:
                resp = library_pb2.CreateBookResponse()
                resp.ISBN = isbn
                resp.error_message_1 = "ISBN should be unique"
                return resp

        # create new book
        new_book = library_pb2.Book()
        new_book.ISBN = isbn
        new_book.title = title
        new_book.author = author
        new_book.genre = genre
        new_book.publishing_year = year
        books.append(new_book)
        new_inventory = library_pb2.InventoryItem()
        new_inventory.inventory_number = isbn
        new_inventory.book.CopyFrom(new_book)
        new_inventory.status = library_pb2.AVAILABLE
        inventory.append(new_inventory)

        # return response with isbn parameter
        return library_pb2.CreateBookResponse(ISBN=isbn)

    # Implementation of get book method
    def GetBook(self, request, context):
        # get isbn of book to be found
        isbn = request.ISBN

        # find the book in database
        for book in books:
            if book.ISBN == isbn:
                resp = library_pb2.GetBookResponse()
                resp.ISBN, resp.title, resp.author, resp.genre, resp.publishing_year = \
                    book.ISBN, book.title, book.author, book.genre, book.publishing_year

                for item in inventory:
                    if item.book == book:
                        resp.status = item.status

                return resp

        # return the get book response
        resp = library_pb2.GetBookResponse()
        resp.ISBN = isbn
        resp.error_message_2 = "Book not found!"
        return resp


# Start the server using this method.
def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_InventoryServiceServicer_to_server(Library(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


# Call server function
if __name__ == '__main__':
    logging.basicConfig()
    serve()
