#!/bin/bash

if rm $RESOURCES/qos.pyc; then 
	echo "qos.pyc deleted"
else
	echo "!!! qos.pyc not deleted !!!"
fi	
if rm $RESOURCES/qos.py; then 
	echo "qos.py deleted"
else
	echo "!!! qos.py not deleted !!!"
fi
exit
