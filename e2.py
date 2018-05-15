"""
 e2.py uses arguments in the command line
 To use, type in the command line:
 e2.py grammar_file
 grammar_file:            path to the grammar file that will be readed
 e1_noprints must be in the same directory to import it
"""

from e1_noprints import main_grammar, Grammar
import copy
simplified_grammar = copy.deepcopy(main_grammar)                                               # Copy the original grammar to the simplified one

"""
Simplification of the grammar
"""

"""
Exclusion of empty productions (production_rule)
1° Step: Done
2° Step: Done
3° Step: Done ?_?
"""
def delete_empty_productions():
    empty_production_variables = []                                                 # List of variables that constitute empty productions

    has_empty_production = False
    for rule in simplified_grammar.production_rules:                                # Search empty productions in the production rules
        if " V " in rule:                                                           # Search the symbol that represents the empty in each production
            has_empty_production = True
            index = rule.find(" ")                                                  # Skips the first " " that appear after the variable symbol of the left
            empty_production_variables.append(rule[:index])                         # With that, the variable symbol in the left will be added in the list
            simplified_grammar.production_rules.remove(rule)                        # Remove the empty production from the simplified grammar

    for rule in simplified_grammar.production_rules:                                # Search productions that generates a variable with empty productions
        for variable in empty_production_variables:
            new_rule = rule
            if (" " + variable + " ") in rule:
                new_rule = new_rule.replace((" " + variable + " "), " ")
                if new_rule[-2:] != "> ":
                    if new_rule not in simplified_grammar.production_rules:
                        simplified_grammar.production_rules.append(new_rule)
                        #print(new_rule)

    if has_empty_production:
        simplified_grammar.production_rules.append(simplified_grammar.initial_symbol + " > V ") # Add the production of the empty symbol by the initial symbol

delete_empty_productions()
print(" New production rules after the exclusions of the empty productions:")
print("  P = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")
