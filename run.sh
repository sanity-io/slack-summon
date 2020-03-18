#!/bin/bash
set -euo pipefail

while read line; do
  declare key=$(echo $line | cut -f 1 -d":")
  declare value=$(echo $line | cut -f2 -d " ")
  export "$key"="$value"
done < env.yaml

flask run
