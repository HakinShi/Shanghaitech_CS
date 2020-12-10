###q111111111
AftertakeAction = []
if action == None:
    return 0
else:
    for nextstate, transprob in self.mdp.getTransitionStatesAndProbs(state, action):
        AftertakeAction.append(
            transprob * (self.mdp.getReward(state, action, nextstate) + self.discount * self.values[nextstate]))
return sum(AftertakeAction)




legal_actions = self.mdp.getPossibleActions(state)
        if len(legal_actions) == 0:
            return None
        max = -9999
        best_action = None
        for action in legal_actions:
            value = self.computeQValueFromValues(state, action)
            if value > max:
                max = value
                best_action = action
        return best_action






nextvalue=util.Counter()
        for iteration in range(self.iterations):
            for state in self.mdp.getStates():
                action=self.computeActionFromValues(state)
                nextvalue[state]=self.computeQValueFromValues(state,action)
            self.values=nextvalue.copy()

