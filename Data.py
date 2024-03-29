import sqlite3


class Data:
    def __init__(self, db_path):
        self.__connection = sqlite3.connect(db_path, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS articles
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            chat_id INTEGER, 
                            text TEXT)
                        """)
        self.__connection.commit()

    def add(self, chat_id, string):
        query = self.__cursor.execute("SELECT id FROM articles WHERE chat_id=? AND text=?", (chat_id, string))
        if len(query.fetchall()) == 0:
            self.__cursor.execute("INSERT INTO articles (chat_id, text) VALUES (?, ?)", (chat_id, string))
            self.__connection.commit()
            return query.lastrowid
        else:
            return -1

    def list(self, chat_id):
        query = self.__cursor.execute("SELECT id, text FROM articles WHERE chat_id=? ORDER BY id DESC", (chat_id, ))
        return query.fetchall()


    def delete(self, chat_id, record_id):
        query = self.__cursor.execute("DELETE FROM articles WHERE chat_id=? AND id=?", (chat_id, record_id))
        self.__connection.commit()

        if query.rowcount == 0:
            return False

        return True

    def edit(self, chat_id, record_id, upd_data):
        self.__cursor.execute("UPDATE articles SET text=? "
                              "WHERE chat_id =? AND id =?", (upd_data, chat_id, record_id))
        self.__connection.commit()

        if self.__cursor.rowcount == 0:
            return False
        return True

    def __del__(self):
        # self.__cursor.close()
        self.__connection.close()
