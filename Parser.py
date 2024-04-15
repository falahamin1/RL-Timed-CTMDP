import numpy as np
from Mdp import Mdp

class MDPParser:
    def __init__(self):
        self.num_states = None
        self.initial_state = None
        self.states = []
        self.available_actions = None
        self.transition_rates = None
        self.final_states = {}
        self.intermediate_states = {}
        self.state_action_counters = {}
        self.transition_list = []
        self.transition_probs = None
        self.exit_rates = None
    
    def parse_file(self, filename):
        with open(filename, 'r') as file:
            # Read the content of the file and extract parameters
            num_states_line = None
            initial_state_line = None

            # Find the lines with information about the number of states and the initial state
            for line in file:
                # print(line.strip())  # Add this line to see each line being processed
                if "s: [" in line:
                    parts = line.strip().split()
                    num_states_line = parts[1].split('0..')[-1].split(']')[0]
                    initial_state_line = parts[3][:-1]
                    break  # Stop searching after finding the line

            # print("num_states_line:", num_states_line)
            # print("initial_state_line:", initial_state_line)

            if num_states_line is None or initial_state_line is None:
                raise ValueError("File does not contain the expected syntax.")

            self.num_states = int(num_states_line)
            self.initial_state = int(initial_state_line)

            # print("Number of States:", self.num_states)
            # print("Initial State:", self.initial_state)
                 # Skip unnecessary lines until you reach the module section
            
            self.final_states = set()
            self.intermediate_states = set()
            for line in file:
                if line.startswith("["):
                    # action_name = f"a{len(self.available_actions)}"
                    parts = line.strip().split()
                    # print("Parts:", parts)
                    state_from = int(parts[1].split('=')[1])
                    # print("State from:", state_from)
                    action_counter = self.state_action_counters.get(state_from, 0)
                    # self.state_action_counters.get(state_from, 0)
                    self.state_action_counters[state_from] = action_counter + 1
                    # Store from_state and next_state in self.states if not already present
                    if state_from not in self.states:
                        self.states.append(state_from)
                    transitions_info = parts[3:]
                    # print("Transition info:", transitions_info)
                    transitions = []
                    for i in range(0, len(transitions_info), 2):
                        # print("Transition info", transitions_info[i].split(':')[0])
                        rate = float(transitions_info[i].split(':')[0])
                        next_state = int(transitions_info[i].split('=')[1].split(')')[0])
                        # print(f'Transition from {state_from} to {next_state} with rate {rate}')
                        if next_state not in self.states:
                            self.states.append(next_state)
                        self.transition_list.append((state_from, action_counter, rate, next_state))
                
                if line.startswith("label"):
                    parts = line.strip().split()
                    # print("Length of parts:", len(parts))
                    # print("Parts:", parts)
                    if parts[1] == "goal":
                        for i in range(2, len(parts)):
                            if parts[i] != "|" and parts[i] !="=":
                                final_state = int(parts[i].split("s=")[1].split(')')[0])
                                self.final_states.add(final_state)
                                
                            
                    
                    elif parts[1] == "intermediate":
                        for i in range(2, len(parts)):
                            if parts[i] != "|" and parts[i] !="=":
                                intermediate_state = int(parts[i].split("s=")[1].split(')')[0])
                                self.intermediate_states.add(intermediate_state)
                    


                    
                        

                    
                
                # if line.startswith("label"):
                #     final_state = int(line.split("s=")[1].split(')')[0])
                #     self.final_states.add(final_state)
                    #todo: need to add provisions to take in multiple final states
                
            file.seek(0)
            num_actions = 0
            for state in self.states:
                num_actions = max(self.state_action_counters.get(state,0), num_actions)
            self.num_actions = num_actions
            self.num_states = len(self.states)

            # print(self.final_states)
            self.decode()
    

    def decode(self):
        transition_rates = np.zeros((self.num_states, self.num_actions, self.num_states))
        available_actions = {state: [] for state in range(self.num_states)}
        for transition in self.transition_list:
            state_from, action_counter, rate, next_state = transition
            transition_rates[state_from, action_counter, next_state] = rate
            if action_counter not in available_actions[state_from]:
                 available_actions[state_from].append(action_counter)


        exit_rates = np.zeros((self.num_states, self.num_actions, 1))
        transition_probs = np.zeros_like(transition_rates)
        for s in self.states:
                for a in available_actions[s]:
                    action_sum = np.sum(transition_rates[s, a, :])
                    if action_sum > 0:
                        exit_rates[s,a,0] = action_sum
                        transition_probs[s, a, :] = transition_rates[s, a, :] / action_sum
                    else:
                        available_actions[s].remove(a)
        self.transition_rates = transition_rates
        self.transition_probs = transition_probs
        self.available_actions = available_actions
        self.exit_rate = exit_rates

    def run(self, filename):
        self.parse_file(filename)
        mdp_instance = Mdp(self.num_states,self.num_actions, self.states, self.available_actions, self.transition_probs,self.transition_rates, self.exit_rates, self.initial_state, self.final_states,self.intermediate_states)
        return mdp_instance
        # mdp_instance.display_mdp()
        # num_states,num_actions, states, available_actions, transition_probs, transition_rates,exit_rates, initial_state, final_states):
        


        


                    
            

    # def parse_second_time(self, filename):
    #     with open(filename, 'r') as file:
    #         transition_rates = np.zeros(self.num_states, self.num_actions, self.num_states)
    #         exit_rates = np.zeros(self.num_states, self.num_actions, 1)
    #         state_action_counter = {}

    #         for line in file:
    #             if line.startswith("["):
    #                 #Parse to get the rates
    #                 parts = line.strip().split()
    #                 print("Parts:", parts)
    #                 state_from = int(parts[1].split('=')[1])
    #                 next_state = int(parts[-1].split('=')[1].split(')')[0])
    #                 rate = float(parts[-2].split(':')[0])
    #                 print("State from:", state_from)
    #                 print("Next state:", next_state)
    #                 print("Rate:", rate)
    #                 action_counter = state_action_counters.get(state_from, 0)
    #                 state_action_counters[state_from] = action_counter + 1

    #                 transition_rates[state_from,action_counter, next_state ] = float(rate)
            
    #         #getting the transition probabilities and exit rates
    #         transition_probs = np.zeros_like(transition_rates)
    #         for s in self.states:
    #             for a in self.available_actions[s]:
    #                 action_sum = np.sum(transition_rates[s, a, :])
    #                 exit_rates[s,a,0] = action_sum
    #                 if action_sum > 0:
    #                     transition_probs[s, a, :] = transition_rates[s, a, :] / action_sum
            
    #         self.transition_rates = transition_rates
    #         self.transition_probs = transition_probs
    #         self.exit_rate = exit_rates



                    


                    # Update available actions
                    # if state_from not in self.available_actions:
                    #     self.available_actions[state_from] = []

                    # self.available_actions[state_from].append(action_name)

                    # # Update transition rates
                    # self.transition_rates[state_from, len(self.available_actions) - 1, next_state] = rate

        


       

        #     # Read the content of the module
        #     num_actions = 0
        #     available_actions = {}
        #     transition_rates = np.zeros((num_states, 1, num_states))
        #     exit_rates = np.zeros((num_states, 1, 1))
        #     final_states = set()

        #     while True:
        #         line = file.readline().strip()
        #         if line.startswith("endmodule"):
        #             break

        #         if line.startswith("["):
        #             num_actions += 1
        #             action_name = f"a{num_actions}"

        #             # Parse state and transition rate
        #             state_from = int(line.split("s=")[1].split()[0])
        #             transition_rate = float(line.split("->")[1].split(":")[0])

        #             if state_from not in available_actions:
        #                 available_actions[state_from] = []

        #             available_actions[state_from].append(num_actions - 1)

        #             # Populate the transition matrix
        #             transition_rates[state_from, 0, :] = transition_rate

        #     # Read the final states
        #     while True:
        #         line = file.readline().strip()
        #         if line.startswith("label"):
        #             final_state = int(line.split("s=")[1].split(')')[0])
        #             final_states.add(final_state)

        # # Create and return an instance of the Mdp class
        # return Mdp(num_states, num_actions, list(range(num_states)), available_actions, transition_rates, transition_rates, exit_rates,
        #            initial_state, list(final_states))

def display_mdp_info(filename):
    mdp_instance = MDPParser()
    mdp_instance.run(filename)

    # Display MDP information
    # print("Number of States:", mdp_instance.num_states)
    # print("Initial State:", mdp_instance.initial_state)
    # print("Available Actions:")
    # for state, actions in mdp_instance.available_actions.items():
    #     print(f"  State {state}: {actions}")
    
    # print("Transition Rates:")
    # for state in range(mdp_instance.num_states):
    #     print(f"  State {state}: {mdp_instance.transition_rates[state, 0, :]}")

    # print("Final States:", mdp_instance.final_states)


filename = "ctmdpModels/toy.prism"  # Replace with the actual file name
display_mdp_info(filename)