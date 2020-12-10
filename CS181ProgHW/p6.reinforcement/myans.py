
###q111111111
ans = 0
        if action!= 0 :
            for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                reward = self.mdp.getReward(state,action, nextstate)
                disc = self.discount * self.values[nextstate]
                ans = prob * (reward +disc)
        else:
            return 0
        return ans




possibleaction = self.mdp.getPossibleActions(state)
ans = None
maxi = -1e10
if self.mdp.isTerminal(state) is None or len(possibleaction) == 0:
    return None
for act in possibleaction:
    q = self.computeQValueFromValues(state, act)
    if q > maxi:
        maxi = q
        ans = act
return ans
