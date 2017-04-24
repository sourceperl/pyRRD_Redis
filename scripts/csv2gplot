#!/bin/bash

# vars
NAME=$(basename $0)
USAGE=$(printf "Usage: %s: [-h] [-r '[min:max]'] CSV_FILE [CSV_FILE]" $NAME)

# parse optionals args
while getopts ':hr:' OPTION
do
    case $OPTION in
    h)
        printf "load RRD CSV files to gnuplot tools\n\n"
        printf "$USAGE\n\n"
        printf "  -h             print this help message\n"
        printf "  -r [min:max]   set Y range (like [12000:13000])\n"
        exit 0
        ;;
    r)
        CMD_RANGE="set yrange $OPTARG"
        ;;
    esac
done
shift $(($OPTIND - 1))

# format command line for 'plot' command
for FILE in $@; do
    PLOT_ARG+="'$FILE' u 1:2 with lines title '$FILE',"
done

# run gnuplot
gnuplot -p <<EOF
#set title 'Wobbe test'
set timefmt '%Y-%m-%d %H:%M:%S'
set xdata time
$CMD_RANGE
set datafile sep ';'
plot $PLOT_ARG
EOF