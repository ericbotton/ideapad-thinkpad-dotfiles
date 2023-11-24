#!/bin/bash

is_prime() {
    if [ $1 -le 1 ]; then
        return 1
    fi
    for ((i=2; i*i<=$1; i++)); do
        if [ $(($1 % $i)) -eq 0 ]; then
            return 1
        fi
    done
    return 0
}

number=$1

if is_prime $number; then
    echo "prime"
else
    lower=$(($number - 1))
    while ! is_prime $lower; do
        lower=$(($lower - 1))
    done
    echo $lower

    upper=$(($number + 1))
    while ! is_prime $upper; do
        upper=$(($upper + 1))
    done
    echo $upper
fi
