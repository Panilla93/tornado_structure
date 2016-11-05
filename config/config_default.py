# -*- coding: utf-8 -*-
import os

DB_HOST = os.getenv("play_db_host", "localhost")
DB_PORT = os.getenv("play_db_port", "5432")
DB_NAME = os.getenv("play_db_name", "bd_to_play")
DB_USER = os.getenv("play_db_user", "postgres")
DB_PASSWORD = os.getenv("play_db_password", "postgres")
PORT = os.getenv("play_port", "8888")