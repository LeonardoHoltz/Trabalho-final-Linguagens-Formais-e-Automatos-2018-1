"""
 e1.py uses arguments in the command line
 To use, type in the command line:
 e1.py grammar_file
 grammar_file:            path to the grammar file that will be readed
"""
import sys

"""
    Definition of the class Grammar
"""
class Grammar:
    def __init__(self):
        self.terminals = []                                                     # Makes a list of the terminal symbols
        self.variables = []                                                     # Makes a list of the variable symbols
        self.production_rules = []                                              # Makes a list of the production rules

    def add_terminal(self, terminal):
        self.terminals.append(terminal)                                         # Add the terminal to the terminals list

    def add_variable(self, variable):
        self.variables.append(variable)                                         # Add the variable to the variables list

    def add_initial(self, initial):
        self.initial_symbol = initial                                           # Set the initial symbol

    def add_production_rule(self, production):
        self.production_rules.append(production)                                # Add the production to the productions list

#-------------------------------------------------------------------------------
"""
 Creation of the grammar that the program will use:
"""
main_grammar = Grammar()

"""
 Grammar file opening, placing the terminal and variable symbols within the grammar created before:
"""
file_name = sys.argv[1]                                                         # The second argument in the command line will be the name of the grammar file
grammar_file = open(file_name, 'r')                                             # Opens the file with permission to read
grammar_file.readline()                                                         # Skips the first line that always will be "#Terminais"
for line in grammar_file:
    if line[0] != "#":
        terminal = line[2:]                                                     # Skips the first part of the line that will be "[ "
        index = terminal.find(" ")                                              # Find the index of the line that is " "
        terminal = terminal[:index]                                             # Skips the part of the line after " "
        main_grammar.add_terminal(terminal)                                     # Add the terminal to the terminals list
    else:
        break                                                                   # Skips the line that contain "#Variaveis
for line in grammar_file:
    if line[0] != "#":
        variable = line[2:]                                                     # Skips the first part of the line that will be "[ "
        index = variable.find(" ")                                              # Find the index of the line that is " "
        variable = variable[:index]                                             # Skips the part of the line after " "
        main_grammar.add_variable(variable)                                     # Add the variable to the variables list
    else:
        break                                                                   # Skips the line that contain "#Inicial
initial = grammar_file.readline()
initial = initial[2:]                                                           # Skips the first part of the line that will be "[ "
index = initial.find(" ")                                                       # Find the index of the line that is " "
initial = initial[:index]                                                       # Skips the part of the line after " "
main_grammar.add_initial(initial)                                               # Set the initial symbol of the grammar

grammar_file.readline()                                                         # Skips the line that will be "#Regras"

for line in grammar_file:
    production_rule = line[2:]                                                  # Skips the first part of the line that will be "[ "
    index = production_rule.find(" ")                                           # Find the index of the line that is " "
    production_rule = production_rule[:index]                                   # Skips the part of the line after " "
    production_rule = production_rule + " > "                                   # Add " > " in the string's end
    index1 = line.find("> [ ")                                                  # Find the index of the line that is "> [ "
    right = line[(index1 + 4):]                                                 # The right of the production rule will start with a symbol
    right = right.split(" ] [ ",)                                               # Transform the right of the p.r. in a list of symbols
    for item in right:
        production_rule = production_rule + item + " "                          # Concatenates the production rule ("'Symbol' > ") with each symbol in the list
    index2 = production_rule.find(" ]")                                         # Find the index of production_rule that is " ]"
    production_rule = production_rule[:index2]                                  # Skips the part of the p.r. after " ]"
    production_rule = production_rule + " "                                     # Add a " " in the end for future string manipulations
    main_grammar.add_production_rule(production_rule)                           # Add the production rule to the production rules list

grammar_file.close()                                                            # Closes the grammar file
