#/bin/bash

# This script is useful to help you to locate LAN ports in network switches.
# Connect a laptop into the LAN cable you want to locate and run this script.
# Then, look for a blinking link status led in the switch side.

ACTION=${1-link}

case $ACTION in
speed|-s)
  ifconfig eth0 up
  while : 
  do
    for speed in 10 100 1000
    do
      echo "Setting speed: $speed"
      ethtool -s eth0 speed $speed duplex full
      sleep 4
    done
  done
  ;;
link|-l)
  while :
  do
    echo "Link down"
    ifconfig eth0 down
    sleep 5 
    echo "Link up"
    ifconfig eth0 up
  done
  ;;
*)
  echo "usage: $0 [link|speed]"
  ;;
esac
