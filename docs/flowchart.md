# Robot Grid Navigation - Flowchart

```text
START
  |
  v
Define Grid
  |
  v
Set Start and Goal
  |
  v
Identify Obstacles
  |
  v
Initialize BFS Queue
  |
  v
Add Start to Queue
  |
  v
Mark Start as Visited
  |
  v
Is Queue Empty?
  |
  +---- YES ----> No Path Found ----> END
  |
  NO
  |
  v
Remove Cell from Queue
  |
  v
Is Current Cell Goal?
  |
  +---- YES ----> Reconstruct Path
  |                     |
  |                     v
  |                Path Found
  |                     |
  |                     v
  |                    END
  |
  NO
  |
  v
Check Neighbours
  |
  v
Is Neighbour Valid?
  |
  +---- NO ----> Check Next Neighbour
  |
  YES
  |
  v
Mark as Visited
  |
  v
Store Parent
  |
  v
Add to Queue
  |
  v
Continue BFS