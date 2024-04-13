#Specification (G_[0,1] \not final) and (F_[1,2] final)
#This class creates the number of states based on the discretization factor and initializes the transition function of the dfa

import numpy as np
import math as math

class Specification:
    def __init__(self, discretization_factor):
        
        self.discretization_factor = discretization_factor
        self.numstates = self.get_num_states(discretization_factor)
        self.transition_function = None
        self.initial_state = 0
        self.current_state = self.initial_state
        self.fstates, self.nfstates = self.fill_states()
        self.transition_function = self.create_transition_function()
        
        

    def get_num_states(self,discretization_factor):
        if discretization_factor > 2: 
            print("Error, large discretization factor")
        else:
            numstates = math.floor(2/discretization_factor)
            self.deadstate = numstates
            self.acceptstate = numstates+1
            return 

    def reset(self):
        self.current_state = 0

    def get_reward(self, input_symbol):
        current_state = self.current_state
        input_s = input_symbol[0]
        if current_state in transition_function:
            if input_s in transition_function[current_state]:
                state = self.transition_function[self.current_state][input_s]
            else:
                print("error, input symbol is wrong")
        else:
            print("error, states out of bounds")
        
        self.current_state = state

        if state in self.acceptstate:
            return 1
        elif state in self.deadstate:
            return -1
        else:
            return 0




    def fill_states(self):
        nfstates = set(range(self.numstates // 2))
        fstates = set(range(numstates // 2, numstates))
        return fstates, nfstates

    def create_transition_function(self):
        numstates = self.numstates
        transition_function = {}

        for state in range(numstates + 2):
            if state in self.fstates:
                transition_function[state] = {'final': (self.acceptstate) if (state) in fstates else self.deadstate,
                                           'notfinal': (state + 1) if (state + 1) in fstates else self.deadstate}
            elif state in self.nfstates:
                # next_state = (state + 1) if (state + 1) in nfstates else (numstates // 2)
                transition_function[state] = {'final': self.deadstate,
                                           'notfinal': (state + 1)}
            elif state in self.deadstate:
                transition_function[state] = {'final': self.deadstate, 'notfinal': self.deadstate}
            else:
                transition_function[state] = {'final': self.acceptstate, 'notfinal': self.acceptstate}
        return transition_function
           


