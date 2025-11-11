# """Return the sum of all elements in the list 'numbers'."""
def sum_list(numbers):
    return sum(numbers)

# """Return the first element of the tuple 't'."""
def first_of_tuple(t):
    return t[0]

# """Return True if 'key' exists in dictionary 'd', else False."""
def has_key(d, key): 
    return key in d

# """Round the float 'f' to 2 decimal places."""
def round_float(f): 
    return round(f, 2)

# """Return a new list that is the reverse of 'lst'."""
def reverse_list(lst): 
    return lst[::-1]

# """For a list of items 'lst', count how many times element 'item' occurs."""
def count_occurrences(lst, item):
    return lst.count(item) 

# """Convert a list of (key, value) tuples 'pairs' into a dictionary."""
def tuples_to_dict(pairs):
    return dict(pairs) 

# """Return the number of characters in string 's'."""
def string_length(s):
    return len(s)

# """Return a list of unique elements from 'lst'."""
def unique_elements(lst):
    return set(lst)

# """Return a new dictionary with keys and values of 'd' swapped."""
def swap_dict(d): #
    return {v: k for k, v in d.items()}
