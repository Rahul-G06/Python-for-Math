'''
Sample execution:
>>> equations = get_equations()
Enter, one by one, each of the equations of the system of equations you would like to solve. Press return to exit.
10x + y + z = 12
2x + 10y + z = 13
2x + 2y + 10z = 14

>>> solve(equations, 10)
Iteration 1 is {'x': 1.2, 'z': 1.948, 'y': 1.54}
Iteration 2 is {'x': 1.5488, 'z': 2.070672, 'y': 1.80456}
Iteration 3 is {'x': 1.5875232000000001, 'z': 2.082419008, 'y': 1.8245718400000002}
Iteration 4 is {'x': 1.5906990848, 'z': 2.0834161605120003, 'y': 1.82638171776}
Iteration 5 is {'x': 1.5909797878272, 'z': 2.0835034722887675, 'y': 1.8265375736166398}
Iteration 6 is {'x': 1.5910041045905408, 'z': 2.083511054547505, 'y': 1.826551168146985}
Iteration 7 is {'x': 1.591006222269449, 'z': 2.083511714435618, 'y': 1.8265523499086402}
Iteration 8 is {'x': 1.5910064064344258, 'z': 2.083511771832975, 'y': 1.826552452730447}
Iteration 9 is {'x': 1.5910064224563423, 'z': 2.0835117768261817, 'y': 1.8265524616745659}
Iteration 10 is {'x': 1.5910064238500747, 'z': 2.0835117772605414, 'y': 1.8265524624526333}
'''

#note that all equations are to be in standard form. ax + by + cz + ... = k.
#where the coefficients of the principle diagonal are not zero.
#and the zero coefficient terms may be written so. (or they may be excluded??????)
#coefficients equal to one need not be mentioned.
#ensure that set of equations is diagonally dominant, or covergence is not guaranteed.
#it is definitely interesting to observe what happens to non diagonally dominant systems.

#read equations from user input.

def get_equations():
    ''' NoneType -> list of str

    Return a list of str containing linear equations inputted by the user.

    Precondition: Each of the equations is in standard form.

    >>> get_equations()
    Enter, one by one, each of the equations of the system of equations you would like to solve. Press return to exit.
    x + 5y + z = 6
    5x + y + 3z = 8
    x - y + 7z = 3

    ['x + 5y + z = 6', '5x + y + 3z = 8', 'x - y + 7z = 3']
    '''

    equations = []
    equation = input('''Enter, one by one, each of the equations of the system of equations you would like to solve. Press return to exit.\n''')

    while equation != '':
        equations.append(equation)
        equation = input()
        
    return equations

#clean up the equations and turn them into a list of separate terms.

def clean_up_terms(equation):
    ''' str -> list of str

    Return a cleaned list of separated terms excluding the '+', '-', signs, merge the '-' sign with the following term.

    >>> clean_up_terms('x - y + 7z = 3')
    ['x', '-1y', '7z', '=', '3']
    '''

    terms = equation.split()
    cleaned_terms = []
    
    for i in range(0, len(terms)):

        term = terms[i]
        
        if term == '-': #ensures that we retain the sign of the coefficient.
            terms[i + 1] = '-1' + terms[i+1]
        
        if term != '+' and term != '-': #retain all terms but the '+' and '-' sign. note that the '=' is retained.
            cleaned_terms.append(term)

    return cleaned_terms

#get the coefficients from the cleaned list.

def get_coefficients(cleaned_list):
    ''' list of str -> list of int

    Return the list of coefficients on the left hand side of the cleaned equations.

    >>> get_coefficients(['x', '-1y', '7z', '=', '3'])
    ['1', '-1', '7']
    '''

    coefficients = []
    valid_chars = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] #to distinguish between the coefficients and variables.
    i = 0
    
    while cleaned_list[i] != '=': #stops at the '=' i.e. only considers LHS.

        coefficient = ''
        j = 0
        
        while cleaned_list[i][j] in valid_chars: #stops at the first non numeric character.
            
            coefficient = coefficient + cleaned_list[i][j]
            j = j + 1

        coefficients.append(coefficient)
        i = i + 1

    for k in range(0, len(coefficients)): #makes sure that coefficients equal to 1, omitted in standard form, are added.
        if coefficients[k] == '':
            coefficients[k] = '1'
    return coefficients

#get the variables from the cleaned list.

def get_variables(cleaned_list):
    ''' list of str -> list of str

    Return the list of variables on the left hand side of the cleaned equations.

    >>> get_variables(['x', '5y', 'z', '=', '6'])
    ['x', 'y', 'z']
    '''
    
    variables = []
    valid_chars = ['-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    i = 0
    
    while cleaned_list[i] != '=': #stops at the '=' i.e. only considers LHS.

        variable = ''
        
        for char in cleaned_list[i]: #obtains the variable from each term.
            if char not in valid_chars:
                variable = variable + char
            
        i = i + 1
        variables.append(variable)
    return variables

#get the constant on the right hand side.

def get_constant(cleaned_list): 
    ''' list of str -> str

    Return the constant on the right hand side.
    
    >>> get_constant(['x', '5y', 'z', '=', '6'])
    '6'
    '''

    return cleaned_list[-1]

#we need a function to convert the str types in the lists to floats

def convert_to_float(list_of_strings):
    ''' list of str -> list of float

    Return a new list of all the strings converted to float.

    >>> convert_to_float(['1', '-1', '7'])
    [1.0, -1.0, 7.0]
    '''

    float_list = []

    for item in list_of_strings:
        float_list.append(float(item))

    return float_list

#a function to create a dictionary setting the initial guess to 0.

def initiialize_variables(variables):
    ''' list of str -> dict of str to float

    Return a dictionary correlating each variable with the initial guess 0.

    >>> initiialize_variables(['x', 'y', 'z'])
    {'x' : 0, 'y' : 0, 'z' : 0}
    '''
    initial_dict = {}

    for key in variables:
        initial_dict[key] = 0

    return initial_dict

#using a dictionary to correlate variables to the coefficients in the equations.

def variable_to_coefficient(variables, coefficients):
    ''' list of str, list of float -> dict of str to float

    Return a dictionary linking each variable to their respective coefficients in an equation.

    >>> variable_to_coefficient(['x', 'y', 'z'], [1.0, -1.0, 7.0])
    {'x' : 1.0, 'y' : -1.0, 'z' : 7.0}
    '''

    dictionary = {}

    for i in range(len(variables)):
        dictionary[variables[i]] = coefficients[i]

    return dictionary

#to simplify the calculations in next_iteration

def sum_of_others(variable_to_approximation, variable_to_coefficient, variable):
    ''' dict of str to float, dict of str to float, str -> float

    Return the sum of all the coefficients in variable_to_coefficients multiplied with the approximation of their respective variables in
    variable_to_approximation, except for a particular variable variable.

    >>> sum_of_others({'x' : 5.0, 'y' : -2.0, 'z' : 1.0}, {'x' : 1.0, 'y' : -1.0, 'z' : 7.0}, 'z')
    7.0
    '''

    total = -(variable_to_approximation[variable] * variable_to_coefficient[variable])

    for key in variable_to_coefficient:
        total = total + variable_to_coefficient[key] * variable_to_approximation[key]

    return total

#writing a function to iterate a particular variable

def next_iteration(variable_to_approximation, variable_to_coefficient, variable, constant):
    ''' dict of str to float, dict of str to float, str, float -> float

    Return the new approximation of a the variable variable using the Gauss-Seidel method.
    
    >>> next_iteration({'x' : 5.0, 'y' : -2.0, 'z' : 1.0}, {'x' : 1.0, 'y' : -1.0, 'z' : 7.0}, 'z', 7.0)
    2.0
    '''

    approximation = (constant + sum_of_others(variable_to_approximation, variable_to_coefficient, variable)) / variable_to_coefficient[variable]

    return approximation

#final function to get all data in required format and to perform the iterations.

def solve(equations, no_of_iterations):
    ''' list of str -> NoneType

    Print the desired number of iterations of the numerical solutions to the list of linear equations.

    >>> solve(['10x + y + z = 12', '2x + 10y + z = 13', '2x + 2y + 10z = 14'], 10)
    Iteration 1 is {'x': 1.2, 'z': 1.948, 'y': 1.54}
    Iteration 2 is {'x': 1.5488, 'z': 2.070672, 'y': 1.80456}
    Iteration 3 is {'x': 1.5875232000000001, 'z': 2.082419008, 'y': 1.8245718400000002}
    Iteration 4 is {'x': 1.5906990848, 'z': 2.0834161605120003, 'y': 1.82638171776}
    Iteration 5 is {'x': 1.5909797878272, 'z': 2.0835034722887675, 'y': 1.8265375736166398}
    Iteration 6 is {'x': 1.5910041045905408, 'z': 2.083511054547505, 'y': 1.826551168146985}
    Iteration 7 is {'x': 1.591006222269449, 'z': 2.083511714435618, 'y': 1.8265523499086402}
    Iteration 8 is {'x': 1.5910064064344258, 'z': 2.083511771832975, 'y': 1.826552452730447}
    Iteration 9 is {'x': 1.5910064224563423, 'z': 2.0835117768261817, 'y': 1.8265524616745659}
    Iteration 10 is {'x': 1.5910064238500747, 'z': 2.0835117772605414, 'y': 1.8265524624526333}
    '''

    #declaring lists
    cleaned_equations = []
    coefficients = []
    all_variables = []
    constants = []

    #clean all equations
    for equation in equations:
        cleaned_equations.append(clean_up_terms(equation))

    #get all the variables in a single list, making sure not to miss any??
    for equation in cleaned_equations:
        variables = get_variables(equation)
        for variable in variables:
            if variable not in all_variables:
                all_variables.append(variable)

    #setting initial guesses to zero
    numerical_approximation = initiialize_variables(all_variables)


    #for loop to get lists of dictionaries of coefficients, getting the constants.
    for equation in cleaned_equations:    
        coefficients.append(variable_to_coefficient(get_variables(equation), convert_to_float(get_coefficients(equation))))
        constants.append(get_constant(equation))

    #converting the constants from strs to floats
    constants = convert_to_float(constants)

    #while loop to repeat iterations
    j = 0
    while j < no_of_iterations:

        #iterating across each variable
        for i in range(len(all_variables)):
            numerical_approximation[all_variables[i]] = next_iteration(numerical_approximation, coefficients[i], all_variables[i], constants[i])

        #printing
        print("Iteration " + str(j + 1) + " is" , numerical_approximation)
        j = j + 1
        
    return

#end of program
