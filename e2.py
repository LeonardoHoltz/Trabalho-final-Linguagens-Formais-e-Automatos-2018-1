"""
 e2.py uses arguments in the command line
 To use, type in the command line:
 e2.py grammar_file
 grammar_file:            path to the grammar file that will be readed
 e1_noprints must be in the same directory to import it
"""

from e1_noprints import main_grammar, Grammar
simplified_grammar = Grammar()

"""
Simplification of the grammar
"""

"""
Exclusion of empty productions
1° Step: Done
"""

empty_production_variables = []                                                 # List of variables that constitute empty productions

for rule in main_grammar.production_rules:                                      # Search empty productions in the production rules
    if " V " in rule:                                                           # Search the symbol that represents the empty in each production
        index = rule.find(" ")                                                  # Skips the first " " that appear after the variable symbol of the left
        empty_production_variables.append(rule[:index])                         # With that, the variable symbol in the left will be added in the list

print(empty_production_variables)
