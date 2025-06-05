# This code will explain how to create a dataframe

# First, import pandas, it is a package that will set the dataframe into table form.
# You can download the package by going into the console, and entering:
# "pip install pandas"
import pandas as pd

# First, create lists representing the columns of each dataframe.
names = ['Ketzia', 'Joey', 'Sara', 'Steve', 'Silvia', 'JongHo', 'Nelson', 'Momo', 'Nancy']
occupation = ['Dancer', 'Assistant Designer', 'Program associate', 'programmer', 'Architect', 'Architect', 'Freelancer',
              'Unemployed', 'Assistant Designer']
age = [25, 24, 25, 27, 24, 26, 24, 24, 24]
company = ['none', 'BCBGMAXAZRIAGROUP', 'The Korea Society', 'Samsung', 'GHS Architects', 'GHS Architects', 'none',
           'none', 'Calvin Klein']

# Use len() to figure out how many items are on the list
# You want to make sure all the lists have the same amount of items
print(len(names))

# Now, create a dataframe where the lists are combined.
dataframe = {'name':names, 'age':age, 'occupation':occupation, 'company':company}
# You will notice that when you print dataframe, the format is weird and unexpected.
print(dataframe)

# To put the dataset into a table format, you'll need an extra function from pandas.
DF = pd.DataFrame(dataframe)
print(DF)
