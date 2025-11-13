# Plan: Implementación SDN con Firewall en Mininet + POX

## 1. Estructura del Proyecto

Crear la estructura de archivos y directorios:

- [`topology.py`](topology.py) - Topología parametrizable de Mininet
- [`controller.py`](controller.py) - Controlador POX con L2 learning y firewall
- [`firewall_rules.json`](firewall_rules.json) - Reglas del firewall
- [`run_topology.sh`](run_topology.sh) - Script para iniciar la topología
- [`run_controller.sh`](run_controller.sh) - Script para iniciar el controlador
- [`test_firewall.sh`](test_firewall.sh) - Script para probar las reglas del firewall
- [`README.md`](README.md) - Instrucciones de uso

## 2. Topología Parametrizable (topology.py)

Implementar una clase `ChainTopology` que:

- Reciba parámetro `N` (número de switches)
- Cree cadena: S1 -- S2 -- ... -- SN
- Conecte 2 hosts a S1 (h1, h2)
- Conecte 2 hosts a SN (h3, h4)
- Caso especial N=1: todos los hosts conectados al mismo switch

**Ejemplo de uso:**

```bash
sudo mn --custom topology.py --topo chain,N=2 --mac --arp --switch ovsk --controller remote
```

## 3. Controlador POX Base (L2 Learning)

Implementar controlador con:

- **L2 Learning Switch**: Aprendizaje automático de la topología
- **Manejo de eventos**: `ConnectionUp` y `PacketIn`
- **Logging detallado**: Para verificar con Wireshark
- **Tabla MAC**: Diccionario para almacenar puerto por MAC address por switch

## 4. Firewall con Reglas JSON

Extender el controlador para:

- Cargar reglas desde [`firewall_rules.json`](firewall_rules.json)
- Implementar las 3 reglas requeridas:

  1. Bloquear puerto destino 80 (HTTP)
  2. Bloquear host 1 → puerto 5001 UDP
  3. Bloquear comunicación entre 2 hosts específicos

- Instalar reglas proactivas en los switches al conectarse
- Permitir agregar nuevas reglas en el JSON

**Estructura del JSON:**

```json
{
  "rules": [
    {
      "type": "block_port",
      "port": 80,
      "protocol": "tcp"
    },
    {
      "type": "block_host_port_protocol",
      "src_ip": "10.0.0.1",
      "dst_port": 5001,
      "protocol": "udp"
    },
    {
      "type": "block_communication",
      "host1_ip": "10.0.0.1",
      "host2_ip": "10.0.0.3"
    }
  ]
}
```

## 5. Verificación y Testing

### 5.1 Prueba básica con pingall

- Ejecutar `mininet> pingall`
- Verificar conectividad completa
- Capturar tráfico con Wireshark
- Revisar logs del controlador

### 5.2 Pruebas del Firewall con iperf

- **Regla 1 (puerto 80)**: 
  - Servidor: `iperf -s -p 80`
  - Cliente: `iperf -c <server_ip> -p 80`
  - Resultado esperado: Bloqueado

- **Regla 2 (h1 → puerto 5001 UDP)**:
  - Servidor: `iperf -s -u -p 5001`
  - Cliente desde h1: `iperf -c <server_ip> -u -p 5001`
  - Resultado esperado: Bloqueado

- **Regla 3 (bloqueo total entre hosts)**:
  - `h1 ping h3` (o los hosts elegidos)
  - Resultado esperado: 100% packet loss

## 6. Scripts de Automatización

- `run_topology.sh`: Iniciar Mininet con la topología
- `run_controller.sh`: Iniciar POX con el controlador
- `test_firewall.sh`: Ejecutar todas las pruebas de firewall automáticamente

## 7. Documentación

Crear [`README.md`](README.md) con:

- Requisitos previos (instalación de Mininet, POX, etc.)
- Orden de ejecución de comandos
- Explicación de cada prueba
- Resultados esperados
- Troubleshooting común