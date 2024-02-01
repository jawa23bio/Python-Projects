#!/usr/bin/env python
# coding: utf-8

# The research article I've selected is **Orthogonality in Principal Component Analysis Allows the Discovery of Lipids in the Jejunum That Are Independent of Ad Libitum Feeding.** https://www.mdpi.com/2218-1989/12/9/866#app1-metabolites-12-00866
# 
# I've tried to replicate Figures 2B and 4A from this article.
# 
# **Fig 2B**. Loadings plot of the first and second principal components of the PCA of joining the lipidomes of the jejunum (circles) and the liver (triangles).
# 
# **Fig 4A**. Barplots of the effect of the treatments on the log of ratio between sum of triacylglycerols (TGs) and the sum of fatty acids (FAs) in the jejunum.

# In[1]:


import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# In[2]:


#Reading the file and setting the first column as row header
data = pd.read_csv("C:/Users/mahen/Downloads/Orthogonality.csv", index_col=0)
data


# In[3]:


# Apply log transformation to the numeric columns using numpy
data_1 = np.log(data)
data_1


# In[4]:


#Centering the data with mean
center_data = data_1 - data_1.mean()
center_data


# In[5]:


#Scaling the data with Standard Deviation
scaled_data = center_data / data_1.std()
scaled_data


# In[6]:


#Transposing the data
transpose_data = np.transpose(scaled_data)
transpose_data


# In[7]:


#Doig Principal component analysis for 2 coponenets
pca = PCA(n_components=2)

# Fit and transform the data using PCA
pca_result = pca.fit_transform(transpose_data)

#Flipping the axis
pca_result_inverted = pca_result * -1 

# Create a DataFrame with the PCA results
pca_df = pd.DataFrame(data=pca_result_inverted, columns=['PC1', 'PC2'], index=transpose_data.index)

# Plot the PCA results
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], c='blue', alpha=0.5)
plt.title('PCA Plot')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.show()


# In[8]:


#Values of PC1 and PC2
pca_df = pca_df.rename_axis('Sample.ID')
pca_df


# In[9]:


# Isolating the family and tissue data from Sheet 1
joiner = pd.read_csv("C:/Users/mahen/Downloads/RawData/BF550/Transformed.csv", index_col=0)
final_join = joiner.iloc[:282,38:41]
final_join


# In[10]:


#Creating 2 dataframes for the seperated columns
tissue_family_df = pd.DataFrame(final_join)
pca_df = pd.DataFrame(pca_df)

# Merge the 2 1dataframes on 'Sample.ID'
merged_df = pd.merge(tissue_family_df, pca_df, on = 'Sample.ID')

merged_df


# In[11]:


#Plotting the PCA results
liver_data = merged_df[merged_df['Tissue'] == 'Liver']
jejunum_data = merged_df[merged_df['Tissue'] == 'Jejunum']

plt.figure(figsize=(10, 8))
# Plot Liver data with circles
plt.scatter(liver_data['PC1'], liver_data['PC2'], c='none', edgecolor='black', marker='^', label='Lipid in Liver')

# Plot Jejunum data with hollow circles and black outline
plt.scatter(jejunum_data['PC1'], jejunum_data['PC2'], c='none', edgecolor='black', marker='o', label='Lipid in Jejunum')

# Jejunum data as circles differentiated by family
jej_fa = jejunum_data[jejunum_data['family'] == 'TG']
jej_sm = jejunum_data[jejunum_data['family'] == 'FA']

plt.scatter(jej_fa['PC1'], jej_fa['PC2'], c='red', marker='o', label='FA in Jejunum')
plt.scatter(jej_sm['PC1'], jej_sm['PC2'], c='blue', marker='o', label='TG in Jejunum')

# Customize plot
plt.title('PCA of the jejunal and hepatic lipidomes')
plt.xlabel('Loadings Principal Component 1')
plt.ylabel('Loadings Principal Component 2') 
plt.legend()  # Show legend with labels

# Add horizontal line at 0
plt.axhline(0, color='black', linestyle='-', linewidth=1)

# Add vertical line at 0
plt.axvline(0, color='black', linestyle='-', linewidth=1)


# Show the plot
plt.show()


# **Figure 2B**: Loadings plot of the first and second principal components of the PCA of joining the lipidomes of the jejunum (circles) and the liver (triangles).

# # 

# In[12]:


data


# In[13]:


#Splitting the rows which are from tissue-Jejunum and family-FA
Jej_FA = data.iloc[:,124:157]

#Taking sum of all jejunum TGs across each variable
Jej_FA['Sum of FA'] = Jej_FA.sum(axis=1)
Jej_FA


# In[14]:


#Splitting the rows which are from tissue-Jejunum and family-TG
Jej_TG = data.iloc[:,241:263]

#Taking sum of all jejunum FAs across each variable
Jej_TG['Sum of TG'] = Jej_TG.sum(axis=1)
Jej_TG


# In[15]:


#Splitting the sum column of TG and FA and concatenating it
s_tg = Jej_TG.iloc[:,22]
s_fa = Jej_FA.iloc[:,33]
result_df = pd.concat([s_fa, s_tg], axis=1)


# In[16]:


# Dividing the TG column by FA column
result_df['Result'] = result_df['Sum of TG'].div(result_df['Sum of FA'])
result_df


# In[17]:


#Splitting the Result column
abc = result_df.iloc[:,2]
#Taking the log of the column
z = np.log(abc)
#Adding the column back to the dataframe
result_df['Log'] = z
result_df


# In[18]:


#Taking mean and standard error of the dataframe
result_summary = result_df.groupby('Sample.ID')['Log'].agg(['mean', 'sem'])
result_summary


# In[19]:


desired_order = ['Control', 'i.V. 6h', 'i.V. 24h', 'i.V. 72h', 'i.V. 168h', 'i.V. dd 72h', 'i.P. 72h']

# Reorder the rows
result_summary = result_summary.reindex(desired_order)

# Display the reordered DataFrame
print(result_summary)


# In[20]:


#Setting colors for each of the treatments
colors = {'Control': 'white', 'i.V. 6h': 'lightpink', 'i.V. 24h': 'pink', 'i.V. 72h': 'coral', 'i.V. 168h': 'red', 'i.V. dd 72h': 'lightgreen', 'i.P. 72h': 'blue',}

# Create a bar plot with error bars and assign colors
ax = result_summary.plot(kind='bar', y='mean', yerr='sem', capsize=5, color=[colors[index] for index in result_summary.index], edgecolor='black', legend=False)

# Set labels and title
plt.ylabel('log(sum(TGs)/sum(FAs))')
plt.title('Effect of the treatment in the selected lipids in the jejunum')

# Add dotted lines after 'Control' and 'i.V. dd 72h'
ax.axvline(result_summary.index.get_loc('Control') + 0.5, linestyle='--', color='black')
ax.axvline(result_summary.index.get_loc('i.V. 168h') + 0.5, linestyle='--', color='black')
ax.axvline(result_summary.index.get_loc('i.V. dd 72h') + 0.5, linestyle='--', color='black')

plt.xticks(rotation=0)
ax.set_xlabel('')


# Show the plot
plt.show()


# **Figure 4A** : Barplots of the effect of the treatments on the log of ratio between sum of triacylglycerols (TGs) and the sum of fatty acids (FAs) in the jejunum

# In[ ]:




