import simplejson
FUNCTION_STRUCTURE = {"prueba": {}, }

def oculta(req):
    """{"prueba": {}}"""
    return simplejson.dumps("Funciona", encoding='utf-8')

def oculta2(req):
    """{"prueba2": {"name": "String value"}}"""
    return simplejson.dumps({"hola": "Funciona 2"}, encoding='utf-8')