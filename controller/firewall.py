"""
Firewall SDN con OpenFlow

Implementación de firewall a nivel de capa 2/3 usando OpenFlow.
Carga reglas desde archivo JSON y las instala en los switches.

Basado en: Coursera - Software Defined Networking (SDN) course
           Programming Assignment: Layer-2 Firewall Application
           Professor: Nick Feamster, Teaching Assistant: Arpit Gupta
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import EventMixin
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr
from utils import load_firewall_rules

log = core.getLogger()


class Firewall(EventMixin):
    """
    Firewall SDN que instala reglas de bloqueo en switches OpenFlow.
    
    Las reglas se cargan desde firewall_rules.json y se instalan
    cuando cada switch se conecta al controlador.
    """
    
    def __init__(self):
        """Inicializa el firewall y carga las reglas desde JSON."""
        self.listenTo(core.openflow)
        self.rules = load_firewall_rules()
        log.info("=" * 70)
        log.info("Firewall SDN inicializado")
        log.info("Reglas cargadas: %d", len(self.rules))
        log.info("=" * 70)

    def _handle_ConnectionUp(self, event):
        """
        Maneja la conexión de un nuevo switch.
        
        Instala todas las reglas de firewall en el switch
        que acaba de conectarse al controlador.
        
        Args:
            event: Evento ConnectionUp con información del switch
        """
        dpid_str = dpidToStr(event.dpid)
        log.info("=" * 70)
        log.info("Switch %s conectado", dpid_str)
        log.info("-" * 70)

        rules_installed = 0
        
        for idx, rule in enumerate(self.rules, 1):
            # Creacion del header del paquete a bloquear (los campos no definidos se consideran comodines)
            packet_header_to_block = of.ofp_match()
            
            # Tipo de Ethernet (IPv4)
            if 'dl_type' in rule or any(k in rule for k in ['src_ip', 'dst_ip', 'protocol']):
                packet_header_to_block.dl_type = rule.get('dl_type', 0x0800)  # IPv4 por defecto
            
            # Dirección IP origen
            if 'src_ip' in rule:
                packet_header_to_block.nw_src = IPAddr(rule['src_ip'])
            
            # Dirección IP destino
            if 'dst_ip' in rule:
                packet_header_to_block.nw_dst = IPAddr(rule['dst_ip'])
            
            # Los protocolos aceptados por openflow son TCP=6, UDP=17, ICMP=1
            # Si no se especifica, queda como comodin (matchea todos)
            if 'protocol' in rule:
                protocol = rule['protocol'].upper()
                if protocol == 'TCP':
                    packet_header_to_block.nw_proto = 6
                elif protocol == 'UDP':
                    packet_header_to_block.nw_proto = 17
                elif protocol == 'ICMP':
                    packet_header_to_block.nw_proto = 1
            
            # Puerto origen
            if 'src_port' in rule:
                packet_header_to_block.tp_src = int(rule['src_port'])
            
            # Puerto destino
            if 'dst_port' in rule:
                packet_header_to_block.tp_dst = int(rule['dst_port'])

            # Creacion de flow mod (sin acciones = DROP)
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = packet_header_to_block

            # revisar si son necesarias estas tres cosas:
            # flow_mod.priority = 100  # Alta prioridad (mayor que L2 learning)
            # flow_mod.idle_timeout = 0  # Nunca expira por inactividad
            # flow_mod.hard_timeout = 0  # Nunca expira por tiempo
            
            # Envio de regla al switch
            event.connection.send(flow_mod)
            rules_installed += 1
            
            rule_desc = rule.get('description', 'Sin descripción')
            log.info("  [%d/%d] %s", idx, len(self.rules), rule_desc)

        log.info("-" * 70)
        log.info("Firewall configurado en %s: %d reglas instaladas", 
                 dpid_str, rules_installed)
        log.info("=" * 70)


def launch():
    """
    Función de inicio del módulo POX.
    
    Registra el firewall en el core de POX.
    """
    core.registerNew(Firewall)
    