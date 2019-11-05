from google.cloud import bigquery


class BigQueryBackend:
    def __init__(self, dataset, table, table_columns):
        self.big_query = bigquery.Client()
        table_ref = self.big_query.dataset(dataset).table(table)
        self.table = self.big_query.get_table(table_ref)
        self.columns = table_columns


    def consume(self, messages):
        data = [[msg.get(k, "") for k in self.columns] for msg in messages]
        self.copy(data)

    def copy(self, rows):
        raise Exception('Method not implemented')
