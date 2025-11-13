#!/bin/bash
################################################################################
# Script para iniciar la topología SDN en Mininet
#
# Uso:
#   ./run_topology.sh [N]
#
# Donde:
#   N = Número de switches (por defecto: 2)
#
# Ejemplos:
#   ./run_topology.sh       # Inicia con 2 switches
#   ./run_topology.sh 3     # Inicia con 3 switches
#   ./run_topology.sh 1     # Inicia con 1 switch
################################################################################

# Configuración por defecto
DEFAULT_N=2
CONTROLLER_IP="127.0.0.1"
CONTROLLER_PORT=6633

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     TOPOLOGÍA SDN - MININET                                ║"
echo "║     Introducción a Sistemas Distribuidos (75.43) - FIUBA  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Nro de switches desde argumentos o default
N=${1:-$DEFAULT_N}

# N > 0
if ! [[ "$N" =~ ^[0-9]+$ ]] || [ "$N" -lt 1 ]; then
    echo -e "${RED}Error: N debe ser un número entero positivo${NC}"
    echo "Uso: $0 [N]"
    exit 1
fi

echo -e "${GREEN}Configuración:${NC}"
echo "  • Número de switches: $N"
echo "  • Controlador remoto: $CONTROLLER_IP:$CONTROLLER_PORT"
echo "  • Archivo de topología: topology.py"
echo ""

# archivo de topología existe
if [ ! -f "topology.py" ]; then
    echo -e "${RED}Error: No se encuentra el archivo topology.py${NC}"
    exit 1
fi

# mininet instalado
if ! command -v mn &> /dev/null; then
    echo -e "${RED}Error: Mininet no está instalado${NC}"
    echo "Instalar con: sudo apt-get install mininet"
    exit 1
fi

# warning sobre el controlador
echo -e "${YELLOW}⚠ IMPORTANTE:${NC}"
echo "  AsegUrate de tener el controlador POX ejecutándose antes de iniciar Mininet"
echo "  Ejecuta en otra terminal: ./run_controller.sh"
echo ""
echo -e "Presiona ${GREEN}Enter${NC} para continuar o ${RED}Ctrl+C${NC} para cancelar..."
read

echo -e "\n${BLUE}► Limpiando instancias previas de Mininet...${NC}"
sudo mn -c &> /dev/null

echo -e "\n${BLUE}► Iniciando Mininet con topología de $N switch(es)...${NC}\n"

sudo mn \
    --custom topology.py \
    --topo chain,N=$N \
    --mac \
    --arp \
    --switch ovsk \
    --controller remote,ip=$CONTROLLER_IP,port=$CONTROLLER_PORT

echo -e "\n${BLUE}► Limpiando...${NC}"
sudo mn -c &> /dev/null

echo -e "${GREEN}✓ Topología finalizada${NC}"

