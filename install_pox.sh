#!/bin/bash
################################################################################
# Script de instalación de POX preservando módulos custom
#
# Este script clona POX y preserva los módulos custom del firewall
# que ya están versionados en este repositorio.
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

# Verifica si ya existe POX completo
if [ -d "pox/pox" ] && [ -f "pox/pox.py" ]; then
    echo -e "${GREEN}✓ POX ya está instalado y completo${NC}"
    echo "Los módulos custom del firewall están en: pox/ext/"
    exit 0
fi

# Verifica si existe el directorio pox/ext con nuestros archivos
if [ ! -f "pox/ext/firewall.py" ]; then
    echo -e "${RED}Error: No se encuentran los módulos custom en pox/ext/${NC}"
    echo "Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

echo -e "${YELLOW}Preparando instalación de POX...${NC}"

# Guarda nuestros módulos custom temporalmente
echo "1. Respaldando módulos custom del firewall..."
mkdir -p .tmp_firewall_backup
cp pox/ext/firewall.py .tmp_firewall_backup/
cp pox/ext/utils.py .tmp_firewall_backup/
cp pox/ext/firewall_rules.json .tmp_firewall_backup/
cp pox/.gitignore .tmp_firewall_backup/

# Elimina el directorio pox parcial
echo "2. Eliminando directorio pox/ parcial..."
rm -rf pox/

# Clona POX completo
echo "3. Clonando POX desde GitHub..."
git clone https://github.com/noxrepo/pox.git

if [ $? -ne 0 ]; then
    echo -e "${RED}Error al clonar POX${NC}"
    # Restaurar backup
    mkdir -p pox/ext
    cp .tmp_firewall_backup/* pox/
    mv pox/firewall.py pox/ext/
    mv pox/utils.py pox/ext/
    mv pox/firewall_rules.json pox/ext/
    rm -rf .tmp_firewall_backup
    exit 1
fi

# Restaura nuestros módulos custom
echo "4. Restaurando módulos custom del firewall..."
cp .tmp_firewall_backup/firewall.py pox/ext/
cp .tmp_firewall_backup/utils.py pox/ext/
cp .tmp_firewall_backup/firewall_rules.json pox/ext/
cp .tmp_firewall_backup/.gitignore pox/

# Elimina el .git de POX para evitar conflictos
echo "5. Eliminando .git de POX (no necesitamos versionarlo)..."
rm -rf pox/.git

# Limpia backup
rm -rf .tmp_firewall_backup

echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════╗"
echo "║     ✓ POX INSTALADO CORRECTAMENTE                         ║"
echo "╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Módulos disponibles:"
echo "  • pox/pox.py                     - Ejecutable principal de POX"
echo "  • pox/forwarding/l2_learning.py  - Módulo L2 learning de POX"
echo "  • pox/ext/firewall.py            - Nuestro firewall (custom)"
echo "  • pox/ext/utils.py               - Nuestras utilidades (custom)"
echo "  • pox/ext/firewall_rules.json    - Nuestras reglas (custom)"
echo ""
echo "Para ejecutar el controlador:"
echo "  cd pox"
echo "  ./pox.py log.level --WARNING forwarding.l2_learning ext.firewall"
echo ""

