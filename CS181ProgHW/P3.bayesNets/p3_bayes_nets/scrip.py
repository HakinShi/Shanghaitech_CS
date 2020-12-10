for housePos in gameState.getPossibleHouses():
    for obsPos in gameState.getHouseWalls(housePos):
        obsVar = OBS_VAR_TEMPLATE % obsPos
        obsFactor = fac(obsVar)
        for assignment in obsFactor.getAllPossibleAssignmentDicts():
            if dic[assignment[FOOD_HOUSE_VAR]] == housePos:
                if assignment[obsVar] == 'red':
                    prob = PROB_FOOD_RED
                elif assignment[obsVar] == 'blue':
                    prob = 1 - PROB_FOOD_RED
                else:
                    prob = 0
            elif dic[assignment[GHOST_HOUSE_VAR]] == housePos:
                if assignment[obsVar] == 'red':
                    prob = PROB_GHOST_RED
                elif assignment[obsVar] == 'blue':
                    prob = 1 - PROB_GHOST_RED
                else:
                    prob = 0
            else:
                if assignment[obsVar] == 'red':
                    prob = 0
                elif assignment[obsVar] == 'blue':
                    prob = 0
                else:
                    prob = 1
            obsFactor.setProbability(assignment, prob)
        bayesNet.setCPT(obsVar, obsFactor)