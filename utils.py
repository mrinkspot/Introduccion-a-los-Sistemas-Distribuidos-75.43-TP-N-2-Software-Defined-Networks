import os
import json
from pox . core import core

log = core . getLogger ()

firewall_rules_json = "firewall_rules.json"

def load_firewall_rules():
    try:
        # Buscamos el archivo en el directorio actual 
        path = os.path.join(os.path.dirname(__file__), firewall_rules_json)
        
        with open(path, 'r') as rules:
            data = json.load(rules)
            log.info("Reglas cargadas exitosamente desde %s", path)
            return data.get('rules', [])
    except FileNotFoundError:
        log.error("Archivo de configuración '%s' no encontrado", firewall_rules_json)
        return []
    except json.JSONDecodeError as e:
        log.error("Error al parsear JSON: %s", e)
        return []
    except Exception as e:
        log.error("Error inesperado al cargar reglas: %s", e)
        return []