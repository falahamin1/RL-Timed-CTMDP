from Mdp import Mdp
from DeepRL import DQNAgent  
import tensorflow as tf
import numpy as np
import random
from Parser import MDPParser
import time

class AdaptiveRL:
    def __init__(self, time_bound,precision, mdp):
        self.time_bound = time_bound
        self.mdp = mdp
        self.agent = None
        self.precision = precision
        self.max_exit_rate = 0
        self.discretization_factor = 0.1
        self.q_value = 0

    def initialize_mdp(self):
        self.mdp = Mdp.input_parameters()
    
    def get_max_exit_rate(self):
        if self.mdp == None:
            print("Error: MDP not initialized. Call initialize_mdp() first.")
            return
        self.max_exit_rate = self.mdp.get_max_exit_rate()
        print("Max exit rate is:", self.max_exit_rate)
    
    # def get_guaranteed_discretization_factor(self):
    #     discretization_factor = (2* self.precision) / (self.time_bound * self.max_exit_rate * self.max_exit_rate)
    #     self.discretization_factor = discretization_factor
    #     self.mdp.change_discretization_factor(discretization_factor)
    #     print("Guaranteed discretization factor",discretization_factor)

    def train_dqn_agent(self, num_episodes=5000, max_steps_per_episode=100):
        if self.mdp is None:
            print("Error: MDP not initialized. Call initialize_mdp() first.")
            return

        self.agent = DQNAgent(mdp= self.mdp)
        self.agent.train_agent(self.mdp, num_episodes=num_episodes, max_steps_per_episode=max_steps_per_episode)
        max_val, max_actions = self.agent.get_initial_q_value(self.mdp.initial_state, self.mdp.get_available_actions(self.mdp.initial_state))
        print("DQN Agent trained, Initial Q-value is:", max_val)
        print("Initial action by the agentL:", max_actions)
        print("Discretization factor used:", self.discretization_factor)
        return max_val


    def run(self):
        if self.mdp is None:
            print("No MDP provided")
        else:
            self.mdp.display_mdp()
        # if self.max_exit_rate == 0:
        #     self.get_max_exit_rate()
        #     print("Max exit rate is:", self.max_exit_rate)
        # self.get_guaranteed_discretization_factor()

        if self.agent is None:
            q_value = 0
            flag = 0
            while flag == 0:
                self.q_value = q_value
                q_value = self.train_dqn_agent(max_steps_per_episode= int(self.time_bound / self.discretization_factor))
                if(abs( q_value - self.q_value) <= 0.01):
                    flag = 1
                self.discretization_factor = self.discretization_factor/2
            # self.train_dqn_agent()
        

if __name__ == "__main__":
    start_time = time.time()
    time_bound = 1  # Set your desired time bound
    precision = 0.01
    filename = "ctmdpModels/toy.prism"
    parser_instance = MDPParser()
    mdp = parser_instance.run(filename)
    rl_instance = AdaptiveRL(time_bound, precision, mdp)
    rl_instance.run()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time taken for the adaptive algorithm:", elapsed_time)
