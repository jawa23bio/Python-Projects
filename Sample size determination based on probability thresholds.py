#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import matplotlib.pyplot as plt

#Defining class for the simulations
class VeterinaryTrial:
    
    #Defining the initializing varibales
    def __init__(self, pc, pv, alpha):
        self.pc = [1-pc, pc] #Probability of exposure before vaccination
        self.pv = [1-pv, pv] #Probability of exposure after vaccinatiom
        self.alpha = alpha #Significance percent
        self.outcomes = [0, 1] #Possible outcomes, 0 for not getting affected and 1 for getting affected
    
    #Defining the outcomes for N
    def probable_outcomes(self, N):
        control_outcomes = np.random.choice(self.outcomes, size=N, p=self.pc) #Finding probable outcomes of control for the N considered
        control_mean = np.mean(control_outcomes)
        
        treatment_outcomes = np.random.choice(self.outcomes, size=N, p=self.pv) #Finding probable outcomes of treatment for the N considered
        treatment_mean = np.mean(treatment_outcomes)
        
        initial_difference = treatment_mean - control_mean #Mean difference
        
        return control_outcomes, treatment_outcomes, initial_difference

    #Defining function for randomizing the observed outcomes
    def permutation_test(self, control_outcomes, treatment_outcomes, initial_difference):
        num_permutations = 1000
        
        #Combining control and treatment
        combined_outcomes = np.concatenate([control_outcomes, treatment_outcomes])

        final_differences = []

        for i in range(num_permutations):
            np.random.shuffle(combined_outcomes) #Randomizing the combined observed outcomes
            
            permuted_control_outcomes = combined_outcomes[:len(control_outcomes)] #Splitting one set as control outcome
            p_control_mean = np.mean(permuted_control_outcomes)
            
            permuted_treatment_outcomes = combined_outcomes[len(control_outcomes):] #And the rest as treatment outcome
            p_treated_mean = np.mean(permuted_treatment_outcomes)
            
            permuted_difference = p_treated_mean - p_control_mean #Checking for mean difference of the permuted set
            
            final_differences.append(permuted_difference)

        num_greater_or_equal = np.sum(np.abs(final_differences) >= np.abs(initial_difference))
        p_value = num_greater_or_equal / len(final_differences) #Calculating p-value based on mean difference from observed and permuted outcomes
        return p_value

    #Defining function for checking N
    def find_optimal_N(self, confidence_range, max_N=1000):
        N_values = []
        p_values = []

        for N in range(2, max_N + 1): #Maximum values to consider for N
            num_simulations = 1000
            significant_count = 0
        
            #Passing each value of N in the fucntion
            for _ in range(num_simulations):
                control_outcomes, treatment_outcomes, initial_difference = self.probable_outcomes(N)
                p_value = self.permutation_test(control_outcomes, treatment_outcomes, initial_difference)

                if p_value < self.alpha: #Checking if p-value is above the significance level
                    significant_count += 1

            confidence = significant_count / num_simulations

            N_values.append(N)
            p_values.append(confidence)

            if confidence >= confidence_range: #Checking if the observed value is higher than the confidence range
                return N_values, p_values

        return 'No significant N possible at the range provided'

    #Plot for confidence vs N
    def plot_confidence_vs_N(self, confidence_range, max_N=1000):
        result = self.find_optimal_N(confidence_range, max_N)
        if result:
            N_values, p_values = result
            plt.plot(N_values, p_values, label='Confidence vs. Sample Size')
            plt.axhline(y=confidence_range, color='r', linestyle='--', label=f'confidence range({confidence_range})')
            plt.xlabel('Sample Size (N)')
            plt.ylabel('Confidence')
            plt.title('Confidence vs. Sample Size')
            plt.axvline(x=N_values[-1], color='g', linestyle='--', label='Optimal N')
            plt.legend()
            plt.show()
            if p_values[-1] >= confidence_range:
                return N_values[-1], p_values[-1]

pc = 0.5
pv = 0.1
alpha = 0.05
confidence_range = 0.9

simulator = VeterinaryTrial(pc, pv, alpha)
optimal_N, observed_p_value = simulator.plot_confidence_vs_N(confidence_range)

print(f"Optimal N: {optimal_N}")
print(f"Confidence observed: {observed_p_value*100}%")


# In[ ]:




