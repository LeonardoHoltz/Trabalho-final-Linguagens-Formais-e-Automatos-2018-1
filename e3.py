from e2 import simplified_grammar, Grammar

def print_chart(chart, word_length):
    for s in range(word_length):
        for r in range(word_length):
            print(chart[s][r] , end=' || ')
        print()

"""
Cocke-Younger-Kasami algorithm:
"""

def CYK(word):
    word_terminals = word.split(" ")                                            # Creates a list with each terminal that is formed by the word
    word_length = len(word_terminals)                                           # The word's length is needed to make the table for the CYK algorithm
    chart = [[0 for r in range(word_length)] for s in range(word_length)]       # Creates the chart for the CYK

    for terminal in word_terminals:                                             #This next part verify if the word has a terminal that doesn't exist in the grammar
        if terminal not in simplified_grammar.terminals:
            return 0

# This fills the first line of the chart, that is the lists of variables that produces the terminals of the word

    terminal_analyzed = 0                                                       # The index of the terminal of the word that is being analyzed
    for terminal in word_terminals:                                             # The first line of the chart will be filled with the variables that produce the terminals
        variables_list = []                                                     # Variables that produce the parts of the word, they will fill each part of the chart
        for production in simplified_grammar.production_rules:
            index = production.find(">") + 2                                    # The index marks the first char in the right of the production
            if terminal == production[index:]:                                  # If the terminal is produced in this production rule
                variable_of_production = production[:(index - 3)]
                variables_list.append(variable_of_production)                   # Add the variable to the variables list
        chart[word_length - 1][terminal_analyzed] = variables_list
        terminal_analyzed += 1                                                  # Increment for the next terminal of the word

    height = 1                                                                  # The height of the line that will be filled in each step (index)
    for s in range (1, word_length):
        word_part = height + 1                                                      # The number of word's terminals that will be analyzed
        for r in range(0,word_length-s):
            variables_list = []                                                 # Starts the list of valid variables empty
            for k in range(0, s):
                for production in simplified_grammar.production_rules:
                    index = production.find(">") + 2                            # The index marks the first char in the right of the production
                    produced_variables = production[index:].split(" ")          # Splits the two variables on the right of the production into a list
                    if chart[k][r] != 0 and chart[s-k-1][r+k+1] != 0:           # Only updates if the values that will be evaluated below and diagonally are not empty
                        if produced_variables[0] in chart[k][r]:                # Checks if the first variable is in the list of variables that form the terminal that is currently below
                            if produced_variables[1] in chart[s-k-1][r+k+1]:    # Checks if the second variable is in the list of variables that form the terminal that is currently diagonally to the right below
                                variable_of_production = production[:(index - 3)]   # If valid adds the variable on the left of the production
                                if variable_of_production not in variables_list:    # To the list of valid variables. Only if it isn't there already!!
                                    variables_list.append(variable_of_production)
            chart[s][r] = variables_list                                        # Updates the current position with the list of valid variables

    print_chart(chart, word_length)
    if simplified_grammar.initial_symbol in chart[word_length-1][0]:            # If the initial_symbol is in the first position
        return 1                                                                # Returns true otherwise returns error
    else: return -1





"""
Main:
"""

word = " "
while(word != ""):
    word = input("\n\n Please, enter the word that will be analyzed or just press 'Enter' to end the program: ")
    if word != "":
        results = CYK(word)
        if results == 0:
            print(" The word that was informed has terminals that doesn't fit in the selected grammar.\n Please, enter a word with the symbols typed correctly!")
    else:
        print("\n The program will be closed!")
