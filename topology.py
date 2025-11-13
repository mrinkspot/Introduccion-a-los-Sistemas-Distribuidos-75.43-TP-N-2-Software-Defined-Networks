#!/usr/bin/env python3
"""
Topología SDN Parametrizable - Cadena de Switches

Este módulo implementa una topología de Mininet con N switches conectados en cadena,
donde los hosts se conectan únicamente a los switches de los extremos.

Topología:
    N >= 2: h1, h2 -- S1 -- S2 -- ... -- SN -- h3, h4
    N = 1:  h1, h2, h3, h4 -- S1
"""

from mininet.topo import Topo


class ChainTopology(Topo):
    """
    Topología de cadena parametrizable con N switches.
    
    Args:
        N (int): Número de switches en la cadena. Default: 2
    
    Atributos:
        num_switches: Cantidad de switches en la topología
        switch_list: Lista con los identificadores de los switches creados
        host_list: Lista con los identificadores de los hosts creados
    """
    
    def __init__(self, N=2, **opts):
        """
        Inicializa la topología con N switches en cadena.
        
        Args:
            N: Número de switches (mínimo 1)
        """
        if N < 1:
            raise ValueError("N debe ser al menos 1")
        
        self.num_switches = N
        self.switch_list = []  # Renombrado para evitar conflicto con Topo.switches()
        self.host_list = []    # Renombrado para evitar conflicto con Topo.hosts()
        
        Topo.__init__(self, **opts)
        
        self.build_topology()
    
    def build_topology(self):
        """Construye la topología de switches y hosts."""
        print(f"\n{'='*60}")
        print(f"Construyendo topología con {self.num_switches} switch(es)")
        print(f"{'='*60}\n")
        
        self.create_switches()
        
        self.connect_switches()
        
        self.create_and_connect_hosts()
        
        self.print_topology_summary()
    
    def create_switches(self):
        """Crea N switches."""
        for i in range(1, self.num_switches + 1):
            switch_name = f's{i}'
            self.addSwitch(switch_name)
            self.switch_list.append(switch_name)
            print(f"  Switch creado: {switch_name}")
    
    def connect_switches(self):
        """Conecta los switches en cadena: S1 -- S2 -- ... -- SN."""
        if self.num_switches < 2:
            print("  • Un solo switch, no hay enlaces entre switches")
            return
        
        print(f"\n  Conectando switches en cadena:")
        for i in range(len(self.switch_list) - 1):
            sw1 = self.switch_list[i]
            sw2 = self.switch_list[i + 1]
            self.addLink(sw1, sw2)
            print(f"    {sw1} <--> {sw2}")
    
    def create_and_connect_hosts(self):
        """
        Crea 4 hosts y los conecta a los switches de los extremos.
        
        Casos:
            - N >= 2: h1, h2 → S1  y  h3, h4 → SN
            - N = 1:  h1, h2, h3, h4 → S1
        """
        print(f"\n  Creando y conectando hosts:")
        
        # Switches de los extremos
        first_switch = self.switch_list[0]   # S1
        last_switch = self.switch_list[-1]   # SN (puede ser el mismo que S1 si N=1)
        
        # creacion de los 4 hosts
        for i in range(1, 5):
            host_name = f'h{i}'
            # asignacion de IP automatica: 10.0.0.1, 10.0.0.2, etc
            host_ip = f'10.0.0.{i}/24'
            self.addHost(host_name, ip=host_ip)
            self.host_list.append(host_name)
            print(f"    ✓ Host creado: {host_name} (IP: {host_ip})")
        
        print(f"\n  Conectando hosts a switches:")
        
        # h1 y h2 al primer switch (S1)
        self.addLink('h1', first_switch)
        print(f"    h1 <--> {first_switch}")
        
        self.addLink('h2', first_switch)
        print(f"    h2 <--> {first_switch}")
        
        # h3 y h4 al ultimo switch (SN)
        self.addLink('h3', last_switch)
        print(f"    h3 <--> {last_switch}")
        
        self.addLink('h4', last_switch)
        print(f"    h4 <--> {last_switch}")
        
        if self.num_switches == 1:
            print(f"\n  ⚠ Nota: Con N=1, todos los hosts están en el mismo switch")
    
    def print_topology_summary(self):
        """Imprime un resumen de la topología creada."""
        print(f"\n{'='*60}")
        print(f"RESUMEN DE LA TOPOLOGÍA")
        print(f"{'='*60}")
        print(f"  Switches: {len(self.switch_list)} → {', '.join(self.switch_list)}")
        print(f"  Hosts:    {len(self.host_list)} → {', '.join(self.host_list)}")
        print(f"  Enlaces:")
        
        if self.num_switches >= 2:
            print(f"    • Cadena de switches: {' -- '.join(self.switch_list)}")
        
        print(f"    • h1, h2 conectados a {self.switch_list[0]}")
        print(f"    • h3, h4 conectados a {self.switch_list[-1]}")
        print(f"{'='*60}\n")


topos = {
    'chain': ChainTopology
}


if __name__ == '__main__':
    """
    Permite probar la topología sin ejecutar Mininet.
    Uso: python3 topology.py
    """
    print("\n" + "="*60)
    print("PRUEBA DE TOPOLOGÍA")
    print("="*60)
    
    for n in [1, 2, 3, 5]:
        topo = ChainTopology(N=n)
        print("\n")

