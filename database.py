import sqlite3;

class Database:
    def __init__ (self, chat_id: int) -> None:
        self.__chat_id: int = chat_id;
        self.__connection = sqlite3.Connection("threads_statuses.db");
        self.__cursor = self.__connection.cursor();


    def __del__ (self) -> None:
        self.__connection.close();

    def add_user (self) -> None:
        self.__cursor.execute(
            """
            INSERT OR IGNORE INTO threadstatuses (chat_id, threadstatus) 
            VALUES (?, ?)
            """,
            (self.__chat_id, 1));
        self.__connection.commit();

    def set_threadstatus (self, threadstatus: int) -> None:
        self.__cursor.execute(
            """
            UPDATE threadstatuses
            SET threadstatus = ?
            WHERE chat_id = ?
            """, (threadstatus, self.__chat_id));
        self.__connection.commit();

    def get_threadstatus (self) -> bool:
        self.__cursor.execute(
            """
            SELECT threadstatus
            FROM threadstatuses
            WHERE chat_id = ?
            """, (self.__chat_id,));
        threadstatus = self.__cursor.fetchall();
        return threadstatus[0][0];

if (__name__ == "__main__"):
    con = sqlite3.Connection("threads_statuses.db");
    cur = con.cursor();
    cur.execute(""" SELECT * FROM threadstatuses """);
    print(cur.fetchall());

