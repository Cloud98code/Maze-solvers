# A* Path-finding algorithm

## What is the A* algorithm?
A* (pronounced "A-star") is a graph traversal and search based algorithm, which is used in many fields of computer science due to its completeness, optimality, and optimal efficiency.
A* was created as part of the Shakey project, which had the aim of building a mobile robot that could plan its own actions.

For the algorithm to properly work, the maze  is decomposed in cells, where each cell can either be free or an obstacle.

A* is formulated in terms of weighted graphs: starting from a chosen starting node of the maze, it aims to find a path to the chosen goal node having the smallest cost (least distance travelled, shortest time, etc.). It does this by maintaining a tree of paths originating at the start node and extending those paths one edge at a time until its termination criterion is satisfied.

At each iteration of its main loop, A* needs to determine which of its paths to extend. It does so based on the cost of the path and an estimate of the cost required to extend the path all the way to the goal. Specifically, A* selects the path that minimizes

*f(n)=g(n)+h(n)*

where n is the next node on the path, *g(n)* is the cost of the path from the start node to n, and *h(n)* is a heuristic function that estimates the cost of the cheapest path from n to the goal. A* terminates when the path it chooses to extend is a path from start to goal or if there are no paths eligible to be extended. The heuristic function is problem-specific. If the heuristic function is admissible – meaning that it never overestimates the actual cost to get to the goal –, A* is guaranteed to return a least-cost path from start to goal. In the given example, Manhattan distance is chosen as *h(n)*.

$h(n) = |(y_2- y_1)| + |(x_2 - x_1)|$

Typical implementations of A* use a priority queue to perform the repeated selection of minimum (estimated) cost nodes to expand. This priority queue is known as the open set, fringe or frontier. At each step of the algorithm, the node with the lowest *f(n)* value is removed from the queue, the f and g values of its neighbors are updated accordingly, and these neighbors are added to the queue. The algorithm continues until a removed node (thus the node with the lowest f value out of all fringe nodes) is a goal node. The f value of that goal is then also the cost of the shortest path, since h at the goal is zero in an admissible heuristic.

The algorithm described so far gives us only the length of the shortest path. To find the actual sequence of steps, the algorithm can be easily revised so that each node on the path keeps track of its predecessor. After this algorithm is run, the ending node will point to its predecessor, and so on, until some node's predecessor is the start node.

## How the implementation works
Once the code is launched, a window with the maze will pop up: from this clicking any free square with the left button of the mouse will set the start and node goal. To reset the start/end nodes, just right click on them. Once the start and end nodes are chosen, pressing the key space button will start the algorithm.
The start node is going to be displayed in Blue, the end node in Orange, visited nodes in red, nodes in the queue in green, the final retrieved path in purple.
Once the algorithm is finished, it is possible to re-initialize a maze just by pressing "*r*" key.