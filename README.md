# Sprout

## Setup
1. Copy the URL: https://github.com/jba395/Sprout.git
1. From the command line in the directory of your choice, `git clone <url>`
1. Enter the newly-created directory with the same name as this repository
1. Run `python ./main.py` to execute the program

## Bugs
- Some output nodes have more than the allotted limit of neighbors
- One output featured tomatoes and potatoes in the graph, and they were never picked in the logs
    - Nothing is ever assigned an edge weight of 4 (designating "foes"), which shouldn't be the case