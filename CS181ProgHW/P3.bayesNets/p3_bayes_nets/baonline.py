

def constructBayesNet(gameState):
    """
    Question 1: Bayes net structure

    """

    obsVars = []
    edges = []
    variableDomainsDict = {}

    "*** YOUR CODE HERE ***"
    for housePos in gameState.getPossibleHouses():
        for obsPos in gameState.getHouseWalls(housePos):
            obsVar = OBS_VAR_TEMPLATE % obsPos
            obsVars.append(obsVar)
    edges.append((X_POS_VAR, FOOD_HOUSE_VAR))
    edges.append((X_POS_VAR, GHOST_HOUSE_VAR))
    edges.append((Y_POS_VAR, FOOD_HOUSE_VAR))
    edges.append((Y_POS_VAR, GHOST_HOUSE_VAR))

    for obsVar in obsVars:
        edges.append((FOOD_HOUSE_VAR, obsVar))
        edges.append((GHOST_HOUSE_VAR, obsVar))
    variableDomainsDict[X_POS_VAR] = X_POS_VALS
    variableDomainsDict[Y_POS_VAR] = Y_POS_VALS
    variableDomainsDict[FOOD_HOUSE_VAR] = HOUSE_VALS
    variableDomainsDict[GHOST_HOUSE_VAR] = HOUSE_VALS

    for obsVar in obsVars:
        variableDomainsDict[obsVar] = OBS_VALS

    variables = [X_POS_VAR, Y_POS_VAR] + HOUSE_VARS + obsVars
    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net, obsVars


def fillYCPT(bayesNet, gameState):
    """
    Question 2a: Bayes net probabilities

    """

    yFactor = bn.Factor([Y_POS_VAR], [], bayesNet.variableDomainsDict())
    "*** YOUR CODE HERE ***"
    from layout import PROB_BOTH_TOP, PROB_BOTH_BOTTOM, PROB_ONLY_LEFT_TOP, PROB_ONLY_LEFT_BOTTOM
    yFactor.setProbability({Y_POS_VAR: BOTH_BOTTOM_VAL}, PROB_BOTH_BOTTOM)
    yFactor.setProbability({Y_POS_VAR: BOTH_TOP_VAL}, PROB_BOTH_TOP)
    yFactor.setProbability({Y_POS_VAR: LEFT_BOTTOM_VAL}, PROB_ONLY_LEFT_BOTTOM)
    yFactor.setProbability({Y_POS_VAR: LEFT_TOP_VAL}, PROB_ONLY_LEFT_TOP)
    bayesNet.setCPT(Y_POS_VAR, yFactor)


def fillObsCPT(bayesNet, gameState):
    """
    Question 2b: Bayes net probabilities

    """

    bottomLeftPos, topLeftPos, bottomRightPos, topRightPos = gameState.getPossibleHouses()

    "*** YOUR CODE HERE ***"
    dictionary = {}
    dictionary[BOTTOM_LEFT_VAL] = bottomLeftPos
    dictionary[TOP_LEFT_VAL] = topLeftPos
    dictionary[BOTTOM_RIGHT_VAL] = bottomRightPos
    dictionary[TOP_RIGHT_VAL] = topRightPos

    for housePos in gameState.getPossibleHouses():
        for obsPos in gameState.getHouseWalls(housePos):
            obsVar = OBS_VAR_TEMPLATE % obsPos
            obsFactor = bn.Factor([obsVar], HOUSE_VARS, bayesNet.variableDomainsDict())
            for assignment in obsFactor.getAllPossibleAssignmentDicts():
                if dictionary[assignment[FOOD_HOUSE_VAR]] == housePos:
                    if assignment[obsVar] == 'red':
                        prob = PROB_FOOD_RED
                    elif assignment[obsVar] == 'blue':
                        prob = 1 - PROB_FOOD_RED
                    else:
                        prob = 0
                elif dictionary[assignment[GHOST_HOUSE_VAR]] == housePos:
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


def getMostLikelyFoodHousePosition(evidence, bayesNet, eliminationOrder):
    """
    Question 7: Marginal inference for pacman

    """
    "*** YOUR CODE HERE ***"
    factor = inference.inferenceByVariableElimination(bayesNet, ['foodHouse', 'ghostHouse'], evidence, eliminationOrder)
    probability = float('-inf')
    d = dict()
    for assignmentDict in factor.getAllPossibleAssignmentDicts():
        p = factor.getProbability(assignmentDict)
        if p > probability:
            probability = p
            d = assignmentDict
    return d


def joinFactors(factors):
    """
    Question 3: Your join implementation

    """

    "*** YOUR CODE HERE ***"
    joinedConditionedVariables = set()
    joinedUnconditionedVariables = set()
    for factor in factors:
        for condVar in factor.conditionedVariables():
            joinedConditionedVariables.add(condVar)
        for uncondVar in factor.unconditionedVariables():
            joinedUnconditionedVariables.add(uncondVar)
    for uncondVar in joinedUnconditionedVariables:
        if uncondVar in joinedConditionedVariables:
            joinedConditionedVariables.remove(uncondVar)
    joinedFactor = Factor(joinedUnconditionedVariables, joinedConditionedVariables, factors[0].variableDomainsDict())
    for joinedAssignment in joinedFactor.getAllPossibleAssignmentDicts():
        factorAssignmentProduct = 1
        for factor in factors:
            factorAssignmentProduct = factorAssignmentProduct * Factor.getProbability(factor, joinedAssignment)
        Factor.setProbability(joinedFactor, joinedAssignment, factorAssignmentProduct)

    return joinedFactor

def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation

        """

        "*** YOUR CODE HERE ***"
        unconditionedVariables = factor.unconditionedVariables()
        unconditionedVariables.remove(eliminationVariable)
        newFactor = Factor(unconditionedVariables, factor.conditionedVariables(), factor.variableDomainsDict())

        for assignment in factor.getAllPossibleAssignmentDicts():
            newAssignment = dict(assignment)
            del newAssignment[eliminationVariable]
            newProb = newFactor.getProbability(newAssignment) + factor.getProbability(assignment)
            newFactor.setProbability(newAssignment, newProb)

        return newFactor


def normalize(factor):
    """
    Question 5: Your normalize implementation

    """
    "*** YOUR CODE HERE ***"
    domains = factor.variableDomainsDict()
    unconditioned = factor.unconditionedVariables()
    conditioned = factor.conditionedVariables()
    for variable, domain in domains.items():
        if len(domain) == 1:
            if variable not in conditioned and variable in unconditioned:
                conditioned.add(variable)
            if variable in unconditioned:
                unconditioned.remove(variable)

    newFactor = Factor(unconditioned, conditioned, factor.variableDomainsDict())
    possibleDicts = newFactor.getAllPossibleAssignmentDicts()
    total = 0

    for p in possibleDicts:
        prob = factor.getProbability(p)
        total = total + prob
    for p in possibleDicts:
        prob = factor.getProbability(p)
        newFactor.setProbability(p, prob/total)
    return newFactor



def inferenceByVariableElimination(bayesNet, queryVariables, evidenceDict, eliminationOrder):
    """
    Question 6: Your inference by variable elimination implementation"""
    tables = bayesNet.getAllCPTsWithEvidence(evidenceDict)

    for i in eliminationOrder:
        joinTuple = joinFactorsByVariable(tables, i)
        tables = joinTuple[0]
        if len(joinTuple[1].unconditionedVariables()) == 1:
            continue
        tables.append(eliminate(joinTuple[1], i))
    newFactor = joinFactors(tables)
    return normalize(newFactor)