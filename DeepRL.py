from Mdp import Mdp
import numpy as np
import tensorflow as tf
import random
from tensorflow.keras import layers, models

class QNetwork(tf.keras.Model):
    def __init__(self, num_actions):
        super(QNetwork, self).__init__()
        self.model = models.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(num_actions, activation='sigmoid')  # No activation for Q-values
        ])

    def call(self, state):
        # Combine state and step before passing through the network
        return self.model(state)

class DQNAgent:
    def __init__(self, mdp, learning_rate=0.01, discount_factor=1, epsilon=1.0, epsilon_decay=0.995):
        self.q_network = QNetwork(mdp.num_actions)
        self.target_q_network = QNetwork(mdp.num_actions)
        self.optimizer = tf.keras.optimizers.legacy.Adam(learning_rate)
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def epsilon_greedy_policy(self, state, step, available_actions):
        if np.random.rand() < self.epsilon:
            return np.random.choice(available_actions)
        else:
            # print("Call to q_network")
            input_tensor = tf.constant([[state, step]], dtype=tf.float32)  
            q_values = self.q_network(input_tensor)
            # print("Q-values for the state are:", q_values)
            available_q_values = tf.gather(q_values, available_actions, axis=1)
            # print("Available q values:", available_q_values)
            max_q_index = tf.argmax(available_q_values, axis= 1).numpy()[0]
            # print("The index with max-q value:", max_q_index)
            max_action = available_actions[max_q_index]
            # print("The best action:", max_action)
            return max_action


    def train(self, states, steps, actions, rewards, next_states, next_steps, available_actions):
        with tf.GradientTape() as tape:
            batch_size = len(states) 
            #converting the batch to np arrays
            states = np.array(states) 
            steps = np.array(steps) 
            next_states = np.array(next_states) 
            next_steps = np.array(next_steps) 
            actions = np.array(actions)
            rewards = np.array(rewards)
            actions = np.expand_dims(actions, axis=1)
            #making the available actions list homegenous and converting it to an np array
            max_length = max(len(sublist) for sublist in available_actions)
            homogeneous_list = [sublist + [sublist[0]] * (max_length - len(sublist)) for sublist in available_actions]
            available_actions = homogeneous_list
            available_actions = np.array(available_actions)
            rewards_tf = tf.constant(rewards, dtype=tf.float32)
            states = np.expand_dims(states, axis=1)
            next_states = np.expand_dims(next_states, axis=1)
            steps = np.expand_dims(steps, axis=1)
            next_steps = np.expand_dims(next_steps, axis=1)
            #Combining the state and step to keep it single
            states_with_steps = np.hstack((states,steps))
            next_states_with_steps = np.hstack((next_states,next_steps))
            #Converting to tensors
            tensor_states = tf.constant(states_with_steps)
            tensor_next_states = tf.constant(next_states_with_steps)
            main_q_values = self.q_network(tensor_states)
            main_q_values = tf.gather(main_q_values, actions, axis= 1, batch_dims=1)
            main_q_values = tf.reduce_max(main_q_values,axis=1)
            target_q_values = self.target_q_network(tensor_next_states)
            target_q_values = tf.gather(target_q_values, available_actions, axis= 1, batch_dims=1)
            target_q_values = tf.reduce_max(target_q_values,axis=1)
            targets = rewards_tf + target_q_values
            loss = tf.reduce_mean(tf.square(targets - main_q_values))
        gradients = tape.gradient(loss, self.q_network.trainable_variables)    
        self.optimizer.apply_gradients(zip(gradients, self.q_network.trainable_variables))

    def update_target_network(self):
        learning_rate = 0.25
        main_q_weights = self.q_network.get_weights()
        target_q_weights = self.target_q_network.get_weights()
        new_target_q_weights = [
        (1.0 - learning_rate) * target_weight + learning_rate * main_weight
        for target_weight, main_weight in zip(target_q_weights, main_q_weights)
        ]

        self.target_q_network.set_weights(new_target_q_weights)

    def train_agent(self, mdp, num_episodes=5000, max_steps_per_episode=100, replay_buffer_size=10, batch_size= 50 ):
        self.q_network(tf.constant([[0,0]], dtype=tf.float32) )#Initializing the networks
        self.target_q_network(tf.constant([[0,0]], dtype=tf.float32) )
        for episode in range(num_episodes):
            state, step = mdp.reset()
            total_reward = 0
            replay_buffer = []  # Initialize replay buffer

            while step <= max_steps_per_episode:
                action = self.epsilon_greedy_policy(state, step, mdp.get_available_actions(state))
                next_state, next_step, reward = mdp.discretized_step(state, step, action)

                if reward > 0:
                    if next_step <= max_steps_per_episode - 1:
                        reward = 1
                if next_step > max_steps_per_episode - 1:
                    reward = -1

                # Store experience in replay buffer
                # print("The experience:",(state, step, action, reward, next_state, next_step, mdp.get_available_actions(next_state)))
                replay_buffer.append((state, step, action, reward, next_state, next_step, mdp.get_available_actions(next_state)))


                #If episode ends before replay buffer is filled, we train the model on the gained knowledge

                if reward > 0 or next_step > max_steps_per_episode - 1:
                    states, steps, actions, rewards, next_states, next_steps, available_actions = zip(*replay_buffer)
                    self.train(states, steps, actions, rewards, next_states, next_steps, available_actions )
                    break

                # Sample a random batch from the replay buffer
                if len(replay_buffer) >= batch_size:
                    batch = random.sample(replay_buffer, batch_size)
                    states, steps, actions, rewards, next_states, next_steps, available_actions = zip(*batch)
                    self.train(states, steps, actions, rewards, next_states, next_steps, available_actions )

                total_reward += reward

                state = next_state
                step = next_step


            self.epsilon *= self.epsilon_decay
            self.update_target_network()
            # print(f"Episode: {episode + 1}, Total Reward: {total_reward}")



    def get_initial_q_value(self, initial_state, available_actions):
        input_tensor = tf.constant([[initial_state, 0]], dtype=tf.float32)  
        q_values = self.q_network(input_tensor)
        available_q_values = tf.gather(q_values, available_actions, axis=1)
        max_q_value = tf.reduce_max(available_q_values)
        max_q_index = tf.argmax(available_q_values, axis= 1).numpy()[0]
        max_action = available_actions[max_q_index]
        return max_q_value.numpy().item(), max_action
        

        
   