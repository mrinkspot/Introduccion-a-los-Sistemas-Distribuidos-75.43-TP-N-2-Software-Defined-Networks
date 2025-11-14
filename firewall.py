# Coursera :
# - Software Defined Networking ( SDN ) course
# -- Programming Assignment : Layer -2 Firewall Application Professor : Nick Feamster
# Teaching Assistant : Arpit Gupta
from pox . core import core
import pox . openflow . libopenflow_01 as of
from pox . lib . revent import *
from pox . lib . util import dpidToStr
from pox . lib . addresses import EthAddr, IPAddr
from collections import namedtuple
import os
# Add your imports here ...
from utils import load_firewall_rules

log = core . getLogger ()
# Add your global variables here ...


class Firewall ( EventMixin ) :
    def __init__ ( self ) :
        self . listenTo ( core . openflow )
        log . debug ( " Enabling ␣ Firewall ␣ Module " )
        self.rules = load_firewall_rules()

    
    def _handle_ConnectionUp ( self , event ) :
        # Add your logic here ...

        log.debug("Switch %s conectado", dpidToStr(event.dpid))

        for rule in self.rules:
            
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

            # de la docu de openflow, si no se especifican acciones se dropea el paquete
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = packet_header_to_block
            event.connection.send(flow_mod)
            ##
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
    



def launch () :
    # Starting the Firewall module
    core . registerNew ( Firewall )