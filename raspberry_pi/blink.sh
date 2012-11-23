#!/bin/bash

# Marcos Martinez
# frommelmak@gmail.com

# Simple script to test the Raspberry Pi GPIO outputs by sending
# a blink signal to the desired output. 

usage (){
cat > /dev/stdout <<EOF

Simple script to test the Raspberry Pi GPIO outputs by sending a
blink signal to the desired output.

usage: $0 GPIO_pin number_of_blinks speed_in_secs

Example: $0 5 10 0.3

EOF
}

on_kill (){

# Restore GPIO settings to avoid errors in the next execution
# This allows you to interrup long blink loops witch Contrl-C

echo 0 > /sys/class/gpio/gpio$1/value
echo "$1" > /sys/class/gpio/unexport && \
echo -e "\n TERM signal recieved! GPIO config restored."
exit 0
}

if [ "$#" -lt "3" ]
then
 usage
 exit 1
fi

# We'll trap all the kill signals coming from the terminal in 
# order to clean up the GPIO interface before ending.
trap 'on_kill $1' SIGINT SIGTERM

#GPIO initialization 
echo "$1" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio$1/direction

LIMIT=$(expr $2 '*' 2)

for ((n=1; n <= LIMIT ; n++))
do
 echo $(expr $n % 2) > /sys/class/gpio/gpio$1/value
 sleep $3 
done

#GPIO clean up 
echo "$1" > /sys/class/gpio/unexport