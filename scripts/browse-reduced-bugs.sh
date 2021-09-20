#!/usr/bin/env bash

for f in $(/bin/ls -rS -1 reduced/regression-incompleteness*.smt2); do
	echo "REGRESSION: $f"
	cat $f
	echo "-------------------------"
done
