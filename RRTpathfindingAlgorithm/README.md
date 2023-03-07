# RRT Path-finding algorithm

## What is the RRT algorithm?
A rapidly exploring random tree (RRT) is an algorithm designed to efficiently search nonconvex, high-dimensional spaces by randomly building a space-filling tree. The tree is constructed incrementally from samples drawn randomly from the search space and is inherently biased to grow towards large unsearched areas of the problem.

An RRT grows a tree rooted at the starting configuration by using random samples from the search space. As each sample is drawn, a connection is attempted between it and the nearest state in the tree. If the connection is feasible (passes entirely through free space and obeys any constraints), this results in the addition of the new state to the tree. With uniform sampling of the search space, the probability of expanding an existing state is proportional to the size of its Voronoi region. As the largest Voronoi regions belong to the states on the frontier of the search, this means that the tree preferentially expands towards large unsearched areas.

The length of the connection between the tree and a new state is frequently limited by a growth factor. If the random sample is further from its nearest state in the tree than this limit allows, a new state at the maximum distance from the tree along the line to the random sample is used instead of the random sample itself. The random samples can then be viewed as controlling the direction of the tree growth while the growth factor determines its rate. This maintains the space-filling bias of the RRT while limiting the size of the incremental growth. 

## How the implementation works
Once the code is launched, a window with the map will pop up: from this, clicking any free square with the left button of the mouse will set the start and node goal. To reset the start/end nodes, just right click on them. Once the start and end nodes are chosen, pressing the key space button will start the algorithm.
The start node is going to be displayed in Blue, the end node in Orange, visited nodes in red, the final retrieved path in purple.
Once the algorithm is finished, it is possible to re-initialize a map by just pressing "*r*" key.