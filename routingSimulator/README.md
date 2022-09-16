# Routing Simulator
This program simulates routing in network. Using this, we can add
a new router, modify and distribute routing tables of a router to
other routers.

## Repository Structure
- RoutingSimulator.py : A routing Simulator
- networkinfo.txt: a sample file containing routing information
- README.md

## Dependencies
python3

## RUN
> python3 RoutingSimulator.py

The program supports two mode to build routing simulator. First, it can takes
a filename as input to read the routing information from the
file. Second, it possible to enter information using command prompt

To get help, type help in the command prompt

## Input File format
The format of the files is:
name!neighbour1;neighbourN!network1:distance1

Content of the line:

    - The line always contains two exclamation marks
    - The name of the router is on the left side of the first exclamation mark
    - Between the exclamation marks there are the names of the neighbouring
      routers separated by semicolons or nothing if there are no neighbouring
      routers
    - On the right side of the later exclamation mark there is the content of
      the routing table.
