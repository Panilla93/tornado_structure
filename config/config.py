# -*- coding: utf-8 -*-
import os

DATABASE = os.getenv("play_db", "bd_to_play")
PORT = os.getenv("play_port", "8888")