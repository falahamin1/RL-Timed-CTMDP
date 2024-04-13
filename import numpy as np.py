import numpy as np
import math as math

class Mdp:
    def __init__(self, num_states, states, available_actions, transition_probs, transition_rates, initial_state):
        self.num_states = num_states
        self.states = states
        self.available_actions = available_actions
        self.transition_probs = transition_probs
        self.transition_rates = transition_rates
        self.initial_state = initial_state
        self.discretization_factor = 1
        self.goal_states = None

    @classmethod
    def input_parameters(cls):
        num_states = int(input("Enter the number of states: "))
        states = list(range(num_states))

        num_actions = int(input("Enter the total number of actions: "))

        available_actions = {}
        for s in states:
            available_actions[s] = [int(x) for x in input(f"Enter available actions for state {s} (space-separated): ").split()]

        transition_rates = np.zeros((num_states, num_actions, num_states))
        for s in states:
            for a in available_actions[s]:
                for s1 in states:
                    next_state_rate = float(input(f"Enter transition ratefor state {s}, action {a}, state {s1}: "))
                    transition_rates[s, a, s1] = next_state_rate

        initial_state = int(input("Enter the initial state: "))
        
        transition_probs = np.zeros_like(transition_rates)
        for s in states:
            for a in available_actions[s]:
                action_sum = np.sum(transition_rates[s, a, :])
                if action_sum > 0:
                    transition_probs[s, a, :] = transition_rates[s, a, :] / action_sum


        return cls(num_states, states, available_actions, transition_probs, transition_rates,  initial_state)
    
    
    def get_transition_rate(self):
        transition_probs = np.zeros_like(self.transition_rates)
        for s in self.states:
            for a in self.available_actions[s]:
                action_sum = np.sum(self.transition_rates[s, a, :])
                if action_sum > 0:
                    transition_probs[s, a, :] = self.transition_rates[s, a, :] / action_sum

        return transition_probs

    def display_mdp(self):
        print("Displaying the CTMDP:")
        print("Number of States:", self.num_states)
        print("States:", self.states)
        print("Available Actions:")
        for s in self.states:
            print(f"  State {s}: {self.available_actions[s]}")
        print("Transition Rates:")
        for s in self.states:
            for a in self.available_actions[s]:
                for s1 in self.states:
                    print(f"  Transition Rate: State {s}, Action {a}, State {s1}: {self.transition_rates[s, a, s1]}")

        print("Transition Probabilities:")
        for s in self.states:
            for a in self.available_actions[s]:
                for s1 in self.states:
                    print(f"  Transition Rate: State {s}, Action {a}, State {s1}: {self.transition_probs[s, a, s1]}")
        print("Initial State:", self.initial_state)

    def reset(self):
        return self.initial_state

    def step(self, state, action):
        exit_rate = np.sum(self.transition_rates[state, action, :])
        time_spent = np.random.exponential(scale= 1/exit_rate)
        next_state_probs = self.transition_probs[state, action, :]
        next_state = np.random.choice(self.num_states, p=next_state_probs)
        return next_state, time_spent

    def discretized_step(self, state, step, action):
        exit_rate = np.sum(self.transition_rates[state, action, :])
        time_spent = np.random.exponential(scale= 1/exit_rate)
        next_state_probs = self.transition_probs[state, action, :]
        next_state = np.random.choice(self.num_states, p=next_state_probs)
        next_step = step + math.ceil(time_spent / self.discretization_factor)
        return next_state, step 

    

# Example usage of the Mdp class with user input
mdp_instance = Mdp.input_parameters()

# Reset the MDP to the initial state
# current_state = mdp_instance.reset()
# print("Initial State:", current_state)

# # Take a random action and transition to the next state
# random_action = np.random.choice(mdp_instance.available_actions[current_state])
# current_state = mdp_instance.step(current_state, random_action)
# print("Next State:", current_state)
mdp_instance.display_mdp()
