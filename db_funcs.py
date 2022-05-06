import psycopg2
from psycopg2 import sql


def get_connection():
    connection = psycopg2.connect(dbname='secure_docs',
                                  user='postgres',
                                  password='1234',
                                  host='localhost')
    return connection


def close_connection(connection):
    if connection:
        connection.close()


def get_all_records(table_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM {table}"
        cursor.execute(
            sql.SQL(select_query).format(table=sql.Identifier(table_name)),
        )

        records = cursor.fetchall()

        cursor.close()
        close_connection(connection)

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)


def get_first_record(table_name):  # TMP!
    try:
        connection = get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM {table} LIMIT 1"
        cursor.execute(
            sql.SQL(select_query).format(table=sql.Identifier(table_name)),
        )

        record = cursor.fetchone()

        cursor.close()
        close_connection(connection)

        return record

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)


def get_records_by_value(table_name, column_name, value):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        table = sql.Identifier(table_name)
        column = sql.Identifier(column_name)
        value = sql.Literal(value)

        select_query = sql.SQL("SELECT * FROM {table} WHERE {column} = {value}").format(
            table=table,
            column=column,
            value=value
        )

        print(select_query.as_string(connection))  # dbg
        cursor.execute(select_query)

        records = cursor.fetchall()

        cursor.close()
        close_connection(connection)

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)


def get_column(table_name, field_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        table = sql.Identifier(table_name)
        field = sql.Identifier(field_name)

        select_query = sql.SQL("SELECT {field} FROM {table}").format(
            table=table,
            field=field,
        )

        print(select_query.as_string(connection))  # dbg
        cursor.execute(select_query)

        records = cursor.fetchall()

        cursor.close()
        close_connection(connection)

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)


def insert_record(table_name, column_names, record_to_insert):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        table = sql.Identifier(table_name)
        columns = sql.SQL(', ').join(sql.Identifier(n) for n in column_names)
        record_tokens = sql.SQL(', ').join(sql.Literal(n) for n in record_to_insert)

        insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=table,
            columns=columns,
            values=record_tokens
        )

        print(insert_query.as_string(connection))  # dbg
        cursor.execute(insert_query)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into '" + table_name + "' table")

        cursor.close()
        close_connection(connection)

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)


def delete_all_records(table_name):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM {table}"
        cursor.execute(
            sql.SQL(delete_query).format(table=sql.Identifier(table_name)),
        )

        connection.commit()

        cursor.close()
        close_connection(connection)

    except (Exception, psycopg2.Error) as error:
        print("Error while getting data", error)
