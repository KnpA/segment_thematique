#!/bin/bash
#
# bash tokenizer.sh LANGUAGE input_file
#

perl tokenizer.pl --no-line-seg --datafile tokenizer.data --language $1 < $2


