import sys

"""
    Definition of the class Grammar
"""
class Grammar:
    def __init__(self):                                                         # The Chomsky's grammar it's a 4-uple
        self.terminals = []                                                     # Makes a list of the terminal symbols
        self.variables = []                                                     # Makes a list of the variable symbols
        self.production_rules = []                                              # Makes a list of the production rules

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_variable(self, variable):
        self.variables.append(variable)

    def add_initial(self, initial):
        self.initial_symbol = initial

    def add_production_rule(self, production):
        self.production_rules.append(production)

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
        terminal = line[2:]
        index = terminal.find(" ")
        terminal = terminal[:index]
        main_grammar.add_terminal(terminal)
    else:
        break
for line in grammar_file:
    if line[0] != "#":
        variable = line[2:]
        index = variable.find(" ")
        variable = variable[:index]
        main_grammar.add_variable(variable)
    else:
        break
initial = grammar_file.readline()
initial = initial[2:]
index = initial.find(" ")
initial = initial[:index]
main_grammar.add_initial(initial)

grammar_file.readline()                                                         # Skips the line that will be "#Regras"

for line in grammar_file:
    production_rule = line[2:]
    index = production_rule.find(" ")
    production_rule = production_rule[:index]
    production_rule = production_rule + " > "
    index1 = line.find("> [ ")
    right = line[(index1 + 4):]
    right = right.split(" ] [ ",)
    for item in right:
        production_rule = production_rule + item
    index2 = production_rule.find(" ]")
    production_rule = production_rule[:index2]
    main_grammar.add_production_rule(production_rule)

grammar_file.close()

print("\n The definition of Chomsky's grammar is a 4-uple:\n")
print(" G = (V, T, P, S)\n")
print(" Where\n")
print(" V is all the variable symbols in the grammar:")
print(main_grammar.variables)
print(" T is all the terminal symbols in the grammar:")
print(main_grammar.terminals)
print(" P is all the production rules in the grammar:\n")
for production in main_grammar.production_rules:
    print(" " + production + "\n")
print(" S is the initial variable symbol in the grammar:\n")
print(" S = " + main_grammar.initial_symbol + "\n")
