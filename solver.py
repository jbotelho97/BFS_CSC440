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
        if depth >= 14:  # if we go beyond what is the shortest path, terminate
            break


        # While startQ exists and has values that a frontier can be made from the loop will continue to generate the
        # frontier until a match is found or the end of the list is reached
        # Termination: The loop will terminate when either a match is found signalling that the shortest path has
        # been found or it reaches the end of the startQ meaning that the next frontier has been found
        for i in range(len(startQ)):

            adjList = genAdj(startQ[i])#generates the frontier by calculating all adjacent moves

            #j - 0=F, 1=Fi, 2=L, 3=Li, 4=U, 5=Ui
            #j is the specific move done to the cube
            #While there exists a node j in the adjList we will compare it to the frontier on the other side
            #If a match is found we return the shortest path other wise we add the node to the visisted heap
            #and add its path to the dictionary
            for j in range(len(adjList)):
                #While an element k exists in the endQ frontier we will compare every element k with every element
                #j from the adjList to see if an equality exists, if one exists then a match and by extension a shortest
                #path has been found.
                #The loop will terminate when the end frontier has been completly checked meaning that element j is not
                # on both the start and ending frontiers
                for k in range(len(endQ)):
                    #This is where we merge the list depending on if we are currently adding from the start side
                    #or the end side
                    if adjList[j] == endQ[k]:
                        if fromStart:#If we are oriented from the start
                            tPath = []
                            if path.get(startQ[i]) != None:
                                tPath = path.get(startQ[i])
                            tPath.append(moves[j])
                            sPath = []
                            if pathE.get(endQ[k]) != None:
                                sPath = pathE.get(endQ[k])
                            q = len(sPath) - 1
                            #Loops through the path oriented on the end in reverse appending it to the working path
                            while(q >= 0):
                                tPath.append(perm_inverse(sPath[q]))
                                q -= 1
                            return tPath
                        else: #If we are oriented from the end side
                            tPath = []
                            if path.get(endQ[k]) != None:
                                tPath = path.get(endQ[k])
                            tPath.append(perm_inverse(moves[j]))
                            sPath = []
                            if pathE.get(startQ[i]) != None:
                                sPath = pathE.get(startQ[i])
                            q = len(sPath) - 1
                            # Loops through the path oriented on the end in reverse appending it to the working path
                            while q >= 0:
                                tPath.append(perm_inverse(sPath[q]))
                                q -= 1
                            return tPath
                #This will check if we have already visited the current node and if we did not, we add its path to the
                #corresonding dictionary
                if adjList[j] not in visit:
                    heapq.heappush(visit, adjList[j]) #add to visit
                    heapq.heappush(nextQ, adjList[j]) #add to the next frontier
                    if fromStart: #If we are oriendted from the start
                        tPath = []
                        if path.get(startQ[i]) != None:
                            tPath = path.get(startQ[i])
                        tPath.append(moves[j])
                        nuPath = {adjList[j]: tPath}
                        path.update(nuPath)
                    else: #If we are oriendinted from the end/target
                        tPath = []
                        if path.get(startQ[i]) != None:
                            tPath = pathE.get(startQ[i])
                        tPath.append(moves[j])
                        nuPath = {adjList[j]: tPath}
                        pathE.update(nuPath)
        #This will flip the algorithm to either fuction from the start of the graph or the end
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

def genAdj(start):
    list = []

    list.append(perm_apply(rubik.F, start))
    list.append(perm_apply(rubik.Fi, start))
    list.append(perm_apply(rubik.L, start))
    list.append(perm_apply(rubik.Li, start))
    list.append(perm_apply(rubik.U, start))
    list.append(perm_apply(rubik.Ui, start))

    return list
