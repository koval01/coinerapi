import logging

import psycopg2
import psycopg2.extras

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER


class PostSQL:
    def __init__(self, user=None) -> None:
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASS, host=DB_HOST
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.user_id = user

    def finish(self) -> None:
        self.cursor.close()
        self.conn.close()

    def check_user(self) -> list:
        try:
            self.cursor.execute(
                'select * from wallet where user_id = %(user_id)s',
                {'user_id': self.user_id},
            )
            result = self.cursor.fetchall()
            self.finish()
            return result[0]
        except Exception as e:
            logging.debug(e)

    def get_balance(self) -> int:
        self.cursor.execute(
            'select balance from wallet where user_id = %(user_id)s limit 1',
            {'user_id': self.user_id},
        )
        result = self.cursor.fetchall()
        self.finish()
        return result[0][0]

    def get_sum_balance(self) -> int:
        self.cursor.execute(
            'select sum(balance) from wallet limit 1',
        )
        result = self.cursor.fetchone()
        self.finish()
        return result

    def get_top_balance(self, limit=10) -> dict:
        self.cursor.execute(
            'select name, balance, user_id from wallet order by balance desc limit %(limit)s',
            {'limit': limit},
        )
        result = self.cursor.fetchall()
        self.finish()
        return result

    def get_slaves(self) -> int:
        self.cursor.execute(
            'select slaves from wallet where user_id = %(user_id)s limit 1',
            {'user_id': self.user_id},
        )
        result = self.cursor.fetchone()
        self.finish()
        return result

    def get_slave_owners(self) -> int:
        self.cursor.execute(
            'select user_id, slaves from wallet where slaves > 0',
        )
        result = self.cursor.fetchall()
        self.finish()
        return result


class PostSQL_Inventory:
    def __init__(self, user) -> None:
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER,
            password=DB_PASS, host=DB_HOST
        )
        self.cursor = self.conn.cursor()
        self.user_id = user

    def finish(self) -> None:
        self.cursor.close()
        self.conn.close()

    def get_inventory(self) -> list:
        self.cursor.execute(
            'select item_id, id from inventory where owner_id = %(user_id)s',
            {'user_id': self.user_id},
        )
        result = self.cursor.fetchall()
        self.finish()
        return result

    def get_item(self, item_id_row) -> dict:
        self.cursor.execute(
            'select item_id, id, owner_id from inventory where id = %(item_id)s',
            {'item_id': item_id_row},
        )
        result = self.cursor.fetchall()
        self.finish()
        return result[0]
