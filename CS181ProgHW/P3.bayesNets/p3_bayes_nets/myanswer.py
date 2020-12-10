def constructBayesNet(gameState):
    """
    Question 1: Bayes net structure

    """

    obsVars = []
    edges = []
    variableDomainsDict = {}

    "*** YOUR CODE HERE ***"
    def apend(a, b):
        a.append(b)

    pos = [(X_POS_VAR, FOOD_HOUSE_VAR), (X_POS_VAR, GHOST_HOUSE_VAR),
           (Y_POS_VAR, FOOD_HOUSE_VAR), (Y_POS_VAR, GHOST_HOUSE_VAR)]
    for edg in pos:
        apend(edges,edg)

    for housePos in gameState.getPossibleHouses():
        for obsPos in gameState.getHouseWalls(housePos):
            obsVar = OBS_VAR_TEMPLATE % obsPos
            obsVars.append(obsVar)
            ## variable
            variableDomainsDict[obsVar] = OBS_VALS
            apend(edges, (FOOD_HOUSE_VAR, obsVar))
            apend(edges, (GHOST_HOUSE_VAR, obsVar))

    dx = [X_POS_VAR, Y_POS_VAR, FOOD_HOUSE_VAR, GHOST_HOUSE_VAR]
    dy = [X_POS_VALS, Y_POS_VALS, HOUSE_VALS, HOUSE_VALS]
    for i in range(0,4):
        variableDomainsDict[dx[i]] = dy[i]

    variables = [X_POS_VAR, Y_POS_VAR] + HOUSE_VARS + obsVars
    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net, obsVars


def fillYCPT(bayesNet, gameState):
    """
    Question 2a: Bayes net probabilities

    """

    yFactor = bn.Factor([Y_POS_VAR], [], bayesNet.variableDomainsDict())
    "*** YOUR CODE HERE ***"
    ypositionlist = [{Y_POS_VAR: BOTH_BOTTOM_VAL}, {Y_POS_VAR: BOTH_TOP_VAL}, {Y_POS_VAR: LEFT_BOTTOM_VAL}, {Y_POS_VAR: LEFT_TOP_VAL}]
    valuelist = [PROB_BOTH_BOTTOM, PROB_BOTH_TOP, PROB_ONLY_LEFT_BOTTOM, PROB_ONLY_LEFT_TOP]
    def setpr(l1,l2):
        for i in range(0, len(l1)):
            yFactor.setProbability(l1[i],l2[i])

    setpr(ypositionlist, valuelist)
    bayesNet.setCPT(Y_POS_VAR, yFactor)


def fillObsCPT(bayesNet, gameState):
    """
    Question 2b: Bayes net probabilities

    """

    bottomLeftPos, topLeftPos, bottomRightPos, topRightPos = gameState.getPossibleHouses()

    "*** YOUR CODE HERE ***"
    # print('possible houses are:  ',gameState.getPossibleHouses())
    # possible houses are:   [(3, 3), (3, 7), (11, 3), (11, 7)]
    # print('walls', gameState.getHouseWalls((3, 7)))
    # walls {(4, 4), (2, 3), (4, 3), (2, 2), (4, 2), (3, 4), (2, 4)}

    '''
     print("dcit is: ", obsFactor.getAllPossibleAssignmentDicts())
     dcit is:  [{'ghostHouse': 'topLeft', 'foodHouse': 'topLeft', 'obs(15,12)': 'blue'}, 
    {'ghostHouse': 'topLeft', 'foodHouse': 'topLeft', 'obs(15,12)': 'red'},
     {'ghostHouse': 'topLeft', 'foodHouse': 'topLeft', 'obs(15,12)': 'none'},
    {'ghostHouse': 'topLeft', 'foodHouse': 'topRight', 'obs(15,12)': 'blue'},
     {'ghostHouse': 'topLeft', 'foodHouse': 'topRight', 'obs(15,12)': 'red'}, 

    obsvar is : obs(4,4)
    obsfac is : P(obs(4,4) | foodHouse, ghostHouse)
   dic[assignment[FOOD_HOUSE_VAR]]   =  (3, 7)
   assignment[FOOD_HOUSE_VAR]   =   topLeft


    '''
    dic = {}
    p = [BOTTOM_LEFT_VAL, TOP_LEFT_VAL, BOTTOM_RIGHT_VAL, TOP_RIGHT_VAL]
    pv = [bottomLeftPos, topLeftPos, bottomRightPos, topRightPos]
    for i in range(0, len(p)):
        dic[p[i]] = pv[i]

    def fac(ov):
        return bn.Factor([ov], HOUSE_VARS, bayesNet.variableDomainsDict())

    for housePos in gameState.getPossibleHouses():
        for obsPos in gameState.getHouseWalls(housePos):
            obsVar = OBS_VAR_TEMPLATE % obsPos
            # print('obsvar is :', obsVar)
            # print('\n')
            obsFactor = fac(obsVar)
            # print('obsfac is :', obsFactor)
            # print('\n')

            def setpro(pro):
                list = [pro, 1 - pro, 0]
                return list

            def setzero():
                return [0, 0, 1]

            for housePos in gameState.getPossibleHouses():
                for obsPos in gameState.getHouseWalls(housePos):
                    obsVar = OBS_VAR_TEMPLATE % obsPos
                    # print('obsvar is :', obsVar)
                    # print('\n')
                    obsFactor = fac(obsVar)
                    # print('obsfac is :', obsFactor)
                    # print('\n')

                    for assignment in obsFactor.getAllPossibleAssignmentDicts():
                        # print("assignment is like: ", assignment)
                        # print("dcit is: ", obsFactor.getAllPossibleAssignmentDicts())
                        # print('dict and assignment[FOOD_HOUSE_VAR] is: ', dic[assignment[FOOD_HOUSE_VAR]], assignment[FOOD_HOUSE_VAR])
                        if dic[assignment[FOOD_HOUSE_VAR]] == housePos:
                            pr, pb, pn = setpro(PROB_FOOD_RED)
                        elif dic[assignment[GHOST_HOUSE_VAR]] == housePos:
                            pr, pb, pn = setpro(PROB_GHOST_RED)
                        else:
                            pr, pb, pn = setzero()
                        if assignment[obsVar] == RED_OBS_VAL:
                            obsFactor.setProbability(assignment, pr)
                        elif assignment[obsVar] == BLUE_OBS_VAL:
                            obsFactor.setProbability(assignment, pb)
                        else:
                            obsFactor.setProbability(assignment, pn)
                    bayesNet.setCPT(obsVar, obsFactor)

def getMostLikelyFoodHousePosition(evidence, bayesNet, eliminationOrder):
    """
    Question 7: Marginal inference for pacman

    """
    "*** YOUR CODE HERE ***"
    factor = inference.inferenceByVariableElimination(bayesNet, ['foodHouse', 'ghostHouse'], evidence, eliminationOrder)
    pr = -1e100
    d = dict()
    for dic in factor.getAllPossibleAssignmentDicts():
        p = factor.getProbability(dic)
        if p > pr:
            pr = p
            d = dic
    return d
    util.raiseNotDefined()


def joinFactors(factors):
    """
    Question 3: Your join implementation

    """

    "*** YOUR CODE HERE ***"
    '''
    print factor.unconditionedVariables()

    factors are 
    [Factor({'D'}, {'W'}, 
    {'W': ['sun', 'rain'], 'D': ['wet', 'dry']}), 
    Factor({'W'}, set(), {'W': ['sun', 'rain'], 'D': ['wet', 'dry']})]

    for fac in factors:
    fac is P(D | W)  / P(W)
    unc is:  {'D'}   /unc is {'W'}
    con is:  {'W'}   /con is : set()

    factors[0].variableDomainsDict() is
    {'W': ['sun', 'rain'], 'D': ['wet', 'dry']}
    '''
    con = set()
    unc = set()
    # print('facs are: ', factors)
    # print('\n')
    # print('vDD is :', factors.variableDomainsDict())
    for fac in factors:
        # print('fac is: ', fac)
        # print('unc is :', fac.unconditionedVariables())
        # print('con is :', fac.conditionedVariables())
        for unco in fac.unconditionedVariables():
            if unco not in unc:
                unc.add(unco)
        for cond in fac.conditionedVariables():
            # if sth is both in con & unc then we keep it in unc so we delete it in con
            both = unc.union(con)
            if cond not in both:
                con.add(cond)
        inter = con.intersection(unc)
        # for i in con:
        #  if i in :
        for i in inter:
            con.remove(i)

    joinf = Factor(unc, con, factors[0].variableDomainsDict())

    '''
    factors[0].variableDomainsDict() is
    {'W': ['sun', 'rain'], 'D': ['wet', 'dry']}

    joinf.getAllPossibleAssignmentDicts() is 
    [{'W': 'sun', 'D': 'wet'}, {'W': 'sun', 'D': 'dry'}, {'W': 'rain', 'D': 'wet'}, {'W': 'rain', 'D': 'dry'}]
    '''
    # print('get all possible ass is: ', joinf.getAllPossibleAssignmentDicts())
    for joinassign in joinf.getAllPossibleAssignmentDicts():
        joinf.setProbability(joinassign, 1)
    for joinassign in joinf.getAllPossibleAssignmentDicts():
        for fac in factors:
            pro = joinf.getProbability(joinassign) * fac.getProbability(joinassign)
            joinf.setProbability(joinassign, pro)
    return joinf

def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation

        """

        "*** YOUR CODE HERE ***"

        unc = factor.unconditionedVariables()
        unc.remove(eliminationVariable)
        newf = Factor(unc, factor.conditionedVariables(), factor.variableDomainsDict())

        assig = factor.getAllPossibleAssignmentDicts()
        pr = []
        newpr = []
        i = 0
        for value in assig:
            pr.append(factor.getProbability(value))
            newpr.append(newf.getProbability(value))
            prob = pr[i] + newpr[i]
            i = i + 1
            newf.setProbability(value, prob)
        return newf


def normalize(factor):
    """
    Question 5: Your normalize implementation

    """
    "*** YOUR CODE HERE ***"

    newcon = set()
    newunc = set()
    for unc in factor.unconditionedVariables():
        newunc.add(unc)
        # print('unc is: ', unc)
        # print('vdd[unc] is: ', variableDomainsDict[unc])
        if len(variableDomainsDict[unc])== 1:
            if unc not in newcon and unc in newunc:
                newunc.remove(unc)
                newcon.add(unc)
    for con in factor.conditionedVariables():
        newcon.add(con)

    newfactor = Factor(newunc, newcon, factor.variableDomainsDict())
    result = 0
    gotsum = False
    summing = True
    #print('last value is: ', newfactor.getAllPossibleAssignmentDicts()[-1])
    l = 0

    for pr in newfactor.getAllPossibleAssignmentDicts():
        #print('len is', len(newfactor.getAllPossibleAssignmentDicts()))
            ps = factor.getProbability(pr)
            result = result + ps
            #print('res is ', result)
           # if pr == newfactor.getAllPossibleAssignmentDicts()[-1]:
            l = l +1
            if l == len(newfactor.getAllPossibleAssignmentDicts()):
                    # calculate the final result
                    # which is the rightnow probability / sum
                    for pr in newfactor.getAllPossibleAssignmentDicts():
                        pg = factor.getProbability(pr)
                        pg = pg / result
                        newfactor.setProbability(pr, pg)

    return newfactor






def inferenceByVariableElimination(bayesNet, queryVariables, evidenceDict, eliminationOrder):
    """
    Question 6: Your inference by variable elimination implementation"""
    cpts = bayesNet.getAllCPTsWithEvidence(evidenceDict)

    for var in eliminationOrder:
        cpts, joinfac = joinFactorsByVariable(cpts, var)
        '''
        var is : T
        fac is : [Factor({'W'}, set(), {'W': ['sun'], 'D': ['dry', 'wet'], 'T': ['hot', 'cold']}), 
        Factor({'D'}, {'W'}, {'W': ['sun'], 'D': ['dry', 'wet'], 'T': ['hot', 'cold']})]
        joinfac is : P(T | W)

        print('var is :', var)
        print('fac is :',fac)
        print('joinfac is :', joinfac)
        '''
        if len(joinfac.unconditionedVariables()) != 1:
            joinfac = eliminate(joinfac, var)
            cpts.append(joinfac)

    return normalize(joinFactors(cpts))


return inferenceByVariableElimination