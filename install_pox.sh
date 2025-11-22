#!/bin/bash
################################################################################
# Script de instalación de POX
#
# Este script clona POX desde GitHub en el directorio del proyecto.
# Los módulos custom del firewall están en controller/, no en pox/ext/.
#
# Uso: ./install_pox.sh
################################################################################

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     INSTALACIÓN DE POX PARA PROYECTO SDN                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar si ya existe POX completo
if [ -f "pox/pox.py" ] && [ -d "pox/pox" ]; then
    echo -e "${GREEN}✓ POX ya está instalado${NC}"
    echo "  POX ejecutable: pox/pox.py"
    echo "  Módulos custom: controller/"
    exit 0
fi

# Verificar si el directorio pox/ existe pero está incompleto
if [ -d "pox" ]; then
    echo -e "${YELLOW}⚠ Directorio pox/ existe pero está incompleto${NC}"
    echo "  Eliminando para reinstalar..."
    rm -rf pox/
fi

echo -e "${YELLOW}Preparando instalación de POX...${NC}"
echo ""

# Clonar POX completo
echo "1. Clonando POX desde GitHub..."
git clone https://github.com/noxrepo/pox.git
cp dns.py pox/pox/lib/packet/dns.py

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Error al clonar POX${NC}"
    exit 1
fi

# Eliminar el .git de POX (no necesitamos versionarlo)
echo "2. Eliminando .git de POX..."
rm -rf pox/.git

echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════╗"
echo "║     ✓ POX INSTALADO CORRECTAMENTE                         ║"
echo "╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Componentes instalados:"
echo "  • pox/pox.py                      - Ejecutable principal de POX"
echo "  • pox/pox/forwarding/l2_learning.py - Módulo L2 learning"
echo ""
echo "Módulos custom del proyecto:"
echo "  • controller/firewall.py          - Firewall SDN (nuestro módulo)"
echo "  • controller/utils.py             - Utilidades"
echo "  • controller/firewall_rules.json  - Reglas del firewall"
echo ""
echo "Para ejecutar el controlador:"
echo "  ./run_controller.sh"
echo ""