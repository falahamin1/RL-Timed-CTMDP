from Mdp import Mdp
from DeepRL import DQNAgent  
from guaranteed_RL import GuaranteedRL
import tensorflow as tf
import numpy as np
import random
from Parser import MDPParser
import time
import argparse


class RL:
    def __init__(self):
        
        self.args = self.setup_parser()
        self.time_bound = 2

    def setup_parser(self):
        parser = argparse.ArgumentParser(description='Run the Guaranteed RL with given specifications.')
        parser.add_argument('-s', '--specfile', type=str, required=True, help='Path to the specification file')
        parser.add_argument('-m', '--mode', type=str, choices=['all', 'single'], required=True, help='Mode type: "all" or "single"')
        parser.add_argument('--model', type=str, help='Path to the model file (required if mode is "single")')
        parser.add_argument('-p', '--precision', type=float,default=0.1 , required=False, help='Precision (default value 0.1)')
        parser.add_argument('-f', '--filename', type=str, required=True, help='Name of the file to which results are written')
        
        args = parser.parse_args()

        if args.mode == 'single' and not args.model:
            parser.error('The --model argument is required when mode is "single".')

        self.precision = args.precision

        return args
    
    # def get_max_exit_rate(self):
    #     if self.mdp == None:
    #         print("Error: MDP not initialized. Call initialize_mdp() first.")
    #         return
    #     self.max_exit_rate = self.mdp.get_max_exit_rate()
        # print("Max exit rate is:", self.max_exit_rate)
    
    def get_guaranteed_discretization_factor(self):
        discretization_factor = (2* self.precision) / (self.time_bound * self.max_exit_rate * self.max_exit_rate)
        return discretization_factor


    def run(self):
        if self.args.mode == 'all':
            self.run_all_experiments()
        else:
             with open(self.args.filename, "w") as file: 
                start_time = time.time()   
                parser_instance = MDPParser()
                mdp = parser_instance.run(self.args.model)
                self.max_exit_rate = mdp.get_max_exit_rate()
                mdp.change_discretization_factor(self.get_guaranteed_discretization_factor())
                mdp.get_specification(self.args.specification)
                rl_instance = GuaranteedRL(self.time_bound, self.args.precision, mdp, self.max_exit_rate)
                q_val = rl_instance.run()
                file.write(f"discretization factor: {rl_instance.discretization_factor}\n")
                file.write(f"Estimated Q-value: {q_val}\n")
                end_time = time.time()
                elapsed_time = end_time - start_time
                file.write(f"Time taken for the guaranteed algorithm: {elapsed_time}\n")


   
        

    def run_all_experiments(self):
        time_bound = 2  # Set your desired time bound
        precision = 0.01
        filenames = [
        "ctmdpModels/toy.prism",
        "ctmdpModels/DynamicPM-tt_3_qs_2_sctmdp.prism",
        "ctmdpModels/ErlangStages-k500_r10.prism",
        "ctmdpModels/DynamicPM-tt_3_qs_6_sctmdp.prism",
        "ctmdpModels/ErlangStages-k2000_r10.prism",
        "ctmdpModels/ftwc_001_mrmc.prism",
        "ctmdpModels/PollingSystem-jt1_qs1_sctmdp.prism",
        "ctmdpModels/PollingSystem-jt1_qs4_sctmdp.prism",
        "ctmdpModels/PollingSystem-jt1_qs7_sctmdp.prism",
        "ctmdpModels/QueuingSystem-lqs_1_rqs_1_jt_2_sctmdp.prism",
        "ctmdpModels/QueuingSystem-lqs_2_rqs_2_jt_3_sctmdp.prism",
        "ctmdpModels/SJS-procn_2_jobn_2_sctmdp.prism",
        "ctmdpModels/SJS-procn_2_jobn_6_sctmdp.prism"
    ]

        with open(self.args.filename, "w") as file:
            for filename in filenames:
                file.write(f'##################### Guaranteed RL looking into {filename} ##############################\n')
                qvalues = 0
                start_time = time.time()
                for i in range(3):
                    parser_instance = MDPParser()
                    mdp = parser_instance.run(filename)
                    self.max_exit_rate = mdp.get_max_exit_rate()
                    mdp.change_discretization_factor(self.get_guaranteed_discretization_factor())
                    rl_instance = GuaranteedRL(self.time_bound, self.args.precision, mdp, self.max_exit_rate)
                    q_val = rl_instance.run()
                    qvalues += q_val
                    file.write(f"discretization factor: {rl_instance.discretization_factor}\n")

                end_time = time.time()
                elapsed_time = end_time - start_time
                file.write(f"Average q-value: {qvalues/3}\n")
                file.write(f"Time taken for the guaranteed algorithm: {elapsed_time/3}\n")

if __name__ == "__main__":
    app = RL()
    app.run()


    # filename = "ctmdpModels/toy.prism"
    # parser_instance = MDPParser()
    # mdp = parser_instance.run(filename)
    # rl_instance = GuaranteedRL(time_bound, precision, mdp)
    # rl_instance.run()
    # end_time = time.time()
    # elapsed_time =  end_time - start_time
    # print("Time taken for the guaranteed algorithm:", elapsed_time)
