#!/bin/sh

# Check if the argument is a positive integer
if [ ! -n "$1" ] || [ ! "$1" -gt 0 ]; then
  echo "Usage: $0 <number>"
  exit 1
fi

# Function to check if a number is prime
function is_prime(){
  local number="$1"
  for ((i=2; i*i<=number; i++)); do
    if [ $((number%i)) -eq 0 ]; then
      return 1
    fi
  done
  return 0
}

# Find the next lower prime number
next_lower_prime=$((1))
while [ "$next_lower_prime" -lt "$1" ]; do
  next_lower_prime=$((next_lower_prime + 1))
  if is_prime "$next_lower_prime"; then
    break
  fi
done

# Find the next higher prime number
next_higher_prime=$((1))
while [ "$next_higher_prime" -le "$1" ]; do
  next_higher_prime=$((next_higher_prime + 1))
  if is_prime "$next_higher_prime"; then
    break
  fi
done

# Print the results
echo "The next lower prime number is $next_lower_prime."
echo "The next higher prime number is $next_higher_prime."

