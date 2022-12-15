from inventory_client import InventoryClient


def get_titles(grpc_client_param, isbn_list_param):
    output = []
    for isbn in isbn_list_param:
        book_details = grpc_client_param.getBook(isbn)
        output.append(book_details.title)

    return output


if __name__ == '__main__':
    grpc_client = InventoryClient('localhost', '50051')
    isbn_list = ["1", "2"]
    title_list = get_titles(grpc_client, isbn_list)
    print(title_list)
