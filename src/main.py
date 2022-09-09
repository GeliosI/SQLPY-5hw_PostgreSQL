from art import tprint
from client_db import ClientDB


def main():
    tprint("ClientDB", font='bulbhead')

    cdb = ClientDB()
    cdb.create_table()

    james_id = cdb.add_client(client_name="James", client_surname="Smith", client_email="JamesSmith@ya.ru", clients_phone="79991110001")
    robert_id = cdb.add_client(client_name="Robert", client_surname="Johnson", client_email="RobertJohnson@ya.ru")
    william_id = cdb.add_client(client_name="William", client_surname="Miller", client_email="WilliamMiller@ya.ru", clients_phone="79991110003")

    cdb.add_client_phone(client_id=robert_id, clients_phone="79991110002")
    cdb.add_client_phone(client_id=william_id, clients_phone="79991110004")

    cdb.del_client_phone(client_id=robert_id, clients_phone="79991110002")

    cdb.change_client(client_id=james_id, client_name="Joseph", clients_phone="79991110005")

    cdb.del_client(client_id=william_id)

    cdb.find_client(client_name="william_id")
    cdb.find_client(client_name="Joseph", clients_phone="79991110005")


if __name__ == '__main__':
    main()