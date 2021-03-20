'''this is place for all handling database,
    from connect, get, update, insert, ...'''
import sqlite3
import traceback
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASEDIR, './products.db')
SCHEMA_FILE = os.path.join(BASEDIR, './schema.sql')


def get_conn():
    '''get connect to sqlite database'''
    conn = sqlite3.connect(DATABASE)
    return conn


def init_db():
    ''' init database from schema file
        include: create table command and trigger
        please check file schema.sql at the root of the project for more detailed information

        Returns:
            bool: True for success, False otherwise'''
    init = True
    try:
        conn = get_conn()
        f_read = open(SCHEMA_FILE, 'r')
        queries = f_read.read()
        conn.cursor().executescript(queries)
    except sqlite3.Error:
        traceback.print_exc()
        init = False
    finally:
        conn.close()
        f_read.close()
    return init


def update_and_get_stat(product_id, score):
    ''' The function gets total count and total score of the product
        if product did not exist in database insert it
        otherwise update new count and total score of that product
        calculate mean from new count and total, then return the result

        Args:
            product_id (str): product_id of product.
            score (int): score of product.

        Returns:
            tuple(product_id, mean_value): The return value. stat of product, None if error occurred
        '''
    try:
        conn = get_conn()
        cur = conn.cursor()
        total_score = score
        count = 1
        product_stat = cur.execute("SELECT product_id, sum(count), sum(total_score)"
                                   " from product_stat where product_id = ?",
                                   [product_id]).fetchone()
        if not all(product_stat):
            cur.execute('insert into product_stat(product_id, count, total_score) values (?, 1, ?)'
                        , [product_id, score])
        else:
            cur.execute('update product_stat '
                        'set count = count + 1, total_score = total_score + ?'
                        ' where product_id = ?', [score, product_id])
            count += int(product_stat[1])
            total_score += float(product_stat[2])

        conn.commit()
        res = (product_id, total_score/count)
    except sqlite3.Error:
        conn.rollback()
        traceback.print_exc()
        res = None
    finally:
        conn.close()
    return res

def validate(product_id, score):
    '''Validate input data before push to database
        + product_id must not be empty
        + score must be integer and value from 0 to 5

        Returns:
            bool: True for success, False otherwise
    '''
    if (product_id.strip()) and isinstance(score, int) and 0 <= score <= 5:
        return True

    return False
