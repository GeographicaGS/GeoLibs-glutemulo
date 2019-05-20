import operator
import time

from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient, CopySQLClient
from carto.exceptions import CartoException

from ..config import cfg
from ..logger import log


def _get_auth_client():
    log.info(f"Using {cfg.CARTO_ONPREMISES_URL}")
    auth_client = APIKeyAuthClient(
        api_key=cfg.CARTO_API_KEY, base_url=cfg.CARTO_ONPREMISES_URL
    )
    return auth_client


def query(sql_query, parse_json=True, do_post=True, format=None, retries=5):
    log.debug(f"Query: {sql_query}")
    sql = SQLClient(_get_auth_client(), api_version="v2")
    res = None

    for retry_number in range(retries):
        try:
            res = sql.send(sql_query, parse_json, do_post, format)

            if res:
                break

        except CartoException as carto_exception:
            if retry_number == retries - 1:
                raise carto_exception
            else:
                time.sleep(5)
                continue

    if format is None:
        return res["rows"]

    return res


def init(dataset):
    """Called on app start"""
    create_table_if_not_exists(dataset, OBSERVATIONS_TABLE)


def copy(tablename, rows, delimiter=",", quote='"'):
    copy_client = CopySQLClient(_get_auth_client())
    headers = delimiter.join(rows[0])
    from_query = f"""COPY {tablename} ({headers}) FROM stdin
        (FORMAT CSV, DELIMITER '{delimiter}', HEADER true)"""
    try:
        return copy_client.copyfrom(from_query, rows_generator(rows, delimiter, quote))
    except CartoException as e:
        log.error(f"Error importing \n\n {rows}")
        log.exception(e)


def rows_generator(rows, delimiter, quote):
    # note the \n to delimit rows
    for r in rows:
        yield bytearray(
            delimiter.join(
                [
                    "{}{}{}".format(
                        quote, str(e).replace(f"{quote}", f"{quote}{quote}"), quote
                    )
                    if e
                    else ""
                    for e in r
                ]
            )
            + "\n",
            "utf-8",
        )


def create_table_if_not_exists(tablename, table_definition, table_indexes, cartodbfy=True):
    tables = map(
        operator.itemgetter("cdb_usertables"), query("SELECT CDB_UserTables()")
    )
    if tablename in tables:
        return
    log.info(f'Creating not found table "{tablename}"')
    query(f"CREATE TABLE IF NOT EXISTS {tablename} ({table_definition})")
    log.debug("Adding indexes")
    for idx in table_indexes.splitlines():
        if not idx:
            continue
        log.debug(f"{idx}")
        query(idx)
    if cartodbfy:
        log.debug("Cartodbfing table")
        query(f"SELECT CDB_CartodbfyTable(current_schema, '{tablename}')")
