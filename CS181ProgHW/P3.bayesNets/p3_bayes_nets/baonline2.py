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
            variableDomainsDict[obsVar] = OBS_VALS
            edges.append((FOOD_HOUSE_VAR, obsVar))
            edges.append((GHOST_HOUSE_VAR, obsVar))
    edges.append((X_POS_VAR, FOOD_HOUSE_VAR))
    edges.append((X_POS_VAR, GHOST_HOUSE_VAR))
    edges.append((Y_POS_VAR, FOOD_HOUSE_VAR))
    edges.append((Y_POS_VAR, GHOST_HOUSE_VAR))

    variableDomainsDict[X_POS_VAR] = X_POS_VALS
    variableDomainsDict[Y_POS_VAR] = Y_POS_VALS
    variableDomainsDict[FOOD_HOUSE_VAR] = HOUSE_VALS
    variableDomainsDict[GHOST_HOUSE_VAR] = HOUSE_VALS

    variables = [X_POS_VAR, Y_POS_VAR] + HOUSE_VARS + obsVars
    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net, obsVars


def fillYCPT(bayesNet, gameState):
    """
    Question 2a: Bayes net probabilities

    """

    yFactor = bn.Factor([Y_POS_VAR], [], bayesNet.variableDomainsDict())
    "*** YOUR CODE HERE ***"
    yFactor.setProbability({Y_POS_VAR: BOTH_BOTTOM_VAL}, PROB_BOTH_BOTTOM)
    yFactor.setProbability({Y_POS_VAR: BOTH_TOP_VAL}, PROB_BOTH_TOP)
    yFactor.setProbability({Y_POS_VAR: LEFT_BOTTOM_VAL}, PROB_ONLY_LEFT_BOTTOM)
    yFactor.setProbability({Y_POS_VAR: LEFT_TOP_VAL}, PROB_ONLY_LEFT_TOP)


def fillObsCPT(bayesNet, gameState):
    """
    Question 2b: Bayes net probabilities

    bottomLeftPos, topLeftPos, bottomRightPos, topRightPos = gameState.getPossibleHouses()
"""
    "*** YOUR CODE HERE ***"
    for housePos in gameState.getPossibleHouses():
        for obsPos in gameState.getHouseWalls(housePos):
            obsVar = OBS_VAR_TEMPLATE % obsPos
            uncond = []
            cond = []
            uncond.append(obsVar)
            cond.append(FOOD_HOUSE_VAR)
            cond.append(GHOST_HOUSE_VAR)
            domain = bayesNet.variableDomainsDict()
            obs_factor = bn.Factor(uncond, cond, domain)

            x = obsPos[0]
            y = obsPos[1]
            w = gameState.data.layout.width
            h = gameState.data.layout.height

            if x > 0.5*w:
                if y > 0.5*h:
                    house_val = TOP_RIGHT_VAL
                else:
                    house_val = BOTTOM_RIGHT_VAL
            else:
                if y > 0.5*h:
                    house_val = TOP_LEFT_VAL
                else:
                    house_val = BOTTOM_LEFT_VAL

            all_assignments = obs_factor.getAllPossibleAssignmentDicts()
            for i in all_assignments:
                if house_val == i[FOOD_HOUSE_VAR]:
                    p_r = PROB_FOOD_RED
                    p_b = 1 - PROB_FOOD_RED
                    p_n = 0
                elif house_val == i[GHOST_HOUSE_VAR]:
                    p_r = PROB_GHOST_RED
                    p_b = 1 - PROB_GHOST_RED
                    p_n = 0
                else:
                    p_r = 0
                    p_b = 0
                    p_n = 1

                if i[obsVar] == RED_OBS_VAL:
                    obs_factor.setProbability(i, p_r)
                elif i[obsVar] == BLUE_OBS_VAL:
                    obs_factor.setProbability(i, p_b)
                else:
                    obs_factor.setProbability(i, p_n)
            bayesNet.setCPT(obsVar, obs_factor)


def joinFactors(factors):
    """
    Question 3: Your join implementation

    """

    "*** YOUR CODE HERE ***"
    new_uncond = []
    new_cond = []
    new_var_domain = {}
    for i in factors:
        for j in i.unconditionedVariables():
            if j not in new_uncond:
                new_uncond.append(j)
    for i in factors:
        for j in i.conditionedVariables():
            if j not in new_cond and j not in new_uncond:
                new_cond.append(j)
    for i in factors:
        new_var_domain = dict(new_var_domain.items() + i.variableDomainsDict().items())

    new_factor = Factor(new_uncond, new_cond, new_var_domain)
    assignments = new_factor.getAllPossibleAssignmentDicts()
    for assignment in assignments:
        new_factor.setProbability(assignment, 1)
    for assignment in assignments:
        for factor in factors:
            p = new_factor.getProbability(assignment) * factor.getProbability(assignment)
            new_factor.setProbability(assignment, p)
    return new_factor

def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation

        """

        "*** YOUR CODE HERE ***"
        new_uncond = []
        new_cond = []
        new_domain = factor.variableDomainsDict()
        for i in factor.unconditionedVariables():
            if i not in new_uncond and i != eliminationVariable:
                new_uncond.append(i)
        for i in factor.conditionedVariables():
            if i not in new_cond:
                new_cond.append(i)

        new_factor = Factor(new_uncond, new_cond, new_domain)
        assignments = factor.getAllPossibleAssignmentDicts()

        for assignment in assignments:
            p = new_factor.getProbability(assignment) + factor.getProbability(assignment)
            new_factor.setProbability(assignment, p)
        return new_factor


def normalize(factor):
    """
    Question 5: Your normalize implementation

    """
    "*** YOUR CODE HERE ***"
    new_uncond = []
    new_cond = []
    new_domain = factor.variableDomainsDict()

    for i in factor.unconditionedVariables():
        if i not in new_uncond:
            if len(variableDomainsDict[i]) == 1:
                new_cond.append(i)
            else:
                new_uncond.append(i)
    for i in factor.conditionedVariables():
        if i not in new_cond:
            new_cond.append(i)

    new_factor = Factor(new_uncond, new_cond, new_domain)
    sum = 0
    assignments = factor.getAllPossibleAssignmentDicts()
    for assignment in assignments:
        sum = sum + factor.getProbability(assignment)
    if sum != 0:
        for assignment in assignments:
            p = factor.getProbability(assignment)
            p = p / sum
            new_factor.setProbability(assignment, p)
        return new_factor
    return None



def inferenceByVariableElimination(bayesNet, queryVariables, evidenceDict, eliminationOrder):
    """
    Question 6: Your inference by variable elimination implementation"""
    "*** YOUR CODE HERE ***"
    new_factors = bayesNet.getAllCPTsWithEvidence(evidenceDict)
    for var in eliminationOrder:
        new_factors, joined_factors = joinFactorsByVariable(new_factors, var)
        if not len(joined_factors.unconditionedVariables()) == 1:
            joined_factors = eliminate(joined_factors, var)
            new_factors.append(joined_factors)
    final_joint = joinFactors(new_factors)
    nor = normalize(final_joint)
    return nor