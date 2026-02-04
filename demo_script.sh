#!/bin/bash
# Automated demo script for Labyrinth Game

# Commands to win the game quickly
# This demonstrates a winning path through the labyrinth

cat << 'EOF' | poetry run project
look
help
take torch
inventory
north
solve
10
inventory
west
take treasure_key
inventory
east
north
north
solve
quit
EOF
