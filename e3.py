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

    print_chart(chart, word_length)





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
