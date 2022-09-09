import psycopg2


class ClientDB:
    def __init__(self, database="netology_db", user="postgres", password="elephant"):
        self.conn = psycopg2.connect(database=database, user=user, password=password)
        self.cur = self.conn.cursor()

    def create_table(self):
        """Creates tables in the database"""

        print("[*] Tables are created...")
        try:
            self.cur.execute("""
                --begin-sql
                CREATE TABLE Сlients(
                    client_id SERIAL PRIMARY KEY,
                    client_name VARCHAR(40) NOT NULL,
                    client_surname VARCHAR(40) NOT NULL,
                    client_email VARCHAR(40) UNIQUE NOT NULL
                    );
                """)
            self.cur.execute("""
                --begin-sql
                CREATE TABLE Phones(
                    phone_id SERIAL PRIMARY KEY,
                    clients_phone VARCHAR(20) UNIQUE NOT NULL,
                    client_id INTEGER REFERENCES Сlients(client_id) ON DELETE CASCADE
                    );
                """)
            self.conn.commit()
            print("  \033[32m[+]\033[0m Tables created!")
        except psycopg2.errors.DuplicateTable as e:
            print("\033[31m[!]\033[0m", e)
            self.conn.rollback()

    def add_client(self, client_name, client_surname, client_email, clients_phone=None):
        """Adds a new client to the database. Returns client id.

        Keyword Arguments:
            - client_name -- name of the client
            - client_surname -- last name of the client
            - client_email -- email of the client
            - clients_phone -- phone nember of the client

        """

        print(f"[*] Client is added...")
        try:       
            self.cur.execute("""
                --begin-sql
                INSERT INTO Сlients(client_name, client_surname, client_email) 
                VALUES (%s, %s, %s)
                RETURNING client_id;
            """, (client_name, client_surname, client_email))
            client_id = self.cur.fetchone()
            print(f"  \033[32m[+]\033[0m Client {client_name} {client_surname} email:{client_email} added!")
            if clients_phone:
                self.add_client_phone(client_id=client_id, clients_phone=clients_phone)
            return(client_id[0])
        except psycopg2.errors.UniqueViolation as e:
            print("\033[31m[!]\033[0m", e)
            self.conn.rollback()              

    def add_client_phone(self, client_id, clients_phone):
        """Adds a clients's phone number to the database.

        Keyword Arguments:
            - client_id -- client id
            - clients_phone -- phone nember of the client

        """

        print(f"[*] Client's phone number is added...")
        try:
            self.cur.execute("""
                --begin-sql
                INSERT INTO Phones(clients_phone, client_id) 
                VALUES (%s, %s);
            """, (clients_phone, client_id))
            self.conn.commit()
            print(f"  \033[32m[+]\033[0m Client's phone number {clients_phone} added!")
        except psycopg2.errors.UniqueViolation as e:
            print("\033[31m[!]\033[0m", e)
            self.conn.rollback()
        except psycopg2.errors.ForeignKeyViolation as e:
            print("\033[31m[!]\033[0m", e)
            self.conn.rollback()        

    def change_client(self, client_id, client_name=None, client_surname=None, client_email=None, clients_phone=None):
        """Updates client data.

        Keyword Arguments:
            - client_id -- client id        
            - client_name -- name of the client
            - client_surname -- last name of the client
            - client_email -- email of the client
            - clients_phone -- phone nember of the client

        """

        print(f"[*] Client id={client_id} update...")
        if client_name:
            self.cur.execute("""
                --begin-sql
                UPDATE Сlients 
                SET client_name=%(client_name)s
                WHERE client_id=%(client_id)s;
            """, {"client_id": client_id, "client_name": client_name})
            self.conn.commit()
            print(f"  \033[32m[+]\033[0m Client name update! New name: {client_name}")
        if client_surname:
            self.cur.execute("""
                --begin-sql
                UPDATE Сlients 
                SET client_surname=%(client_surname)s
                WHERE client_id=%(client_id)s;
            """, {"client_id": client_id, "client_surname": client_surname})
            self.conn.commit()
            print(f"  \033[32m[+]\033[0m Client surname update! New surname: {client_surname}")
        if client_email:
            self.cur.execute("""
                --begin-sql
                UPDATE Сlients 
                SET client_email=%(client_email)s
                WHERE client_id=%(client_id)s;
            """, {"client_id": client_id, "client_email": client_email})
            self.conn.commit()
            print(f"  \033[32m[+]\033[0m Client email update! New email: {client_email}")
        if clients_phone:
            self.cur.execute("""
                --begin-sql
                UPDATE Phones 
                SET clients_phone=%(clients_phone)s
                WHERE client_id=%(client_id)s;
            """, {"client_id": client_id, "clients_phone": clients_phone})
            self.conn.commit()
            print(f"  \033[32m[+]\033[0m Client phone update! New phone: {clients_phone}")
                             
    def del_client_phone(self, client_id, clients_phone):
        """Deletes the client's phone.

        Keyword Arguments:
            - client_id -- client id        
            - clients_phone -- phone nember of the client

        """

        print(f"[*] Client's phone number is deleted...")
    
        self.cur.execute("""
            --begin-sql
            DELETE FROM Phones
            WHERE client_id=%s
            AND clients_phone=%s;
        """, (client_id, clients_phone, ))
        self.conn.commit()
        print(f"  \033[32m[+]\033[0m Client's phone number {clients_phone} deleted!")
 
    def del_client(self, client_id):
        """Deletes the client.

        Keyword Arguments:
            - client_id -- client id

        """

        print(f"[*] Сlient is deleted...")
        self.cur.execute("""
            --begin-sql
            DELETE FROM Сlients
                WHERE client_id=%(client_id)s;
        """, {"client_id": client_id})
        self.conn.commit()
        print(f"  \033[32m[+]\033[0m Client id={client_id} deleted!")


    def find_client(self, client_name=None, client_surname=None, client_email=None, clients_phone=None):
        """Finds a client.

        Keyword Arguments:   
            - client_name -- name of the client
            - client_surname -- last name of the client
            - client_email -- email of the client
            - clients_phone -- phone nember of the client

        """

        print(f"[*] Client search...")
        self.cur.execute("""
            --begin-sql
            SELECT cl.client_id, client_name, client_surname, client_email, clients_phone
              FROM Сlients cl
              JOIN Phones ph ON cl.client_id = ph.client_id
             WHERE (client_name = %(client_name)s OR %(client_name)s IS NULL)
               AND (client_surname = %(client_surname)s OR %(client_surname)s IS NULL)
               AND (client_email = %(client_email)s OR %(client_email)s IS NULL)
               AND (clients_phone = %(clients_phone)s OR %(clients_phone)s IS NULL);
        """, {"client_name": client_name, "client_surname": client_surname, "client_email": client_email, "clients_phone": clients_phone})
        clients = self.cur.fetchall()
        if clients: 
            print('  \033[32m[+]\033[0m Сlient found!', *clients)
        else:
            print('  \033[31m[!]\033[0m Сlient not found!')      

    def __del__(self):
        self.cur.close()
        self.conn.close()