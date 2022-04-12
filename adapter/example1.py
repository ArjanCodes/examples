from bs4 import BeautifulSoup 

# Reading the data inside the xml file to a variable under the name  data
with open('models.xml', 'r') as f:
    data = f.read() 

# Passing the stored data inside the beautifulsoup parser 
bs_data = BeautifulSoup(data, 'xml') 

# Finding all instances of tag   
b_unique = bs_data.find_all('unique') 
print(b_unique) 

# Using find() to extract attributes of the first instance of the tag 
b_name = bs_data.find('child', {'name':'Acer'}) 
print(b_name) 

# Extracting the data stored in a specific attribute of the `child` tag 
value = b_name.get('qty') 
print(value)
