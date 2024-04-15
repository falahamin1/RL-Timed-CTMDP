#Specification F_[0,5] (intermediate and F_[2,4] final)
#This class creates the number of states based on the discretization factor and initializes the transition function of the dfa

import numpy as np
import math as math

class Specification2:
    def __init__(self, discretization_factor):
        
        self.discretization_factor = discretization_factor
        self.numstates = self.get_num_states(discretization_factor)
        self.transition_function = None
        self.initial_state = (0,'istate')
        self.current_state = self.initial_state
        self.fstates = set()
        self.istates = set()
        self.ifstates = set()
        self.dstate = set()
        self.fill_states()
        # self.transition_function = self.create_transition_function()
        self.time_bound = 9
        

    def get_num_states(self,discretization_factor):
        if discretization_factor > 2: 
            print("Error, large discretization factor")
        else:
            numstates = math.floor(9/discretization_factor)
            self.deadstate = numstates
            self.acceptstate = numstates+1
            return numstates

    def reset(self):
        self.current_state = 0

    def get_reward(self, input_symbol):
        current_state = self.current_state
        input_f = input_symbol[0] #final label
        input_i = input_symbol[1] #intermediate label
        if current_state in self.istates:
            
            if input_i == 'intermediate':
                if current_state[0] == len(self.istates - 1):
                    self.current_state[0] = 0
                    self.current_state[1] = 'fstate'
                    return 0 
                self.current_state[0] += 1
                self.current_state[1] = 'dstate'
                return 0
            else:
                self.current_state[0] += 1
                return 0


        elif current_state in self.dstate:
            
            if current_state[0] == len(self.dstates - 1):
                    self.current_state[0] = 0
                    self.current_state[1] = 'fstate'
                    return 0 
               
            else:
                self.current_state[0] += 1
                return 0

        elif current_state in self.ifstates:
            
            if input_i == 'intermediate' and input_f == 'final':
                return 1
            if input_i == 'intermediate':
                self.current_state[0] += 1
                self.current_state[1] = 'fstate'
                return 0
            elif input_f == 'final':
                self.current_state[0] += 1
                self.current_state[1] = 'dfstate'
                return 0

        elif current_state in self.fstates:
            
            if input_i == 'final':
                return 1
            else:
                self.current_state[0] += 1
                return 0
        
        elif current_state in self.dfstates:
            
            if input_i == 'intermediate':
                return 1
                
            else:
                self.current_state[0] += 1
                return 0
        else:
            return -1





    def fill_states(self):
        istates = (self.numstates*2)//9 #intermediate not seen state
        dstates = (self.numstates*2)//9 #intermediate seen state
        ifstates = self.numstates - istates - 2 #final can be seen state intermediate not seen
        fstates = self.numstates - istates - 2 #final can be seen state intermediate seen
        dfstates = self.numstates - istates - 2 #final seen state intermediate not seen

        self.fstates = set()
        self.istates = set()
        self.ifstates = set()
        self.dstate = set()
        self.dfstates = set()
        for i in range(istates):
            self.istates.add((i,'istate'))
            self.dstate.add((i,'dstate'))
        for i in range(fstates):
            self.ifstates.add((i,'ifstate'))
            self.fstates.add((i,'fstate'))
            self.dfstates.add((i,'dfstate'))
        

    # def create_transition_function(self):
    #     numstates = self.numstates
    #     transition_function = {}

    #     for state in range(numstates + 2):
    #         if state in self.fstates:
    #             transition_function[state] = {'final': (self.acceptstate) if (state) in fstates else self.deadstate,
    #                                        'notfinal': (state + 1) if (state + 1) in fstates else self.deadstate}
    #         elif state in self.nfstates:
    #             # next_state = (state + 1) if (state + 1) in nfstates else (numstates // 2)
    #             transition_function[state] = {'final': self.deadstate,
    #                                        'notfinal': (state + 1)}
    #         elif state in self.deadstate:
    #             transition_function[state] = {'final': self.deadstate, 'notfinal': self.deadstate}
    #         else:
    #             transition_function[state] = {'final': self.acceptstate, 'notfinal': self.acceptstate}
    #     return transition_function
           




