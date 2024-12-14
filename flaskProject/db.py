import decimal

import psycopg2
import csv
import json
import xml.etree.ElementTree as ET
import datetime
import os


class BankDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = psycopg2.connect(
            host="localhost",
            database="bank",
            user="postgres",
            password="root"
        )
        self.cursor = self.conn.cursor()

    def user_exists(self, email, password):
        """Проверка на существование юзера в БД"""
        query = "SELECT UserID FROM users WHERE email = %s and password = %s"
        values = (email, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return bool(result)

    def org_exists(self, email, password):
        """Проверка на существование юзера в БД"""
        query = "SELECT orgid FROM organization WHERE email = %s and password = %s"
        values = (email, password)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return bool(result)

    def get_organization_email(self, user_email):
        query = """SELECT org.email from organization as org
        inner join organization_users as ou on org.orgid=ou.orgid
        inner join users on ou.userid=users.userid
        where users.email=%s"""
        self.cursor.execute(query, (user_email,))
        result = self.cursor.fetchall()
        print(result)
        return result[0]

    def get_organizations(self):
        """Получение списка организаций из БД"""
        try:
            # Выполнение запроса
            query = "SELECT orgid, name FROM organization"
            self.cursor.execute(query)

            # Получение результатов
            results = self.cursor.fetchall()

            # Преобразование результатов в список организаций
            organizations = [{'id': row[0], 'name': row[1]} for row in results]

            return organizations
        except Exception as e:
            print(e)
            return []

    def add_user(self, email, password, org_name):
        """Добавление пользователя в БД и связывание его с организацией"""
        try:
            # Добавление пользователя
            query = "INSERT INTO users (email, password) VALUES (%s, %s)"
            values = (email, password)
            self.cursor.execute(query, values)

            # Получение ID только что созданного пользователя
            query = "SELECT userid FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            user_id = self.cursor.fetchone()

            query = "INSERT INTO organization_users (userid, orgid) VALUES (%s, %s)"
            values = (user_id, org_name)
            self.cursor.execute(query, values)
            ## Поиск организации
            # query = "SELECT orgid FROM organization WHERE name = %s"
            # self.cursor.execute(query, (org_name,))
            # result = self.cursor.fetchone()
            # print(result)

            # if result is not None:
            #   org_id = result[0]

            # Добавление связи между пользователем и организацией
            # query = "INSERT INTO organization_users (userid, orgid) VALUES (%s, %s)"
            # values = (user_id, org_id)
            # self.cursor.execute(query, values)
            # else:
            #
            #  return False

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def add_org(self, email, password, org_name, city, account_details):
        """Добавление пользователя в БД и связывание его с организацией"""
        try:
            # Добавление организации
            query = "INSERT INTO organization (name, email, password, adress) VALUES (%s, %s, %s, %s)"
            values = (org_name, email, password, city)
            self.cursor.execute(query, values)

            # Получение ID только что созданной организации
            query = "SELECT orgid FROM organization WHERE email = %s and name = %s"
            self.cursor.execute(query, (email, org_name))
            org_id = self.cursor.fetchone()

            # Добавление банковского счета организации
            query = "INSERT INTO bank_accounts (account_number, orgid) VALUES (%s, %s)"
            values = (account_details, org_id)
            self.cursor.execute(query, values)

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def get_transaction_info(self, org_email):
        query = ("""SELECT t.transactionid,t.date,t.sum,ba.account_number,t.typeid,tt.type,t.sum_remains FROM transactions as t
                    inner join transaction_type as tt on t.typeid=tt.typeid
                    inner join bank_accounts as ba on t.account_nubmber=ba.account_number
                    where ba.account_number=(select account_number from bank_accounts
                    inner join organization as org on bank_accounts.orgid=org.orgid
                    where email=%s)""")
        self.cursor.execute(query, (org_email,))
        data = self.cursor.fetchall()
        return data

    def update_transactions(self, data, org_mail, ):
        try:
            print(data)
            for row in data:

                query = "select orgid from organization where email=%s"
                self.cursor.execute(query, (org_mail,))
                org_id = self.cursor.fetchone()

                query = "UPDATE bank_accounts SET account_number = %s where orgid=%s"
                self.cursor.execute(query, (row[3], org_id,))

                query = "UPDATE transactions SET date=%s,sum=%s,typeid=%s where transactionid=%s"
                values = [row[1], row[2], row[4], row[0]]
                self.cursor.execute(query, values)

                self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def delete_transaction(self, data, org_mail):
        try:

            query = "DELETE FROM transactions WHERE transactionid=%s"
            self.cursor.execute(query, (data[0],))

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def add_transaction(self, data, email):
        try:
            query = """select account_number from bank_accounts as ba
                        inner join organization as org on ba.orgid=org.orgid 
                        where email=%s"""
            self.cursor.execute(query, (email,))
            acc_num = self.cursor.fetchone()
            print(acc_num)
            query = """select org.balance from organization as org where email=%s"""
            self.cursor.execute(query, (email,))
            balance = self.cursor.fetchone()
            print(balance)
            sum_remains = balance[0]
            if data[2] == '1':
                sum_remains += int(data[1])
            elif data[2] == '2':
                sum_remains -= int(data[1])
            print(sum_remains)
            query = "insert into transactions (account_nubmber,date,sum,typeid,sum_remains) values (%s,%s,%s,%s,%s)"
            self.cursor.execute(query, (acc_num + tuple(data)+(sum_remains, )))
            query = "update organization set balance = %s where email=%s"
            self.cursor.execute(query, (sum_remains, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def get_users_info(self, org_mail):
        query = """select users.userid,users.email,users.password from users 
                 inner join organization_users as ou on users.userid=ou.userid
                 inner join organization as org on ou.orgid=org.orgid
                 where org.email=%s"""
        self.cursor.execute(query, (org_mail,))
        user_data = self.cursor.fetchall()
        return user_data

    def update_users(self, data, org_mail):
        try:
            for row in data:
                print(row)
                # Получение id Организации
                query = "select orgid from organization where email=%s"
                self.cursor.execute(query, (org_mail,))
                org_id = self.cursor.fetchone()

                query = "UPDATE users SET email = %s,password = %s where userid = %s"

                self.cursor.execute(query, (row[1], row[2], row[0]))

                self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def delete_users(self, user_data, org_mail):

        try:

            query = "DELETE FROM users WHERE userid=%s"
            self.cursor.execute(query, (user_data[0],))

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def org_add_users(self, email, password, org_mail):
        """Добавление пользователя в БД и связывание его с организацией"""
        try:
            # Добавление пользователя
            query = "INSERT INTO users (email, password) VALUES (%s, %s)"
            values = (email, password)
            self.cursor.execute(query, values)

            # Получение ID только что созданного пользователя
            query = "SELECT userid FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            user_id = self.cursor.fetchone()

            # Поиск организации
            query = "SELECT orgid FROM organization WHERE email = %s"
            self.cursor.execute(query, (org_mail,))
            result = self.cursor.fetchone()
            print(result)

            if result is not None:
                org_id = result[0]

                # Добавление связи между пользователем и организацией
                query = "INSERT INTO organization_users (userid, orgid) VALUES (%s, %s)"
                values = (user_id, org_id)
                self.cursor.execute(query, values)
            else:

                return False

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def export_db_to_files(self, save_directory):
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [table[0] for table in self.cursor.fetchall()]
        # Create the specified directory for the exported files
        os.makedirs(save_directory, exist_ok=True)

        # Initialize empty lists for each file type
        all_data_json = []
        all_data_csv = []
        all_data_xml = ET.Element("root")

        for table in tables:
            self.cursor.execute("SELECT * FROM {}".format(table))
            data = self.cursor.fetchall()

            # Convert Decimal objects to strings
            data = [[str(item) if isinstance(item, decimal.Decimal) else item for item in row] for row in data]

            # JSON
            all_data_json.append({table: data})

            # CSV
            all_data_csv.append([table] + data)

            # XML
            for row in data:
                item = ET.SubElement(all_data_xml, table)
                for cell in row:
                    ET.SubElement(item, "field").text = str(cell)

        # Write all data to files in the specified directory
        json_file_path = os.path.join(save_directory, 'all_data.json')
        with open(json_file_path, 'w') as f:
            json.dump(all_data_json, f, default=str)

        csv_file_path = os.path.join(save_directory, 'all_data.csv')
        with open(csv_file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(all_data_csv)

        xml_file_path = os.path.join(save_directory, 'all_data.xml')
        tree = ET.ElementTree(all_data_xml)
        tree.write(xml_file_path)

    def import_data(self, file, email):
        if file:
            filename = file.filename
            if filename.endswith('.json'):
                data = json.load(file)
                print(data)
                transactions = data[-1]['transactions']
                print(transactions)

                # Для каждой транзакции вызовите функцию add_transaction
                for transaction in transactions:
                    array = [str(transaction[2]), str(transaction[3]), str(transaction[4])]
                    print(array)
                    result = BankDB.add_transaction(self, array, email)
                    if result:
                        print("Транзакция успешно добавлена")
                    else:
                        print("Ошибка при добавлении транзакции")
                # Здесь ваш код для импорта данных из JSON в базу данныхx
            else:
                return "Неподдерживаемый тип файла"
            return "Данные успешно импортированы"
        else:
            return "Файл не найден"
