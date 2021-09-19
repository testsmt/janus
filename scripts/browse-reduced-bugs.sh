#!/usr/bin/env bash

for f in reduced/regression-incompleteness*.smt2; do
	echo "REGRESSION: $f"
	cat $f
	echo "-------------------------"
done
