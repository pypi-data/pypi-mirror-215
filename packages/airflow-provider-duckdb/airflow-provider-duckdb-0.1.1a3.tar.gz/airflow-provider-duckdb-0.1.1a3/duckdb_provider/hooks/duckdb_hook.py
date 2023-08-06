from __future__ import annotations
from typing import Dict

import duckdb

from airflow.exceptions import AirflowException
from airflow.providers.common.sql.hooks.sql import DbApiHook


class DuckDBHook(DbApiHook):
    """Interact with DuckDB."""

    conn_name_attr = "duckdb_conn_id"
    default_conn_name = "duckdb_default"
    conn_type = "duckdb"
    hook_name = "DuckDB"
    placeholder = "?"

    def get_conn(self) -> duckdb.DuckDBPyConnection:
        """Returns a duckdb connection object"""
        uri = self.get_uri()
        return duckdb.connect(uri)

    def get_uri(self) -> str:
        """Override DbApiHook get_uri method for get_sqlalchemy_engine()"""
        # get the conn_id from the hook
        conn_id = getattr(self, self.conn_name_attr)

        # get the airflow connection object with config
        airflow_conn = self.get_connection(conn_id)

        # if a user gave both the host and schema, raise an error
        if airflow_conn.host and airflow_conn.schema:
            raise AirflowException(
                "You cannot set both host and schema! If you're connecting to a local file, set host to the path to the file. If you're connecting to a MotherDuck instance, set schema to the database name."
            )

        # if a user gave a host, use a connection to a local file
        if airflow_conn.host:
            return f"duckdb:///{airflow_conn.host}"

        # if a user gave a password, use a connection to a MotherDuck instance
        if airflow_conn.password:
            db_name = airflow_conn.schema or ""
            return f"duckdb:///md:{db_name}?motherduck_token{airflow_conn.password}&token={airflow_conn.password}"

        # otherwise use an in-memory connection
        return f"duckdb:///:memory:"

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["login", "port", "extra"],
            "relabeling": {
                "host": "Path to local database file",
                "schema": "MotherDuck database name",
                "password": "MotherDuck Service token",
            },
        }
