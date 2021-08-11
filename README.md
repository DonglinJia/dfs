# Depth First Search for HuaRongDao

Depth First Search is an uniformed search algorithm.
- Treats the frontier as a stack (LIFO)
- Expands the last/most recent node added to the frontier
- It starts one successor and explores all the paths first, then turns to another successor then explores all its paths, and repeat, until it reaches all successors for current node.
- Properties of DFS:
  * b: branching factor (there are less than b successors for each node)
  * m: maximum depth
  * d: depth of shallowest goal node
- Space complexity is O(bm), we might find the deepest result (m level).
- Time complexity is O(bm) (visit all the states)
- It may not find a solution if there is an infinite path forever.

Please visit https://donglinjia.github.io/angular-website/assets/files/AI.pdf page 6 for more explanation.
