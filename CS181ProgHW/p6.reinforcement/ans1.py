###q111111111
value = 0
        for next_state, p in self.mdp.getTransitionStatesAndProbs(state, action):
            r = self.mdp.getReward(state, action, next_state)
            value = value + p*(r + self.discount*self.values[next_state])
        return value

if self.mdp.isTerminal(state):
    return None
else:
    allQvalueAndAction = []
    allQvalue = []
    for action in self.mdp.getPossibleActions(state):
        qvalue = self.computeQValueFromValues(state, action)
        allQvalue.append(qvalue)
        allQvalueAndAction.append((action, qvalue))
    for action, Qvalue in allQvalueAndAction:
        if Qvalue == max(allQvalue):
            return action


cnt = 0
        while cnt < self.iterations:
            new = util.Counter()
            for state in self.mdp.getStates():
                q_values = util.Counter()

                if len(self.mdp.getPossibleActions(state)) == 0:
                    new[state] = 0
                    continue

                for action in self.mdp.getPossibleActions(state):
                    q_values[action] = self.computeQValueFromValues(state, action)
                my_max = -9999
                for i in q_values:
                    if q_values[i] > my_max:
                        my_max = q_values[i]
                new[state] = my_max

            cnt = cnt + 1
            self.values = new

