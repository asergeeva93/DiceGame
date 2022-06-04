from abc import ABC, abstractmethod
from dice_game import DiceGame
import numpy as np


class DiceGameAgent(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def play(self, state):
        pass


class AlwaysHoldAgent(DiceGameAgent):
    def play(self, state):
        return (0, 1, 2)


class PerfectionistAgent(DiceGameAgent):
    def play(self, state):
        if state == (1, 1, 1) or state == (1, 1, 6):
            return (0, 1, 2)
        else:
            return ()
        
        
def play_game_with_agent(agent, game, verbose=False):
    state = game.reset()
    
    if(verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if(verbose): print(f"Starting dice: \n\t{state}\n")
    
    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1
        
        if(verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if(verbose and not game_over): print(f"Dice: \t\t{state}")

    if(verbose): print(f"\nFinal dice: {state}, score: {game.score}")
        
    return game.score

class MyAgent(DiceGameAgent):
    def __init__(self, game):

         
        """
        if your code does any pre-processing on the game, you can do it here
        
        e.g. you could do the value iteration algorithm here once, store the policy, 
        and then use it in the play method
        
        you can always access the game with self.game
        """
        # this calls the superclass constructor (does self.game = game)
        super().__init__(game) 
        
        
    def play(self, state):

        high_triple(state)
        low_triple(state)
        high_double(state)
        low_double(state)

        current_reward = score_calc(state)
        print(score_calc(state))

        game = DiceGame()
        penalty = game._penalty
        print(drop_one(state)[0], "Drop one")
        print(drop_three(state)[0], "drop three")
        drop_two(state)

        if drop_one(state)[0]  > drop_three(state)[0]:       
            move = drop_one(state)
            expected_reward = move[0]

        else:
            move = drop_three(state)
            expected_reward = move[0]
      
        if float(expected_reward) < float(current_reward) + penalty:
            return (0,1,2)
        else:
            return(move[1:])
      
        """
        given a state, return the chosen action for this state
        at minimum you must support the basic rules: three six-sided fair dice
        
        if you want to support more rules, use the values inside self.game, e.g.
            the input state will be one of self.game.states
            you must return one of self.game.actions
        
        read the code in dicegame.py to learn more
        """
        return (0, 1, 2)

#high triple = unwanted as it will lead to a low score
def high_triple(state):
    for num, i in enumerate(state):
        if (state[num] == state[num+1] == state[num+2]) and (i == 4 or i ==5 or i ==6):
            return True
        else:
            return False

def low_triple(state):
    for num, i in enumerate(state):
        if (state[num] == state[num+1] == state[num+2]) and (i == 1 or i ==2 or i ==3):
            return True
        else:
            return False

def high_double(state):
    for num, i in enumerate(state):
        if (state[0] == state[1] or state[1] == state[2]) and (state[1] == 4 or state[1] ==5 or state[1] ==6):
            return True
        else:
            return False

def low_double(state):
    for num, i in enumerate(state):
        if (state[0] == state[1] or state[1] == state[2]) and (state[1] == 1 or state[1] ==2 or state[1] ==3):
            return True
        else: 
            return False

def score_calc(state):
    if low_triple(state) or high_triple(state):
        current_reward = 7 - state[0] * 3
    elif low_double(state) or high_double(state):
        if state[0] == state[1]:
            current_reward = (7 - state[1])*2 + state[2]
        else:
            current_reward = (7 - state[1])*2 + state[0]
    else:
        current_reward = 0
        for i in state:
            current_reward = current_reward + i 
    return current_reward

def roll_one(state):
    l = list()
    for i in range(0,3):
        expected_reward = 0
        for j in range(1,7):
            new_state = list(state)
            new_state[i] = j
            expected_reward = expected_reward + (1/6 * score_calc(new_state))
        l.append(expected_reward)
    print(l)
    if l[0] > l[1] and l[0] > l[2]:
      return(float(l[0]),1,2)
    elif l[1] > l[2] and l[1] > l[0]:
      return(float(l[1]),0,2)
    elif l[2] > l[1] and l[2] > l[0]:
      return(float(l[2]),0,1)
    else:
      return (float(l[0]),1,2)

def drop_one(state):
    rewards = list()
    for i in range(0,3):
        expected_reward = 0
        for j in range(1,7):
            new_state = list(state)
            new_state[i] = j
            expected_reward = expected_reward + (1/6 * score_calc(new_state))
        rewards.append(expected_reward)
    max_reward = max(rewards)
    outcome = list(state)
    outcome.pop(rewards.index(max_reward))
    return (float(max_reward),1,2)

def drop_two(state):
  rewards = list()
  for num1,i in enumerate(state):
    for num2,j in enumerate(state):
     if not i == j:
       print (num1, num2)
       expected_reward = 0
       for k in range(1,7):  
         for n in range(1,7):
            new_state = list(state)
            new_state[num1] = k
            new_state[num2] = n
            expected_reward = expected_reward + (1/12 * score_calc(new_state))
    rewards.append(expected_reward)
  max_reward = max(rewards)
  outcome = list(state)
  outcome.pop(rewards.index(max_reward))
  return (float(max_reward),1,2)
      
def drop_three(state):
    expected_reward = 0
    for i in range(0,3):
        for j in range(1,7):
            new_state = list(state)
            new_state[i] = j
            expected_reward = expected_reward + (1/18 * score_calc(new_state))
    return (expected_reward,())
  
def main():
    # random seed makes the results deterministic
    # change the number to see different results
    # or delete the line to make it change each time it is run
    #np.random.seed(1)
    
    game = DiceGame()
    
    agent1 = MyAgent(game)
    play_game_with_agent(agent1, game, verbose=True)




if __name__ == "__main__":
    main()