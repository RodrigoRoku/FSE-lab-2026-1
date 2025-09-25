#!/bin/bash

echo "Primer argumento {$1}"
echo "Segundo argumento {$2}"

if [ -z "${1}" ] || [ -z "${2}" ]; then
  echo "Usando valores de SSID y contraseña por default"
  SSID="RaspberryAP_TapiaHernandez"
  PASSWORD="12345678"
else
  SSID=$1
  PASSWORD=$2
fi

USER="$(whoami)"

if [ $USER != "root" ]; then
  echo "El script debe ejecutarse root"
  exit 1
else
  echo "OK el usuario es root"
fi

if ! dpkg -s dnsmasq &> /dev/null; then
  echo "dnsmasq no està instalado, instalando"
  apt install -y dnsmasq
else
  echo "OK dnsmasq instalado"
fi

systemctl stop dnsmasq

cd /etc
#cd /home/rodrigo/Documents/Embebidos
#crear backup del archivo sino existe
if ! [ -f "dnsmasq.conf.bak" ]; then
  mv dnsmasq.conf dnsmasq.conf.bak
fi

#Creamos el archivo
echo "# Use the require wireless interface - usually wlan0
  interface=wlan0 
  # Reserve 20 IP addresses, set the subnet mask, and lease time
  dhcp-range=192.168.1.200,192.168.1.220,255.255.255.0,24h " > dnsmasq.conf

DHCP_DIR="/etc/NetworkManager/conf.d"

if ! [ -d ${DHCP_DIR} ]; then
  echo "el directorio para el archivo dhcp no existe"
  exit 1
fi

cd $DHCP_DIR
#cd /home/rodrigo/Documents/Embebidos

echo "[main]
dhcp=dhcpcd" > dhcp.conf

nmcli device wifi hotspot con-name AccessPoint ssid ${SSID} band bg password ${PASSWORD} 

nmcli connection modify "AccessPoint" ipv4.addresses "192.168.1.254/24" \
ipv4.gateway "192.168.1.254" ipv4.method manual ipv6.method disabled

systemctl restart NetworkManager

nmcli connection up AccessPoint

nmcli connection show AccessPoint

nmcli connection up AccessPoint



