#!/bin/bash
################################################################################
# Script para iniciar el controlador POX con módulos custom
#
# Uso:
#   ./run_controller.sh
#
# Este script inicia POX con:
#   - L2 Learning (forwarding de paquetes)
#   - Firewall (reglas de bloqueo)
################################################################################

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     CONTROLADOR SDN - POX                                  ║"
echo "║     Introducción a Sistemas Distribuidos (75.43) - FIUBA  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar que POX esté instalado
if [ ! -f "pox/pox.py" ]; then
    echo -e "${RED}Error: POX no está instalado${NC}"
    echo "Ejecuta primero: ./install_pox.sh"
    exit 1
fi

# Verificar que existan los módulos custom
if [ ! -f "controller/firewall.py" ]; then
    echo -e "${RED}Error: No se encuentra controller/firewall.py${NC}"
    exit 1
fi

echo -e "${GREEN}Configuración:${NC}"
echo "  • Puerto del controlador: 6633"
echo "  • Módulos cargados:"
echo "    - forwarding.l2_learning (aprendizaje de MACs)"
echo "    - firewall (reglas de bloqueo)"
echo "  • Módulos custom desde: ./controller/"
echo ""

echo -e "${YELLOW}Iniciando controlador POX...${NC}"
echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}"
echo ""

# Ejecutar POX con módulos custom desde controller/
cd pox
PYTHONPATH=../controller:$PYTHONPATH python3.9 ./pox.py log.level --WARNING forwarding.l2_learning firewall
    log.level --WARNING \
    py --completion \
    --ext-path=../controller \
    forwarding.l2_learning \
    firewall

echo -e "\n${GREEN}✓ Controlador detenido${NC}"