
if __name__ == '__main__':
    import sqlite3
    connection = sqlite3.connect(':memory:')
    cur = connection.cursor()
    cur.execute("CREATE TABLE sales (id INT PRIMARY KEY, "
                "date DATETIME, sales INT);")
    cur.execute("INSERT INTO sales (id, date, sales) VALUES (1, '2016-09-13', 52)")

    cursor = VCRDB('sample2.yaml', connection).cursor()
    # cursor.execute("SELECT * FROM sales WHERE date = ?", ["2016-09-12"])
    # print(cursor.fetchall())

    cursor.execute("SELECT * FROM sales WHERE date = ?", ["2016-09-13"])
    print(cursor.fetchall())
