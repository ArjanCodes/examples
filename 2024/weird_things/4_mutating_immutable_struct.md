# Run the following in the Python console
# Expected bevahior! data is (1,2)
data = (1, 2)
data[0] += 1 # Returns an error
data # Is (1,2)

# Not expected! data is ([1, 3], 2)
data = ([1],2)
data[0] += [3]
data 
