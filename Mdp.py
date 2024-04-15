import numpy as np
import math as math


class Mdp:
    def __init__(self, num_states,num_actions, states, available_actions, transition_probs, transition_rates,exit_rates, initial_state, final_states,intermediate_states):
        self.num_states = num_states
        self.states = states
        self.available_actions = available_actions
        self.transition_probs = transition_probs
        self.transition_rates = transition_rates
        self.initial_state = initial_state
        self.initial_step = 0
        self.discretization_factor = 1
        self.final_states = final_states
        self.intermediate_states = intermediate_states
        self.num_actions = num_actions
        self.exit_rates = exit_rates
        self.Specification = None
    
    def get_transition_rate(self):
        transition_probs = np.zeros_like(self.transition_rates)
        for s in self.states:
            for a in self.available_actions[s]:
                action_sum = np.sum(self.transition_rates[s, a, :])
                if action_sum > 0:
                    transition_probs[s, a, :] = self.transition_rates[s, a, :] / action_sum

        return transition_probs

    def display_mdp(self):
        print("Initial State:", self.initial_state)
        print("Final State:", self.final_states)
        print("Intermediate State:",self.intermediate_states)

    def reset(self):
        self.Specification.reset()
        return self.initial_state, self.initial_step

    def step(self, state, action):
        exit_rate = np.sum(self.transition_rates[state, action, :])
        time_spent = np.random.exponential(scale= 1/exit_rate)
        next_state_probs = self.transition_probs[state, action, :]
        next_state = np.random.choice(self.num_states, p=next_state_probs)
        return next_state, time_spent

    def discretized_step(self, state, step, action):
        exit_rate = np.sum(self.transition_rates[state, action, :])
        # print("Exit rate is", exit_rate)
        if action in self.available_actions[state]:
            time_spent = np.random.exponential(scale= 1/exit_rate)
            # print("Time spent:", time_spent)
            next_state_probs = self.transition_probs[state, action, :]
            next_state = np.random.choice(len(next_state_probs), p=next_state_probs)
            # print("state chosen:",next_state)
            next_step = step + math.ceil(time_spent / self.discretization_factor)
            reward = 0
            current_label = ['notfinal', 'notintermediate']
            next_label = ['notfinal', 'notintermediate']
            if state in self.final_states:
                current_label[0] = 'final'
            if next_state in self.final_states:
                next_label[0] = 'final'
            if state in self.intermediate_states:
                current_label[1] = 'intermediate'
            if next_state in self.intermediate_states:
                next_label[1] = 'intermediate'
            reward = 0
            # print(f"Current label in mdp: {current_label}, next label: {next_label}")

            for i in range(step,next_step):
                reward = self.Specification.get_reward(current_label)
                if reward == -1: 
                    break
                elif reward == 1: 
                    break 
            reward = self.Specification.get_reward(next_label)
        else:
            print("Error, action not in available actions")
        return next_state, next_step, reward

    def get_available_actions(self,state):
        return self.available_actions[state]
    
    def change_discretization_factor(self, discretization_factor,Specification):
        self.discretization_factor = discretization_factor
        self.Specification = Specification(discretization_factor)
    def get_max_exit_rate(self):
        max_exit_rate = 0
        for s in self.states:
            for a in self.available_actions[s]:
                action_sum = np.sum(self.transition_rates[s, a, :])
                max_exit_rate = max(max_exit_rate, action_sum)
        return max_exit_rate
        
    def get_specification(self, specification):
        self.Specification = specification


#Todo: For the step function, add something when there are no actions available

    

# Example usage of the Mdp class with user input
# mdp_instance = Mdp.input_parameters()

# Reset the MDP to the initial state
# current_state = mdp_instance.reset()
# print("Initial State:", current_state)

# # Take a random action and transition to the next state
# random_action = np.random.choice(mdp_instance.available_actions[current_state])
# current_state = mdp_instance.step(current_state, random_action)
# print("Next State:", current_state)
# mdp_instance.display_mdp()
