#!/usr/bin/env python
# coding: utf-8

# In[2]:


import xml.etree.ElementTree as ET
import pandas as pd

# Replace 'path/to/your/file.xml' with the actual path to your XML file
file_path = 'en_product4.xml'

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Create lists to store data
orphacodes = []
diseases = []
hpo_ids = []
hpo_terms = []

# Iterate through each Disorder element
for disorder_element in root.findall('.//Disorder'):
    # Extract OrphaCode, Disease Name
    orpha_code = disorder_element.find('OrphaCode').text
    disease_name = disorder_element.find('Name').text
    
    # Iterate through each HPODisorderAssociation element
    for hpo_association in disorder_element.findall('.//HPODisorderAssociation'):
        # Extract HPOId and HPOTerm
        hpo_id = hpo_association.find('.//HPO/HPOId').text
        hpo_term = hpo_association.find('.//HPO/HPOTerm').text

        # Append data to the lists
        orphacodes.append(orpha_code)
        diseases.append(disease_name)
        hpo_ids.append(hpo_id)
        hpo_terms.append(hpo_term)

# Create a DataFrame
df = pd.DataFrame({'OrphaCode': orphacodes, 'DiseaseName': diseases, 'HPOId': hpo_ids, 'HPOTerm': hpo_terms})
df


# In[3]:


# Finding the number of unique diseases in this dataset
unique_diseases = df['DiseaseName'].unique()
total_unique_diseases = len(unique_diseases)
print("\nTotal Unique diseases:", total_unique_diseases)

#Finding the number of unique phenotypes
unique_phenotypes = df['HPOTerm'].unique()
total_unique_phenotypes = len(unique_phenotypes)
print("\nTotal Unique Phenotypes:", total_unique_phenotypes)


# In[4]:


grouped = df.groupby(['OrphaCode', 'DiseaseName'])['HPOTerm'].apply(list).reset_index()
grouped


# In[5]:


grouped['Number of Phenotypes'] = grouped['HPOTerm'].apply(len)
grouped


# In[5]:


grouped.to_csv('All-Disease-Phenotype-Map::Orphanet.csv', index=False)


# In[6]:


import pandas as pd
from itertools import combinations

# Create an empty list to store common phenotypes information
common_phenotypes_data = []

# Get unique disease names
unique_diseases = grouped['DiseaseName'].unique()

# Iterate through combinations of diseases
for disease_combination in combinations(unique_diseases, 2):
    disease_1, disease_2 = disease_combination
    
    # Extract HPO associations for each disease
    hpo_list_1 = grouped[grouped['DiseaseName'] == disease_1]['HPOTerm'].iloc[0]
    hpo_list_2 = grouped[grouped['DiseaseName'] == disease_2]['HPOTerm'].iloc[0]
    
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


# In[11]:


common_phenotypes_df.to_csv('Common_Phenotypes-ALL.csv', index=False)


# In[12]:


print(common_phenotypes_df.columns)


# In[13]:


from scipy.stats import hypergeom

# Create a list to store p-values
p_values = []

# Iterate through each row in the DataFrame
for index, row in common_phenotypes_df.iterrows():
    # Define parameters for hypergeometric distribution
    N = total_unique_phenotypes  # Total number of unique phenotypes
    K = row['Number of Common Phenotypes']  # Total number of common phenotypes
    n1 = row['Disease 1 Phenotypes']  # Number of phenotypes for Disease 1
    n2 = row['Disease 2 Phenotypes']  # Number of phenotypes for Disease 2
    
    # Perform hypergeometric test
    p_value = hypergeom.sf( K - 1, N, n1 , n2)
    
    # Append p-value to the list
    p_values.append(p_value)

# Add the p-values to the DataFrame
common_phenotypes_df['P-Value'] = p_values
common_phenotypes_df


# In[14]:


common_phenotypes_df.to_csv('Final-p-values::Orphanet.csv', index=False)


# In[ ]:


print("Hi")


# In[ ]:





# In[ ]:




