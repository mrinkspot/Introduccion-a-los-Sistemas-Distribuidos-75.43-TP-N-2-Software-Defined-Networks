"""
Utilidades para el firewall SDN

Módulo para cargar y parsear reglas de firewall desde archivo JSON.
"""

import os
import json
from pox.core import core

from pox.lib.addresses import IPAddr

log = core.getLogger()

firewall_rules_json = "firewall_rules.json"

MIN_PORT = 1
MAX_PORT = 65535


def validate_rule(rule, rule_idx):
    """
    Valida que una regla de firewall tenga un formato válido.
    
    Args:
        rule (dict): Regla a validar
        rule_idx (int): Índice de la regla (para logging)
    
    Returns:
        bool: True si la regla es válida, False en caso contrario
    """
    if not isinstance(rule, dict):
        log.warning("Regla %d: No es un diccionario válido", rule_idx)
        return False
    
    # Al menos un campo de matching
    valid_fields = ['src_ip', 'dst_ip', 'protocol', 'src_port', 'dst_port', 'dl_type']
    if not any(field in rule for field in valid_fields):
        log.warning("Regla %d: No tiene campos de matching válidos", rule_idx)
        return False
    
    # Protocolo existe
    if 'protocol' in rule:
        protocol = rule['protocol'].upper()
        if protocol not in ['TCP', 'UDP', 'ICMP']:
            log.warning("Regla %d: Protocolo '%s' inválido (debe ser TCP, UDP o ICMP)", 
                       rule_idx, rule['protocol'])
            return False
        
        # ICMP no tiene puertos
        if protocol == 'ICMP' and ('src_port' in rule or 'dst_port' in rule):
            log.warning("Regla %d: ICMP no puede tener puertos TCP/UDP", rule_idx)
            return False
    
    # Si hay puertos, hay protocolo
    if ('src_port' in rule or 'dst_port' in rule) and 'protocol' not in rule:
        log.warning("Regla %d: Puertos requieren especificar 'protocol' (TCP o UDP)", rule_idx)
        return False
    
    # Formato de IPs
    for ip_field in ['src_ip', 'dst_ip']:
        if ip_field in rule:
            ip = rule[ip_field]
            if not isinstance(ip, str) or not is_valid_ip(ip):
                log.warning("Regla %d: IP inválida en '%s': %s", rule_idx, ip_field, ip)
                return False
    
    # Puertos (rango 1-65535)
    for port_field in ['src_port', 'dst_port']:
        if port_field in rule:
            try:
                port = int(rule[port_field])
                if port < MIN_PORT or port > MAX_PORT:
                    log.warning("Regla %d: Puerto fuera de rango en '%s': %d", 
                               rule_idx, port_field, port)
                    return False
            except (ValueError, TypeError):
                log.warning("Regla %d: Puerto inválido en '%s': %s", 
                           rule_idx, port_field, rule[port_field])
                return False
    
    return True


def is_valid_ip(ip_str):
    """
    Valida formato de dirección IPv4.
    
    Args:
        ip_str (str): String con dirección IP
    
    Returns:
        bool: True si es una IP válida, False en caso contrario
    """

    if not isinstance(ip_str, str):
        return False

    try:
        IPAddr(ip_str)  # acepta solo IPv4
        return True
    except:
        return False



def load_firewall_rules():
    """
    Carga y valida las reglas de firewall desde el archivo JSON.
    
    Returns:
        list: Lista de reglas válidas (diccionarios) o lista vacía si hay error
    """
    try:
        # Buscamos el archivo en el directorio actual 
        path = os.path.join(os.path.dirname(__file__), firewall_rules_json)
        
        with open(path, 'r') as rules:
            data = json.load(rules)
            rules_list = data.get('rules', [])
            
            if not rules_list:
                log.warning("El archivo JSON no contiene reglas")
                return []
            
            # Validación de cada regla
            valid_rules = []
            for idx, rule in enumerate(rules_list, 1):
                if validate_rule(rule, idx):
                    valid_rules.append(rule)
                else:
                    log.error("Regla %d ignorada por errores de validación", idx)
            
            log.info("Reglas cargadas desde %s: %d válidas de %d totales", 
                    path, len(valid_rules), len(rules_list))
            
            return valid_rules
            
    except FileNotFoundError:
        log.error("Archivo de configuración '%s' no encontrado en %s", 
                 firewall_rules_json, os.path.dirname(__file__))
        log.error("Asegurate de que el archivo exista en el directorio 'controller/'")
        return []
    except json.JSONDecodeError as e:
        log.error("Error al parsear JSON: %s", e)
        log.error("Verificá que el archivo JSON tenga sintaxis válida")
        return []
    except Exception as e:
        log.error("Error inesperado al cargar reglas: %s", e)
        return []