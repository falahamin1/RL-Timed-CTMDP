from Mdp import Mdp
from DeepRL import DQNAgent  
import tensorflow as tf
import numpy as np
import random
from Parser import MDPParser
import time
import argparse

class GuaranteedRL:
    def __init__(self, time_bound, precision,  mdp, exit_rate):
        self.time_bound = time_bound
        self.mdp = mdp
        self.agent = None
        self.precision = precision
        self.max_exit_rate = exit_rate
        self.discretization_factor = 0
    
    def get_guaranteed_discretization_factor(self):
        discretization_factor = (2* self.precision) / (self.time_bound * self.max_exit_rate * self.max_exit_rate)
        self.discretization_factor = discretization_factor
        self.mdp.change_discretization_factor(discretization_factor)
        # print("Guaranteed discretization factor",discretization_factor)

    def train_dqn_agent(self, num_episodes=1000, max_steps_per_episode=100):
        self.agent = DQNAgent(mdp= self.mdp)
        self.agent.train_agent(self.mdp, num_episodes=num_episodes, max_steps_per_episode=max_steps_per_episode)
        max_val, max_actions = self.agent.get_initial_q_value(self.mdp.initial_state, self.mdp.get_available_actions(self.mdp.initial_state))
        return max_val
        

    def run(self):
        self.get_guaranteed_discretization_factor()

        if self.agent is None:
            max_val = self.train_dqn_agent(max_steps_per_episode= int(self.time_bound / self.discretization_factor))
            return max_val

