import sqlite3
from sqlite3 import Error, OperationalError


class DataBaseSqlite:
    create_table_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        gender TEXT
        );
    """

    create_table_messages = """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """

    update_message = """
    UPDATE
        messages
    SET
        text = "{text}"
    WHERE
        user_id = "{user_id}" and id = "{message_id}"
    """

    delete_message = """
    DELETE FROM
    messages
    WHERE
    user_id = "{user_id}" and id = "{message_id}"
    """

    user_exist = 'SELECT * FROM users where first_name = "{first_name}" and last_name = "{last_name}"'
    create_insert_user = """
        INSERT INTO
            users (first_name, last_name, age, gender)
        VALUES 
            ("{fname}", "{lname}", 0, '')
    ;"""

    create_insert_message = """
        INSERT INTO
            messages (text, user_id)
        VALUES 
            ("{text}", "{user_id}")
    ;"""

    fetchall_messages = 'SELECT * FROM messages where user_id = "{user_id}"'

    fetch_user = 'SELECT * FROM users where id = "{user_id}"'

    def __init__(self):
        self.connection = sqlite3.connect("guest_book.db")

    def run_insert_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except OperationalError as e:
            print(f'error is {e}')
        except Error as err:
            print(f'error is {err}')

    def select_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f'error is {e}')
        except Error as err:
            print(f'error is {err}')

    def select_one_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except OperationalError as e:
            print(f'error is {e}')
        except Error as err:
            print(f'error is {err}')

    def update_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except OperationalError as e:
            print(e)
        except Error as err:
            print(f'error is {err}')


class GuestBook:

    def __init__(self, guest_first_name, guest_last_name):
        self.guest_first_name = guest_first_name
        self.guest_last_name = guest_last_name

    @staticmethod
    def new_message(guest_message):
        return input(guest_message)

    @staticmethod
    def getting_user_name(message):
        try:
            first_name, last_name = input(message).split()
            print(" ")
            if len(first_name) <= 1 or len(last_name) <= 1:
                return 0, 0, False
            else:
                return first_name, last_name, True
        except Exception as ex:
            return 0, 0, False

    @staticmethod
    def show_messages(messages):
        menu = ""
        print('PLEASE SELECT MESSAGE YOU WANT: ')
        for index, item in enumerate(messages, start=1):
            menu += f'{index}- {item[1]} \n'
        print(menu)

    @staticmethod
    def show_all_messages(messages):
        result = "ALL ENTRIES: \n"
        for index, item in enumerate(messages, start=1):
            user_texted = database_object.select_one_query(database_object.fetch_user.format(user_id=item[2]))
            result += f'{index}- "{user_texted[1]} {user_texted[2]}" SAYS: {item[1]}\n'
        print(result)


if __name__ == "__main__":
    # make database connection and object
    database_object = DataBaseSqlite()
    database_object.run_insert_query(database_object.create_table_users)
    database_object.run_insert_query(database_object.create_table_messages)

    print(80 * "*")
    welcome_message = """\nkhosh amadid be mehmanie ma, lotfan baraye sabt ya virayeshe payame khod lotfan esmo famil khodra kamel vared konid (nemoone: hooman javan): """
    input_first_name, input_last_name, loop_breaker = GuestBook.getting_user_name(welcome_message)
    while not loop_breaker:
        if not loop_breaker:
            welcome_message_wrong_input = """\nlotfan dar vared kardane vorodi deghat konid esme shoma bayad bishtar az 1 harf bashad, lotfan baraye sabt ya virayeshe payame khod lotfan esmo famil khodra kamel vared konid (nemoone: hooman javan): """
            input_first_name, input_last_name, loop_breaker = GuestBook.getting_user_name(welcome_message_wrong_input)
    else:
        guest_book = GuestBook(guest_first_name=input_first_name, guest_last_name=input_last_name)
        loop_breaker = True
    print(80 * "*")

    user = database_object.select_one_query(
        database_object.user_exist.format(
            first_name=guest_book.guest_first_name, last_name=guest_book.guest_last_name))
    if not user:
        database_object.run_insert_query(
            database_object.create_insert_user.format(
                fname=guest_book.guest_first_name, lname=guest_book.guest_last_name))

    exit_flag = False
    print(35 * "*", "MAIN MENU", 35 * "*")
    while not exit_flag:
        print(35 * "*", "USER:", guest_book.guest_first_name, " ", guest_book.guest_last_name, 35 * "*")
        print("CHOOSE FROM MENU: ")
        print(" ")
        print("1- ADD NEW MESSAGE ")
        print("2- EDIT MY MESSAGES ")
        print("3- DELETE MY MESSAGE ")
        print("4- SHOW ALL ENTRIES")
        print("5- EXIT")
        selected_menu = input(":")
        user = database_object.select_one_query(
            database_object.user_exist.format(
                first_name=guest_book.guest_first_name, last_name=guest_book.guest_last_name))
        user_id = user[0]
        if selected_menu not in ["1", "2", "3", "4", "5"]:
            print("PLEASE SELECT FROM MENU 1, 2, 3, 4 OR 5!")
            continue
        elif selected_menu == "1":
            message = guest_book.new_message("PLEASE SEND YOUR MESSAGE: ")
            try:
                database_object.run_insert_query(
                    database_object.create_insert_message.format(text=message, user_id=user_id))
                print("YOUR MESSAGE WAS ADDED...")
            except Exception as e:
                print("SOMETHING IS WRONG!")
            finally:
                continue
        elif selected_menu == "2":
            messages = database_object.select_query(database_object.fetchall_messages.format(user_id=user_id))
            if not messages:
                print('YOU DONT HAVE ANY MESSAGE FOR EDIT...!')
                continue
            guest_book.show_messages(messages)
            while True:
                selected_message = input()
                try:
                    if int(selected_message) in range(1, len(messages) + 1):
                        break
                    else:
                        print("WRONG INPUT SELECT AGAIN...")
                except Exception as e:
                    print("WRONG INPUT SELECT AGAIN...")
                    continue
            new_message = input('PLEAS ADD NEW MESSAGE FOR EDIT PREVIEWS MESSAGE: ')
            try:
                message_id = messages[int(selected_message) - 1][0]
                database_object.update_query(
                    database_object.update_message.format(
                        text=new_message, user_id=user_id, message_id=message_id))
                print("YOUR MESSAGE WAS UPDATED...")
            except Exception as e:
                print("SOMETHING IS WRONG!")
            finally:
                continue
        elif selected_menu == "3":
            messages = database_object.select_query(database_object.fetchall_messages.format(user_id=user_id))
            if not messages:
                print('YOU DONT HAVE ANY MESSAGE FOR EDIT...!')
                continue
            guest_book.show_messages(messages)
            while True:
                selected_message = input()
                try:
                    if int(selected_message) in range(1, len(messages) + 1):
                        break
                except Exception as e:
                    print("WRONG INPUT SELECT AGAIN...")
                    continue
            try:
                message_id = messages[int(selected_message) - 1][0]
                database_object.update_query(
                    database_object.delete_message.format(message_id=message_id, user_id=user_id))
                print("YOUR MESSAGE WAS DELETED...")
            except Exception as e:
                print("SOMETHING IS WRONG!")

        elif selected_menu == "4":
            messages = database_object.select_query(database_object.fetchall_messages.format(user_id=user_id))
            if not messages:
                print('THERE IS NO ENTRIES ...!')
                continue
            guest_book.show_all_messages(messages)
            continue

        elif selected_menu == "5":
            print("BY BY")
            break
