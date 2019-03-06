from rubik import perm_apply
import rubik
import heapq


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """

    moves = [rubik.F, rubik.Fi, rubik.L, rubik.Li,  rubik.U, rubik.Ui]

    depth = 1

    startQ = [start]
    endQ = [end]
    visit = []
    heapq.heappush(visit, start)
    heapq.heappush(visit, end)
    path = {start: None}

    if start == end:
        return []

    while startQ:

        nextQ = []

        depth += 1
        if depth >= 14:
            break

        for i in range(len(startQ)):

            adjList = genAdj(startQ[i])

            #j - 0=F, 1=Fi, 2=L, 3=Li, 4=U, 5=Ui
            for j in range(len(adjList)):
                if adjList[j] in endQ:
                    tPath = []
                    if path.get(startQ[i]) != None:
                        tPath = path.get(adjList[j])
                    tPath.append(moves[j])
                    return tPath
                if adjList[j] not in visit:
                    heapq.heappush(visit, adjList[j])
                    heapq.heappush(nextQ, adjList[j])
                    tPath = []
                    if path.get(startQ[i]) != None:
                        tPath = path.get(startQ[i])
                    tPath.append(moves[j])
                    nuPath = {adjList[j]: tPath}
                    path.update(nuPath)


        if(len(nextQ) < len(endQ)):
            startQ = nextQ
        else:
            startQ = endQ
            endQ = nextQ

    return






# #
# def bfs(s, e, adjS, adjE):
#     depth = {s: 0}
#     parent = {s: None}
#     i = 1
#     frontier = [s]
#     while frontier:
#         next = []
#         for u in frontier:
#             for v in adj[u]:
#                 if v not in depth:
#                     depth[v] = i
#                     parent[v] = u
#                     next.append(v)
#         frontier = next
#         i += 1
#     return parent

def genAdj(start):
    list = []

    list.append(perm_apply(rubik.F, start))
    list.append(perm_apply(rubik.Fi, start))
    list.append(perm_apply(rubik.L, start))
    list.append(perm_apply(rubik.Li, start))
    list.append(perm_apply(rubik.U, start))
    list.append(perm_apply(rubik.Ui, start))

    return list


