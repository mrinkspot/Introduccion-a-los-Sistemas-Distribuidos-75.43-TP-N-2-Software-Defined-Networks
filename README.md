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

**Importante**: POX no está incluido completamente en este repositorio (es una dependencia externa). Solo los módulos custom del firewall están versionados en `pox/ext/`.

#### Instalación Automática

```bash
# Desde el directorio del proyecto
./install_pox.sh
```

Este script:
- Clona POX desde GitHub
- Preserva automáticamente los módulos custom del firewall
- Configura todo correctamente

#### Instalación Manual

Si preferís instalar manualmente:

```bash
# 1. Hace un backup de los módulos custom
mkdir -p .tmp_backup
cp -r pox/ext/* .tmp_backup/
cp pox/.gitignore .tmp_backup/

# 2. Elimina el directorio parcial y clona POX completo
rm -rf pox/
git clone https://github.com/noxrepo/pox.git

# 3. Restaura los módulos custom
cp .tmp_backup/* pox/ext/
cp .tmp_backup/.gitignore pox/
rm -rf pox/.git .tmp_backup/
```

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

### 1. Ejecutar la Topología

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

### 2. Comandos Útiles en Mininet

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

### 3. Pruebas Manuales

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
.
├── topology.py              # Topología parametrizable de Mininet
├── run_topology.sh          # Script para iniciar la topología
└── README.md                # Este archivo
```

### Descripción de Archivos

- **`topology.py`**: Implementa la clase `ChainTopology` que crea la topología parametrizable
- **`run_topology.sh`**: Script bash para facilitar la ejecución de Mininet

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

1. Esta topología todavía requiere un controlador SDN externo. Sin controlador, los switches no van a aprender y no va a haber conectividad.

2. Mininet requiere permisos de superusuario (`sudo`) para crear interfaces de red virtuales.

3. El script `run_topology.sh` limpia automáticamente las configuraciones previas de Mininet.

4. Por ahora solo tenemos la topología. Las siguientes fases incluirán:
   - Controlador POX con L2 learning
   - Firewall con reglas configurables
   - Scripts de prueba automatizados

---

## TODO

- [ ] Implementar controlador POX con L2 learning
- [ ] Agregar funcionalidad de firewall
- [ ] Crear archivo de reglas JSON
- [ ] Implementar scripts de prueba
- [ ] Documentar con capturas de Wireshark

---

## Comandos para testear 

en una conso levantar la topologia con n switches

en otra el controlador open flow (recordar colocar el archivo firewall y sus dependencias en la carpeta "ext" del repositorio de pox):
```bash
   python3.9 ./pox.py forwarding.l2_learning firewall
```

```bash
mininet> h1 ping -c 4 h4 #deberia andar
mininet> h2 ping -c 4 h3 #no deberia andar
mininet> h2 ping -c 4 h3 #tampoco

mininet> h2 iperf -s -u -p 5001 &  # levantamos servidor
mininet> h1 iperf -c -u -p 5001  # tratamos de mandar - no deberia llegar nada a h2 
mininet> h4 iperf -c -u -p 5001  # deberia funcionar

#probar condicion del puerto 80
```

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


