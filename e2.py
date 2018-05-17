"""
 e2.py uses arguments in the command line
 To use, type in the command line:
 e2.py grammar_file
 grammar_file:            path to the grammar file that will be readed
 e1_noprints must be in the same directory to import it
"""

from e1_noprints import main_grammar, Grammar
import copy
simplified_grammar = copy.deepcopy(main_grammar)                                # Copy the original grammar to the simplified one

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
    empty_production_variables = []                                             # List of variables that constitute empty productions

    has_empty_production = False                                                # This marks that if the empty symbols is in the grammar alphabet, for now it's just false
    for rule in simplified_grammar.production_rules:                            # Search empty productions in the production rules
        if " V " in rule:                                                       # Search the symbol that represents the empty in each production
            has_empty_production = True                                         # The empty symbol is in the grammar alphabet, now it's true
            index = rule.find(" ")                                              # Skips the first " " that appear after the variable symbol of the left
            empty_production_variables.append(rule[:index])                     # With that, the variable symbol in the left will be added in the list
            simplified_grammar.production_rules.remove(rule)                    # Remove the empty production from the simplified grammar

    for rule in simplified_grammar.production_rules:                            # Search productions that generates a variable with empty productions
        for variable in empty_production_variables:                             # For each variable with empty productions
            new_rule = rule                                                     # New production rule that can be added to the grammar
            if (" " + variable + " ") in rule:                                  # If the variable with empty production is in the actual rule
                new_rule = new_rule.replace((" " + variable + " "), " ")        # Removes that variable from the new production rule
                if new_rule[-2:] != "> ":                                       # If that don't generates something like "Symbol > " (no symbols in the right side)
                    if new_rule not in simplified_grammar.production_rules:     # and if the new rule is not yet in the production rules list,
                        simplified_grammar.production_rules.append(new_rule)    # the new rule finally can be added in the list

    if has_empty_production:
        simplified_grammar.production_rules.append(simplified_grammar.initial_symbol + " > V ") # Add the production of the empty symbol by the initial symbol

    for rule in simplified_grammar.production_rules:
        rule = rule[:-1]

"""
def delete_unit_productions():
    unit_variables = {}                                                         # Creates a dictionary that every symbol is relacionated with their unit production_rules
    for rule in simplified_grammar.production_rules:                            # Search the production rules with unit productions
        for variable in simplified_grammar.variables:                           # For each variable that can be a unit production
            if ("> " + variable) in rule:                                       # The
"""

delete_empty_productions()
print(" New production rules after the exclusions of the empty productions:")
print("  P = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")
