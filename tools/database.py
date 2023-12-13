import sqlite3 as sl
from sqlite3 import Error

default_database_addrs = "./results/benchmarks.db"


def display_table(conn):
    try:
        c = conn.cursor()

        # Execute a SELECT query to retrieve all rows from the 'benchmarks' table
        c.execute("SELECT * FROM benchmarks")

        # Fetch all rows from the executed query
        rows = c.fetchall()

        # Print column headers
        header = [description[0] for description in c.description]
        print("|".join(header))

        # Print each row in the table
        for row in rows:
            print("|".join(str(col) for col in row))

    except Error as e:
        print(e)


def create_connection(db_file=default_database_addrs):
    conn = None
    try:
        conn = sl.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def initialization(conn):
    sql_create_benchmarks_table = """
    CREATE TABLE IF NOT EXISTS benchmarks (
                                        id integer PRIMARY KEY,
                                        platform text NOT NULL,
                                        provider text NOT NULL,
                                        backend text NOT NULL,
                                        algorithm text NOT NULL,
                                        num_qubit integer NOT NULL,
                                        num_shot integer NOT NULL,
                                        type text NOT NULL,
                                        value real NOT NULL,
                                        date text NOT NULL
                                    );
    """
    try:
        create_table(conn, sql_create_benchmarks_table)
    except Error as e:
        print(e)


def create_benchmark(conn, benchmark):
    sql = """
    INSERT INTO benchmarks(
        platform,
        provider,
        backend,
        algorithm,
        num_qubit,
        num_shot,
        type,
        value,
        date
    ) VALUES(?,?,?,?,?,?,?,?,?)
    """
    cur = conn.cursor()
    cur.execute(sql, benchmark)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
    conn = create_connection()
    
    with conn:
        display_table(conn)
