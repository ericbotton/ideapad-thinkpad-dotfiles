#!/bin/bash
# Here is a bash script that takes one argument and checks if it is a prime number.
# If it is not prime, it prints the closest prime number:
#   bing ChatGTP
is_prime() {
    n=$1
    if ((n <= 1)); then
        return 1
    elif ((n <= 3)); then
        return 0
    elif ((n % 2 == 0 || n % 3 == 0)); then
        return 1
    fi

    i=5
    w=2

    while ((i * i <= n)); do
        if ((n % i == 0)); then
            return 1
        fi

        i=$((i + w))
        w=$((6 - w))
    done

    return 0
}

find_closest_prime() {
    n=$1
    i=1

    while true; do
        if is_prime $((n - i)); then
            echo $((n - i))
            break
        elif is_prime $((n + i)); then
            echo $((n + i))
            break
        fi

        i=$((i + 1))
    done
}

if is_prime $1; then
    echo "Prime"
else
    find_closest_prime $1
fi