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
    right = line[index1 + 4:]
    production_rule = production_rule + right
    print(production_rule)



grammar_file.close()

print(main_grammar.initial_symbol)
print(main_grammar.terminals)
print(main_grammar.variables)


final_grammar = []
final_grammar.append(main_grammar.variables)
final_grammar.append(main_grammar.terminals)
final_grammar.append(main_grammar.initial_symbol)
print(final_grammar)
