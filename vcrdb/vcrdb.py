import os.path
import yaml


class VCRCursor(object):

    def __init__(self, cassette_filename, connection):
        self.cassette_filename = cassette_filename
        if os.path.exists(cassette_filename):
            with open(cassette_filename) as sample_file:
                cassette = yaml.load(sample_file.read())
            self.cassette = cassette
            self.connection = None
        else:
            self.cassette = None
            self.connection = connection

    def execute(self, statement, params=[]):
        if self.cassette is not None:
            for query in self.cassette['queries']:
                if query['statement'] == statement and query['params'] == params:
                    self.results = query['results']
                    break
            else:
                error_msg = ("Error, could not find cassette for "
                             "statement {} with params {}".format(statement, params))
                raise ValueError(error_msg)
        else:
            cursor = self.connection.cursor()
            cursor.execute(statement, params)
            data = cursor.fetchall()
            results = {
                "columns": map(lambda x: x[0], cursor.description),
                "data": data
            }
            query = {
                "statement": statement,
                "params": params,
                "results": results
            }
            self.results = results
            with open(self.cassette_filename, 'w') as cassette_file:
                cassette_file.write(yaml.dump({'queries': [query]}))
            cursor.close()

    def fetchall(self):
        return self.results['data']


class VCRDB(object):

    def __init__(self, cassette_filename, connection):
        self.cassette_filename = cassette_filename
        self.connection = connection

    def cursor(self):
        return VCRCursor(self.cassette_filename, self.connection)


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
