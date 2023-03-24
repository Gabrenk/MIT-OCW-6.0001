# Problem Set 4A
# Name: Breno
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    #recursion must be used
    #smallest version
    if len(sequence) <= 1:
        return [sequence]
    
    #recursive part
    else:
        #create a list for all possible permutations
        permutations = []
        for i, letter in enumerate(sequence):
            # getting the permutantion of all but the first character
            for item in get_permutations(sequence[:i] + sequence[i + 1:]):
                #inserting each character
                permutations += [letter + item]

        #eliminate multiple occurrences with list(set())      
        #sort in alphabetical order and return
        return sorted(list(set(permutations)))

if __name__ == '__main__':

    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = 'bob'
    print('Input:', example_input)
    print('Expected Output:', ['bob', 'obb', 'bbo'])
    print('Actual Output:', get_permutations(example_input))
    
    example_input = 'dado'
    print('Input:', example_input)
    print('Expected Output:', ['doad', 'doda', 'ddao', 'aodd', 'dado', 'ddoa', 'oadd', 'adod', 'odad', 'daod', 'addo', 'odda'])
    print('Actual Output:', get_permutations(example_input))




