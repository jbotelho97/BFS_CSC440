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

    #Set of moves the rubik's cube can make
    moves = [rubik.F, rubik.Fi, rubik.L, rubik.Li,  rubik.U, rubik.Ui]

    #Depth of search
    depth = 1

    startQ = [start] #Holds the starting values we make the frontier from
    endQ = [end] #Holds the ending values we compare the frontier to
    visit = [] #Holds all positions we have already visited
    heapq.heappush(visit, start) #adds start and end to the visited heap
    heapq.heappush(visit, end)
    path = {start: None} #Hold the paths from the node to the start position
    pathE = {end: None} #Holds the paths from the node to the end position
    fromStart = True #True if we are oriendted from the start position

    #true if cube is already solved
    if start == end:
        return []

    #While there exists a list of values to test we will continue to generate the frontier to
    # compare to the end points
    #Termination: When startQ no longer exists we know there is no end points to compare to so
    # we have reached the point where no solution is possible
    while startQ:

        nextQ = []

        depth += 1
        if depth >= 14: #if we go beyond what is the shortest path, terminate
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
                            q = len(sPath) - 1
                            while(q >= 0):
                                # tPath.append(perm_inverse(sPath[q]))
                                tPath.append(perm_inverse(sPath[q]))
                                q -= 1
                            return tPath
                        else:
                            tPath = []
                            if path.get(endQ[k]) != None:
                                tPath = path.get(endQ[k])
                            # move = applyMove(j, startQ[i])
                            # tPath.append(move)
                            tPath.append(perm_inverse(moves[j]))
                            sPath = []
                            if pathE.get(startQ[i]) != None:
                                sPath = pathE.get(startQ[i])
                            q = len(sPath) - 1
                            while q >= 0:
                                tPath.append(perm_inverse(sPath[q]))
                                q -= 1
                            return tPath
                #increasing path
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

def applyMove(move, pos):
    moves = [rubik.F, rubik.Fi, rubik.L, rubik.Li, rubik.U, rubik.Ui]
    return perm_apply(moves[move], pos)




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

