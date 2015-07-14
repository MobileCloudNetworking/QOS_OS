#!/bin/bash

if rm $RESOURCES/qos_easy.pyc; then 
	echo "qos_easy.pyc deleted"
else
	echo "!!! qos_easy.pyc not deleted !!!"
fi	
if rm $RESOURCES/qos_easy.py; then 
	echo "qos_easy.py deleted"
else
	echo "!!! qos_easy.py not deleted !!!"
fi
exit
