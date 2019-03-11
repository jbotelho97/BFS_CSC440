from rubik import perm_apply, perm_inverse
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
    pathE = {end: None}
    fromStart = True


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
            #j is the specific move done to the cube
            for j in range(len(adjList)):
                # if adjList[j] in endQ:
                #     tPath = []
                #     if path.get(startQ[i]) != None:
                #         tPath = path.get(adjList[j])
                #     tPath.append(moves[j])
                #     return tPath
                for k in range(len(endQ)):
                    #merging
                    if adjList[j] == endQ[k]:
                        if fromStart:
                            tPath = []
                            if path.get(startQ[i]) != None:
                                tPath = path.get(startQ[i])
                            tPath.append(moves[j])
                            sPath = []
                            if pathE.get(endQ[k]) != None:
                                sPath = pathE.get(endQ[k])
                            for q in range(len(sPath) - 1, 0, -1):
                                tPath.append(perm_inverse(sPath[q]))
                            return tPath
                        else:
                            tPath = []
                            if path.get(startQ[i]) != None:
                                tPath = path.get(endQ[k])
                            tPath.append(perm_inverse(moves[j]))
                            sPath = []
                            if pathE.get(startQ[i]) != None:
                                sPath = pathE.get(startQ[i])
                            for q in range(len(sPath) - 1, 0, -1):
                                tPath.append(perm_inverse(sPath[q]))
                            return tPath
                if adjList[j] not in visit:
                    heapq.heappush(visit, adjList[j])
                    heapq.heappush(nextQ, adjList[j])
                    if fromStart:
                        tPath = []
                        if path.get(startQ[i]) != None:
                            tPath = path.get(startQ[i])
                        tPath.append(moves[j])
                        nuPath = {adjList[j]: tPath}
                        path.update(nuPath)
                    else:
                        tPath = []
                        if path.get(startQ[i]) != None:
                            tPath = pathE.get(startQ[i])
                        tPath.append(moves[j])
                        nuPath = {adjList[j]: tPath}
                        pathE.update(nuPath)

        if(len(nextQ) < len(endQ)):
            startQ = nextQ
        else:
            startQ = endQ
            endQ = nextQ
            if fromStart:
                fromStart = False
            else:
                fromStart = True

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


