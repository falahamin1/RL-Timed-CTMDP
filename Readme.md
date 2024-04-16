# Reinforcement Learning for CTMDPs

This Python script implements a reinforcement learning algorithm designed to optimize decision-making in CTMDPs for MITL specifications. It features a command-line interface to manage various input parameters and is capable of processing different specifications based on user-defined inputs.

## Prerequisites

Ensure you have the following prerequisites installed:
- Python 3.x
- NumPy
- TensorFlow (ensure compatibility with your Python installation)
- Any additional Python packages listed in `requirements.txt`

## Installation

1. **Clone the Repository:**
   
   git clone https://github.com/falahamin1/RL-Timed-CTMDP.git

2. **Running the tool:**

python RL-algorithm.py -s <specfile> -m <mode> [--model <model_path>] [-p <precision>] -f <filename>

## Arguments

This script accepts several command-line options to control its execution:

- `-s, --specfile <path>`: **Required.** Path to the specification file that describes the objectives and parameters for the reinforcement learning process. The specification should be a Python file, such as `Specification1.py`. There are three specifcation classes provided `Specification1.py`, `Specification2.py`, and `Specification3.py`.

- `-m, --mode <mode>`: **Required.** Specifies the mode of operation. Use `all` to run experiments on all predefined models listed in the script, or `single` to run a single experiment with a specific model file.
  - `all`: Runs multiple experiments based on a series of model files.
  - `single`: Runs a single experiment; requires `--model` to be specified.

- `--model <model_path>`: **Conditional.** Required if the `--mode` is set to `single`. Path to the model file that the reinforcement learning algorithm will process. This should be a PRISM model file (`.prism`).

- `-p, --precision <precision>`: Optional. The precision used for discretization in the reinforcement learning computation. Defaults to `0.1` if not specified. This value affects the granularity of the time discretization in CTMDPs.

- `-f, --filename <output_filename>`: **Required.** Name of the file where the results will be written. This file will contain the discretization factors, estimated Q-values, and timing information for each run.

### Example Usage

- **Single Experiment Mode:**

  python RL-algorithm.py -s Specification1.py -m single --model ctmdpModels/toy.prism -p 0.05 -f result.txt

