# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from functools import reduce
from bayesNet import Factor
import operator as op
import util

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print ("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError ("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    factors = list(factors)
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print ("Factor failed joinFactors typecheck: ", factor)
            raise ValueError ("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


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
    #print('vDD is :', factors.variableDomainsDict())
    for fac in factors:
        # print('fac is: ', fac)
        # print('unc is :', fac.unconditionedVariables())
        # print('con is :', fac.conditionedVariables())
        for unco in fac.unconditionedVariables():
            if  unco not in unc:
                unc.add(unco)
        for cond in fac.conditionedVariables():
            #if sth is both in con & unc then we keep it in unc so we delete it in con
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
    #print('get all possible ass is: ', joinf.getAllPossibleAssignmentDicts())
    for joinassign in joinf.getAllPossibleAssignmentDicts():
        joinf.setProbability(joinassign, 1)
    for joinassign in joinf.getAllPossibleAssignmentDicts():
        for fac in factors:
            pro = joinf.getProbability(joinassign) * fac.getProbability(joinassign)
            joinf.setProbability(joinassign, pro)
    return joinf



def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print ("Factor failed eliminate typecheck: ", factor)
            raise ValueError ("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print ("Factor failed eliminate typecheck: ", factor)
            raise ValueError ("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

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
    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain.  Since there is only one entry in that variable's domain, we 
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables 
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print ("Factor failed normalize typecheck: ", factor)
            raise ValueError ("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"
    '''
    domains = factor.variableDomainsDict()
    con = factor.conditionedVariables()
    unc = factor.unconditionedVariables()
  
     print('domains are: ', domains)
    print('cons are: ', con)
    print('uncons are: ', unc)
    
    domains are:  {'W': ['sun', 'storm', 'rain']}
    cons are:  set()
    uncons are:  {'W'}
    '''

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
