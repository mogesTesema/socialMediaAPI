import sqlite3


class DatabaseConnection:
    def __init__(self, host_storage):
        self.connection = None
        self.host_storage = host_storage

    def __enter__(self):
        self.connection = sqlite3.connect(self.host_storage)
        self.connection.execute("PRAGMA foreign_keys=ON;")
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type or exc_value or exc_tb:
            self.connection.rollback()
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()