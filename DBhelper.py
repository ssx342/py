# DBHelper.py

import pymysql


class DBHelper:

    def __init__(self, host, user, password, db):

        self.host = host

        self.user = user

        self.password = password

        self.db = db

        self.connection = None

        self.cursor = None

    def Commit(self):

            self.connection.commit()

    def insertWithoutCommit(self, query, params=()):

            try:

                self.execute_query(query, params)

            except Exception as e:

                self.connection.rollback()

    def connect(self):

        try:

            self.connection = pymysql.connect(

                host=self.host,

                user=self.user,

                password=self.password,

                db=self.db,

                charset='utf8',

                cursorclass=pymysql.cursors.DictCursor

            )

            self.cursor = self.connection.cursor()

        except pymysql.MySQLError as e:

            print(f"Error connecting to the database: {e}")

            raise

    def close(self):

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

        except pymysql.MySQLError as e:

            print(f"Error closing the database connection: {e}")

    def execute_query(self, query, params=()):

        try:

            self.cursor.execute(query, params)

            return self.cursor.fetchall()

        except pymysql.MySQLError as e:

            print(f"Error executing query: {e}")

            raise

    def fetch_all(self, query, params=()):

        self.connect()

        try:

            result = self.execute_query(query, params)

        finally:

            self.close()

        return result

    def insert(self, query, params=()):

        self.connect()

        try:

            self.execute_query(query, params)

            self.connection.commit()

        except Exception as e:

            self.connection.rollback()

            print(f"Error inserting data: {e}")

            raise

        finally:

            self.close()

    def update(self, query, params=()):

        self.connect()

        try:

            self.execute_query(query, params)

            self.connection.commit()

        except Exception as e:

            self.connection.rollback()

            print(f"Error updating data: {e}")

            raise

        finally:

            self.close()

    def delete(self, query, params=()):

        self.connect()

        try:

            self.execute_query(query, params)

            self.connection.commit()

        except Exception as e:

            self.connection.rollback()

            print(f"Error deleting data: {e}")

            raise

        finally:

            self.close()