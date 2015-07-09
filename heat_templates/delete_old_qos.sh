#!/bin/bash

if rm $RESOUCES/qos_easy.pyc; then 
	echo "qos_easy.pyc deleted"
else
	echo "!!! qos_easy.pyc not deleted !!!"
fi
exit
