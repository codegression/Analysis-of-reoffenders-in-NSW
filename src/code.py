#!/usr/bin/env python
# coding: utf-8

# # Analysis of Reoffenders in NSW

# Python code to analyze reoffenders in NSW based on data the NSW Reoffendng Database from the NSW Bureau of Crime Statistics and Research.

# # Loading libraries

# Let's load relevant Python libraries.

# In[1]:


import numpy as np 
import pandas as pd 
import seaborn as sns
import plotly.express as px
from plotly import graph_objects as go
import matplotlib.pyplot as plt 
from matplotlib.ticker import MaxNLocator
from IPython.display import display, Markdown
import matplotlib as mpl
import warnings
warnings.filterwarnings("ignore")


# # Loading data

# The dataset was acquired from the NSW Bureau of Crime Statistics and Research. 

# In[2]:


filename = 'Reoffending in NSW.xlsx';
data = pd.ExcelFile(filename)


# Let's list the sheets.

# In[3]:


data.sheet_names


# # Analysis of reoffenders without imprisonment

# Let's analyze people reoffending within 12 months with proven prior finalised court appearances, completed Youth Justice Conferences, or received a penalty other than prison.

# In[4]:


data = pd.read_excel(filename, 'Table 1')
data.head(10)


# The first 6 rows need to be skipped because they are part of a header.

# In[5]:


data.tail(12)


# The last 11 rows need to be skipped.

# In[6]:


data = pd.read_excel(filename, 'Table 1', skiprows=6, skipfooter=11)
data.rename(columns={'Unnamed: 0' : '', 'Unnamed: 1' : ' '}, inplace=True)


# In[7]:


data.head()


# Let's fill up NaN values of the first columns with their preceeding values.

# In[8]:


for i in range(1, len(data)):
    if str(data[''][i])=='nan':
        data[''][i] = data[''][i-1]
    if str(data[' '][i])=='nan':
        data[' '][i] = data[' '][i-1]    
    if data[''][i].startswith('Adults'):
        data[''][i]='Adults'
    if data[''][i].startswith('Juveniles'):
        data[''][i]='Juveniles'
    if data[' '][i].startswith('Proportion'):
        data[' '][i] = 'Average'
data = data.reset_index(drop=True)
data.head()


# We are only interested in percentage values since absolute values do not convey a lot of information. 

# In[9]:


data = data[data['Unnamed: 2']=='%']
data.drop(['Unnamed: 2'], axis=1, inplace=True)
data = data.reset_index(drop=True)
data = data.set_index(['', ' ']).T


# In[10]:


data.head()


# ### Analysis of changes over time

# Let's see whether there are any significant changes in the proportions of reoffending in NSW.

# In[11]:


ax = sns.lineplot(data=data)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlabel('Year')              
plt.ylabel('Percentage')
plt.title('Reoffending rates in NSW over time')     
plt.show()


# In[12]:


ax = data.plot()
plt.legend(loc='upper right')     
plt.legend(bbox_to_anchor=(1.05, 1))   
plt.xlabel('Year')              
plt.ylabel('Percentage')
plt.title('Reoffending rates in NSW over time')       
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()


# Now that we have established that the reoffending rates are fairly constant as shown above, let's calculate the mean value for each category.

# ### Adults

# In[13]:


count_html_output = 1
def SaveAsHTML(fig):
    global count_html_output
    #fig.show()
    #pio.write_html(fig, file='src/' + str(count_html_output) + '.html', auto_open=False)
    #print ('<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="src/' + str(count_html_output) + '.html" height="100%" width="100%"></iframe>')
    fig.write_image("src/chart" + str(count_html_output) + ".png")
    display(Markdown("![png](src/chart" + str(count_html_output) + ".png)"))
    count_html_output = count_html_output + 1


# In[14]:


mean = data.mean(axis=0).sort_values(ascending=False)


# In[15]:


df = pd.DataFrame(
     {'Proportion': list(mean['Adults']),
     'Cohort': list(mean['Adults'].index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Cohort'
               )
SaveAsHTML(fig)


# For adults, indigenous people, on average, have 31.76% reoffending rate, which is the highest offending rate. Males tend to have high reoffending rate than females (18.9% versus 15.2%). Reoffending rate seems to decrease with age. Note that the cohorts are overlapped. For instance, the "18 to 24" cohort includes male, female, indigenous, and non-indigenous. Likewise, "indigenous" includes male, female, and all age groups.

# ### Juveniles

# In[16]:


df = pd.DataFrame(
     {'Proportion': list(mean['Juveniles']),
     'Cohort': list(mean['Juveniles'].index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Cohort',
                color_discrete_sequence=px.colors.sequential.RdBu
               )
SaveAsHTML(fig)


# Just like adults, indigenous teenagers tend to have higher reoffending rate than non-indigenous teenagers (according to the data). 
# Boys tend to have high reoffending rate than girls. Reoffending rate seems to decrease with age. 

# Let's plot two categories side by side.

# In[17]:


df = pd.DataFrame(
     {'Proportion': list(mean),
     'Cohort': [x[1] for x in mean.index],  
     'Category': [x[0] for x in mean.index],
      })


# In[18]:


df.sort_values('Proportion', ascending=False, inplace=True)


# In[19]:


fig = px.bar(df, x='Proportion',
             y='Cohort',
             barmode='group',
             color='Category')
SaveAsHTML(fig)

fig = px.bar(df, x='Proportion',
             y='Cohort',       
             color='Category')
SaveAsHTML(fig)


# # Analysis of reoffenders with imprisonment

# Let's analyze people released from prison in ROD custody data between 2000 and 2017.

# In[20]:


data = pd.read_excel(filename, 'Table 2', skiprows=6, skipfooter=11)
data.head()


# In[21]:


data.rename(columns={'Unnamed: 0' : '', 'Unnamed: 1' : ' '}, inplace=True)


# In[22]:


data.head()


# Let's fill up NaN values of the first columns with their preceeding values.

# In[23]:


for i in range(1, len(data)):
    if str(data[''][i])=='nan':
        data[''][i] = data[''][i-1]
    if str(data[' '][i])=='nan':
        data[' '][i] = data[' '][i-1]    
    if data[''][i].startswith('Adult'):
        data[''][i]='Adults'
    if data[''][i].startswith('Juvenile'):
        data[''][i]='Juveniles'
    if data[' '][i].startswith('Proportion'):
        data[' '][i] = 'Average'
data = data.reset_index(drop=True)
data.head()


# We are only interested in percentage values since absolute values do not convey a lot of information. 

# In[24]:


data = data[data['Unnamed: 2']=='%']
data.drop(['Unnamed: 2'], axis=1, inplace=True)
data = data.reset_index(drop=True)
data = data.set_index(['', ' ']).T


# In[25]:


data.drop([('Adults', '10 to 13'), 
        ('Adults', '14 to 17'),
       ('Juveniles', '18 to 24'),
        ('Juveniles', '25 to 34'),
        ('Juveniles', '35 to 44'),
        ('Juveniles', '45 and over'),
       ], axis=1, inplace=True)


# In[26]:


data.head()


# ### Analysis of changes over time

# Let's see whether there are any significant changes in the proportions of reoffending for offences involving imprisonment.

# In[27]:


ax = sns.lineplot(data=data)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlabel('Year')              
plt.ylabel('Percentage')
plt.title('Reoffending rates in NSW over time')     
plt.show()


# Now that we have established that the reoffending rates are fairly constant, let's calculate the mean value for each category.

# ### Adults

# In[28]:


mean = data.mean(axis=0).sort_values(ascending=False)


# In[29]:


df = pd.DataFrame(
     {'Proportion': list(mean['Adults']),
     'Cohort': list(mean['Adults'].index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Cohort'
               )
SaveAsHTML(fig)


# Just like offences without imprisonment, the indigenous adults, on average, have the highest offending rate. One thing that is intesting is that, the reoffending rate of men is slightly lower than that of women, contrary to the offences without imprisonment. Reoffending rate decreases with age. 
# 
# In general, reoffending rates of people committing offences involving imprisonment are significantly higher than those committing offences that do not involve imprisonment.

# ### Juveniles

# In[30]:


df = pd.DataFrame(
     {'Proportion': list(mean['Juveniles']),
     'Cohort': list(mean['Juveniles'].index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Cohort',
                color_discrete_sequence=px.colors.sequential.RdBu
               )
SaveAsHTML(fig)


# The rates rare so high especially the '10 to 13' cohort which has a whopping 72.95% reoffending rate.

# In[31]:


df = pd.DataFrame(
     {'Proportion': list(mean),
     'Cohort': [x[1] for x in mean.index],  
     'Category': [x[0] for x in mean.index],
      })


# In[32]:


df.sort_values('Proportion', ascending=False, inplace=True)


# In[33]:


fig = px.bar(df, x='Proportion',
             y='Cohort',
             barmode='group',
             color='Category')
SaveAsHTML(fig)

fig = px.bar(df, x='Proportion',
             y='Cohort',       
             color='Category')
SaveAsHTML(fig)


# # Analysis of reoffenders committing the same offences

# Let's analyze people re-offending within the same offences within 12 months after getting released.

# In[34]:


data = pd.read_excel(filename, 'Table 3', skiprows=6, skipfooter=11)
data.head()


# Let's fill up NaN values of the first columns with their preceeding values.

# In[35]:


data.rename(columns={'Unnamed: 0' : ''}, inplace=True)
for i in range(1, len(data)):
    if str(data[''][i])=='nan':
        data[''][i] = data[''][i-1]         
    if str(data[2008][i])=='nan':
        for year in range(2008, 2018):
            data[year][i] = data[year][i-1]
data = data.reset_index(drop=True)
data.head()


# We are only interested in percentage values since absolute values do not convey a lot of information. 

# In[36]:


data = data[data['Unnamed: 2']=='%']
data.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16'], axis=1, inplace=True)
data.head()


# In[37]:


data = data.reset_index(drop=True)
data = data.set_index(['']).T
data.head()


# In[38]:


data.head()


# Let's see whether there are any significant changes in the proportions of Reoffending in NSW.

# In[39]:


ax = data.plot()
plt.legend(loc='upper right')     
plt.legend(bbox_to_anchor=(1.05, 1))   
plt.xlabel('Year')              
plt.ylabel('Percentage')
plt.title('Reoffending rates in NSW over time')       
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()


# Theft and related offences have the highest reoffending rate and for some reason the offending rate is increasing year by year. Let's take a look at individual plots.

# In[40]:


max = data.max().sort_values(ascending=False)
np.random.seed(4)
colors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(max), replace=False)

for i, crime in enumerate(max.index):
    display(Markdown("### " + crime))
    print()
    ax = data[crime].plot(kind = 'line', color=colors[i],linewidth=2,alpha = 1,grid = True,linestyle = '-')     
    plt.xlabel('Year')              
    plt.ylabel('Percentage')   
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
    print()


# In[41]:


mean = data.mean(axis=0).sort_values(ascending=False)
df = pd.DataFrame(
     {'Proportion': list(mean),
     'Crime': list(mean.index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Crime',
                color_discrete_sequence=px.colors.sequential.Agsunset
               )

#fig.update_yaxes(showticklabels=False)
fig.update_layout(
    margin=dict(l=500)   
)
SaveAsHTML(fig)


# In[42]:


#df = data.reset_index().rename(columns={'index':'Year'}).melt(id_vars='Year', var_name='Crime', value_name='Proportion(%)')

#fig = px.line(df, x="Year", y="Proportion(%)", color='Crime')

#fig.show()


# # Analysis of reoffenders committing any other offences

# Let's analyze people re-offending within the same offences within 12 months after getting released.

# In[43]:


data = pd.read_excel(filename, 'Table 4', skiprows=6, skipfooter=11)
data.head()


# Let's fill up NaN values of the first columns with their preceeding values.

# In[44]:


data.rename(columns={'Unnamed: 0' : ''}, inplace=True)
for i in range(1, len(data)):
    if str(data[''][i])=='nan':
        data[''][i] = data[''][i-1]         
    if str(data[2008][i])=='nan':
        for year in range(2008, 2018):
            data[year][i] = data[year][i-1]
data = data.reset_index(drop=True)
data.head()


# We are only interested in percentage values since absolute values do not convey a lot of information. 

# In[45]:


data = data[data['Unnamed: 2']=='%']
data.drop(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16'], axis=1, inplace=True)
data.head()


# In[46]:


data = data.reset_index(drop=True)
data = data.set_index(['']).T
data.head()


# In[47]:


data.head()


# Let's see whether there are any significant changes in the proportions of reoffending in NSW.

# In[48]:


ax = data.plot()
plt.legend(loc='upper right')     
plt.legend(bbox_to_anchor=(1.05, 1))   
plt.xlabel('Year')              
plt.ylabel('Percentage')
plt.title('Reoffending rates in NSW over time')       
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()


# Again, theft and related offences have the highest reoffending rate. Let's take a look at individual plots.

# In[49]:


max = data.max().sort_values(ascending=False)
np.random.seed(4)
colors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(max), replace=False)

for i, crime in enumerate(max.index):
    display(Markdown("### " + crime))
    print()
    ax = data[crime].plot(kind = 'line', color=colors[i],linewidth=2,alpha = 1,grid = True,linestyle = '-')     
    plt.xlabel('Year')              
    plt.ylabel('Percentage')   
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()
    print()


# In[50]:


mean = data.mean(axis=0).sort_values(ascending=False)
df = pd.DataFrame(
     {'Proportion': list(mean),
     'Crime': list(mean.index),     
      })
    
fig = px.funnel(df,
                x = 'Proportion',
                y = 'Crime',
                color_discrete_sequence=px.colors.diverging.Earth
               )

#fig.update_yaxes(showticklabels=False)
fig.update_layout(
    margin=dict(l=500)   
)
SaveAsHTML(fig)


# In[51]:


#df = data.reset_index().rename(columns={'index':'Year'}).melt(id_vars='Year', var_name='Crime', value_name='Proportion(%)')

#fig = px.line(df, x="Year", y="Proportion(%)", color='Crime')

#fig.show()

