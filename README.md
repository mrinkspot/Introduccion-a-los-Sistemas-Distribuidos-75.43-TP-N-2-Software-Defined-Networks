# TP N° 2: Software-Defined Networks (SDN)

**Introducción a los Sistemas Distribuidos (75.43) - FIUBA**

Implementación de una topología SDN parametrizable con Mininet y controlador POX con funcionalidad de firewall.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Topología](#topología)
- [Uso Básico](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)

---

## Descripción

Este proyecto implementa:

1. **Topología Parametrizable**: Una cadena de N switches con hosts en los extremos
2. **Controlador POX**: Con L2 learning y funcionalidad de firewall
3. **Reglas de Firewall**: Configurables mediante archivo JSON
4. **Pruebas y Validación**: Scripts para verificar el funcionamiento

---

## Requisitos Previos

### Software Necesario

- **Python 3.x**
- **Mininet** (simulador de redes SDN)
- **POX** (controlador SDN)
- **Wireshark** (captura de tráfico)
- **iperf** (pruebas de rendimiento)

### Instalación de Dependencias

```bash
# Actualización de repositorios
sudo apt-get update

# Mininet
sudo apt-get install mininet

# Instalacion de iperf
sudo apt-get install iperf

# Instalación de Wireshark (opcional)
sudo apt-get install wireshark
```

### Instalación de POX

**Importante**: POX no está incluido en este repositorio (es una dependencia externa). Los módulos custom del firewall están en `controller/`, no en `pox/`.

```bash
# Desde el directorio del proyecto
./install_pox.sh
```

Este script clona POX desde GitHub y lo configura correctamente

---

## Topología

### Descripción de la Topología

La topología consiste en una cadena de **N switches** conectados linealmente, con **4 hosts** distribuidos en los extremos:

```
Caso N ≥ 2:

    h1 ──┐                           ┌── h3
         │                           │
    h2 ──┤── S1 ── S2 ── ... ── SN ───── h4
         
Caso N = 1:

    h1 ──┐
    h2 ──┤── S1
    h3 ──┤
    h4 ──┘
```

### Características

- **Switches**: De S1 a SN (cadena lineal)
- **Hosts**:
  - `h1` y `h2` conectados al switch S1 (primer extremo)
  - `h3` y `h4` conectados al switch SN (último extremo)
- **IPs Asignadas**:
  - h1: `10.0.0.1/24`
  - h2: `10.0.0.2/24`
  - h3: `10.0.0.3/24`
  - h4: `10.0.0.4/24`

---

## Uso

⚠️ **ORDEN IMPORTANTE: Controlador PRIMERO, Topología DESPUÉS**

### 1. Ejecutar el Controlador POX (PRIMERO)

**Terminal 1** - Iniciar el controlador con firewall y L2 learning:

```bash
chmod +x run_controller.sh
./run_controller.sh
```

El controlador quedará escuchando en el puerto 6633 y cargará:
- `forwarding.l2_learning`: Aprendizaje de direcciones MAC
- `firewall`: Reglas de bloqueo (desde `controller/firewall_rules.json`)

**Esperar a ver:**
```
======================================================================
Firewall SDN inicializado
Reglas cargadas: 4
======================================================================
```

### 2. Ejecutar la Topología (DESPUÉS)

**Terminal 2** - SOLO después de que el controlador esté corriendo:

```bash
# Permisos de ejecución al script
chmod +x run_topology.sh

# Ejecución con 2 switches (por defecto)
./run_topology.sh

# Ejecución con N switches (ejemplo: 3)
./run_topology.sh 3

# Ejecución con 1 switch
./run_topology.sh 1
```

### 3. Comandos Útiles en Mininet

Una vez dentro del CLI de Mininet:

```bash
# Ver todos los nodos
mininet> nodes

# Ver todos los enlaces
mininet> net

# Ver información de dump
mininet> dump

# Ping entre todos los hosts
mininet> pingall

# Ping específico
mininet> h1 ping h3

# Ejecutar comando en un host
mininet> h1 ifconfig

# Abrir terminal de un host
mininet> xterm h1

# Salir de mininet
mininet> exit
```

### 4. Pruebas Manuales

Se puede ejecutar la topología manualmente sin el script:

```bash
# Limpia las configuraciones previas
sudo mn -c

# Ejecuta Mininet con topología personalizada
sudo mn --custom topology.py --topo chain,N=2 --mac --arp --switch ovsk --controller remote
```

---

## Estructura del Proyecto

```
proyecto/
├── controller/              # Módulos SDN custom
│   ├── __init__.py
│   ├── firewall.py         # Implementación del firewall
│   ├── utils.py            # Utilidades (carga de reglas)
│   └── firewall_rules.json # Reglas del firewall
├── pox/                     # POX (no versionado, se instala con script)
├── topology.py              # Topología Mininet parametrizable
├── run_controller.sh        # Script para ejecutar POX
├── run_topology.sh          # Script para ejecutar Mininet
├── install_pox.sh           # Script de instalación de POX
└── README.md

```

### Descripción de Archivos

**Topología:**
- **`topology.py`**: Implementa la clase `ChainTopology` que crea la topología parametrizable
- **`run_topology.sh`**: Script bash para facilitar la ejecución de Mininet

**Controlador:**
- **`controller/firewall.py`**: Módulo POX que implementa el firewall SDN
- **`controller/utils.py`**: Funciones auxiliares para cargar reglas
- **`controller/firewall_rules.json`**: Reglas del firewall en formato JSON
- **`run_controller.sh`**: Script para ejecutar POX con los módulos custom

**Instalación:**
- **`install_pox.sh`**: Script para clonar e instalar POX

---

## Verificación de la Topología

### Test 1: Verificar Conectividad Básica

```bash
mininet> pingall
```

**Resultado esperado**: 100% de éxito en todos los pings (sin controlador activo, no hay conectividad)

### Test 2: Ver Estructura de la Red

```bash
mininet> net
```

**Resultado esperado**: Debe mostrar todos los switches, hosts y sus conexiones

### Test 3: Inspeccionar un Host

```bash
mininet> h1 ifconfig
mininet> h1 ip addr show
```

**Resultado esperado**: Ver la interfaz de red con la IP asignada (10.0.0.1)

---

## Notas Importantes

1. **Controlador requerido**: La topología requiere el controlador POX ejecutándose. Sin controlador, los switches no aprenden rutas y no hay conectividad.

2. **Permisos**: Mininet requiere `sudo` para crear interfaces de red virtuales.

3. **Limpieza automática**: El script `run_topology.sh` limpia automáticamente configuraciones previas de Mininet.

4. **Módulos custom**: Los módulos del firewall están en `controller/`, separados del código de POX.

5. **Reglas del firewall**: Edita `controller/firewall_rules.json` para modificar las reglas de bloqueo.

6. **Errores de POX**: Si ves errores de `ipv4.ipv4` en los logs, son un bug conocido de POX con Python 3.12. No afectan la funcionalidad. Ver `KNOWN_ISSUES.md`.

---

## Pruebas del Firewall

### Configuración

Las reglas activas están definidas en `controller/firewall_rules.json`:

1. **Regla 1**: Bloquear puerto 80 (HTTP) - cualquier protocolo
2. **Regla 2**: Bloquear UDP desde h1 (10.0.0.1) al puerto 5001
3. **Regla 3**: Bloquear comunicación bidireccional entre h2 ↔ h3

### Tests Sugeridos

**Test 1: Conectividad general (h2 ↔ h3 bloqueada)**
```bash
mininet> h1 ping -c 4 h4    # Debería funcionar
mininet> h2 ping -c 4 h3    # Bloqueado (regla 3)
mininet> h3 ping -c 4 h2    # Bloqueado (regla 3 reversa)
mininet> h1 ping -c 4 h3    # Debería funcionar
```

**Test 2: UDP puerto 5001 desde h1 bloqueado**
```bash
# Servidor UDP en h4
mininet> h4 iperf -s -u -p 5001 &

# Cliente desde h1 - BLOQUEADO
mininet> h1 iperf -c 10.0.0.4 -u -p 5001
# No debería llegar tráfico (regla 2)

# Cliente desde h2 - PERMITIDO
mininet> h2 iperf -c 10.0.0.4 -u -p 5001
# Debería funcionar (solo h1 está bloqueado)
```

**Test 3: Puerto 80 bloqueado para todos**
```bash
# Servidor HTTP en h1
mininet> h1 python3 -m http.server 80 &

# Desde h4
mininet> h4 curl -m 3 http://10.0.0.1:80
# Timeout (puerto 80 bloqueado - regla 1)

# Servidor en otro puerto
mininet> h1 python3 -m http.server 8000 &
mininet> h4 curl http://10.0.0.1:8000
# Debería funcionar (solo puerto 80 está bloqueado)
```

---

## Integrantes
- Camila Bartocci
- Franco Patiño
- Melina Retamozo
- Matias Sagastume
- Alejo Sendra

Trabajo Práctico N°2 - Introducción a Sistemas Distribuidos (75.43)  
Facultad de Ingeniería, Universidad de Buenos Aires

---

## Referencias

- [Mininet Documentation](http://mininet.org/)
- [POX Controller](https://noxrepo.github.io/pox-doc/html/)
- [OpenFlow Specification](https://www.opennetworking.org/)


