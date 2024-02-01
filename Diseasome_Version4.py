#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd

def parse_hpoa_file(file_path):
    # Specify the columns you want to keep
    columns_to_keep = ["database_id", "disease_name", "hpo_id"]

    # Read the HPOA file into a Pandas DataFrame with selected columns
    hpo_df = pd.read_csv(file_path, sep='\t', comment='#', header=0, usecols=columns_to_keep)

    return hpo_df

# Example usage
file_path = "phenotype (3).hpoa"
hpo_data = parse_hpoa_file(file_path)

# Now you can work with the parsed data in the DataFrame
hpo_data


# In[13]:


hpo_data.to_csv('Data.csv', index=False)


# In[11]:


# Finding the number of unique diseases in this dataset
unique_diseases = hpo_data['disease_name'].unique()
total_unique_diseases = len(unique_diseases)
print("\nTotal Unique diseases:", total_unique_diseases)

#Finding the number of unique phenotypes
unique_phenotypes = hpo_data['hpo_id'].unique()
total_unique_phenotypes = len(unique_phenotypes)
print("\nTotal Unique Phenotypes:", total_unique_phenotypes)


# In[15]:


grouped = hpo_data.groupby(['database_id', 'disease_name'])['hpo_id'].apply(list).reset_index()
grouped


# In[16]:


grouped['Number of Phenotypes'] = grouped['hpo_id'].apply(len)
grouped


# In[20]:


grouped.to_csv('DP-Map_HPO.csv', index=False)


# In[1]:


import pandas as pd
from itertools import combinations

# Create an empty list to store common phenotypes information
common_phenotypes_data = []

# Get unique disease names
unique_diseases = grouped['disease_name'].unique()

# Iterate through combinations of diseases
for disease_combination in combinations(unique_diseases, 2):
    disease_1, disease_2 = disease_combination
    
    # Extract HPO associations for each disease
    hpo_list_1 = grouped[grouped['disease_name'] == disease_1]['hpo_id'].iloc[0]
    hpo_list_2 = grouped[grouped['disease_name'] == disease_2]['hpo_id'].iloc[0]
    
    # Find common phenotypes using list comprehension
    common_phenotypes = [phenotype for phenotype in hpo_list_1 if phenotype in hpo_list_2]
    
    num_phenotypes_1 = len(hpo_list_1)
    num_phenotypes_2 = len(hpo_list_2)
    num_common_phenotypes = len(common_phenotypes)
    
    # Append data to the list
    common_phenotypes_data.append({
        'Disease 1': disease_1,
        'Disease 2': disease_2,
        'Disease 1 Phenotypes': num_phenotypes_1,
        'Disease 2 Phenotypes': num_phenotypes_2,
        'Common Phenotypes': common_phenotypes,
        'Number of Common Phenotypes': num_common_phenotypes
    })

# Create a DataFrame from the list
common_phenotypes_df = pd.DataFrame(common_phenotypes_data)
common_phenotypes_df


# In[ ]:




