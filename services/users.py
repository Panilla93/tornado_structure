import simplejson
FUNCTION_STRUCTURE = {"prueba": {}, }

def login(req):
    """{
    "input": {
        "username": "User email",
        "password": "Alphanumeric with eight caracter"
        },
    "output": {
        "id_user": "User identificator",
        "id_session": 200
        }
    }"""
    return simplejson.dumps("Funciona", encoding='utf-8')

def ppppppppppppppppppppp(req):
    """{"prueba2": {"name": "String value"}}"""
    return simplejson.dumps({"hola": "Funciona 2"}, encoding='utf-8')