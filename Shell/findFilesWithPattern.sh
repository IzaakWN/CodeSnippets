#!/bin/bash

grep `grep *.e* -e "available/usable" -l | sed 's/.e/.o/g'` -e HOSTNAME