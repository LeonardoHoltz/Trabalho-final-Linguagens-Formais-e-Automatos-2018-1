"""
 e2.py uses arguments in the command line
 To use, type in the command line:
 e2.py grammar_file
 grammar_file:            path to the grammar file that will be readed
 e1 must be in the same directory to import it
"""

from e1 import main_grammar, Grammar
import copy
simplified_grammar = copy.deepcopy(main_grammar)                                # Copy the original grammar to the simplified one

"""
Simplification of the grammar
"""

"""
Exclusion of empty productions
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
        updated_rule = rule + "]"                                               # This add a mark in the final of the production rules, just to make easy to find unit productions in the next function
        index = simplified_grammar.production_rules.index(rule)
        simplified_grammar.production_rules[index] = updated_rule


"""
Exclusion of the productions that substitute variables
"""

def delete_unit_productions():
    unit_variables = {}                                                         # Creates a dictionary that every symbol is relacionated with their unit production_rules
    for variable in simplified_grammar.variables:
        unit_variables[variable] = []
    unit_found = False
    must_delete_rules = []
    for rule in simplified_grammar.production_rules:                            # Search the production rules with unit productions
        for variable in simplified_grammar.variables:                           # For each variable that can be a unit production
            if ("> " + variable + " ]") in rule:                                # The rule must have this form to be a unit production
                index = rule.find(" >")
                right_variable = rule[:index]
                unit_variables[right_variable].append(variable)
                unit_found = True
        if unit_found:
            must_delete_rules.append(rule)
            unit_found = False
    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)

    for symbol in unit_variables:
        for variable in unit_variables[symbol]:
            for rule in simplified_grammar.production_rules:
                if (variable + " >") in rule:
                    index = rule.find(" >")
                    new_rule = symbol + rule[index:]
                    simplified_grammar.production_rules.append(new_rule)

    for rule in simplified_grammar.production_rules:
        updated_rule = rule[:-2]
        index = simplified_grammar.production_rules.index(rule)
        simplified_grammar.production_rules[index] = updated_rule

"""
Exclusion of useless symbols
"""

def delete_useless_symbols():
    # First Step
    V1 = []
    V1_size = 0
    V1_growed = True
    while(V1_growed):
        for rule in simplified_grammar.production_rules:
            index = rule.find(">")
            right_of_production = rule[(index+2):]                              # produz terminais diretamente
            left_of_production = rule[:(index-1)]
            if right_of_production in simplified_grammar.terminals or right_of_production in V1:
                if left_of_production not in V1:
                    V1.append(left_of_production)

        for rule in simplified_grammar.production_rules:
            index = rule.find(">")
            right_of_production = rule[(index+2):]
            right_of_production = right_of_production.split(" ")                # produz terminais Indiretamente
            left_of_production = rule[:(index-1)]
            for symbol in right_of_production:
                if symbol in V1:
                    if left_of_production not in V1:
                        V1.append(left_of_production)
        new_V1_size = len(V1)
        if new_V1_size > V1_size:                                               # Testa a função até que V1 não cresça mais
            V1_size = new_V1_size                                               # Aqui ele calcula se V1 cresceu desde o ultimo laço while ou não
            V1_growed = True
        else:
            V1_growed = False

    must_delete_variables = []
    must_delete_rules = []
    for variable in simplified_grammar.variables:
        if variable not in V1:
            must_delete_variables.append(variable)
            for rule in simplified_grammar.production_rules:
                if variable in rule:
                    must_delete_rules.append(rule)
    for variable in must_delete_variables:
        simplified_grammar.variables.remove(variable)
    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)

    # Second Step
    T2 = []
    V2 = []
    V2.append(simplified_grammar.initial_symbol)
    V2_size = 1
    T2_size = 0
    V2_growed = True
    T2_growed = True
    while(V2_growed or T2_growed):
        for rule in simplified_grammar.production_rules:
            index = rule.find(">")
            right_of_production = rule[(index+2):]
            right_symbols = right_of_production.split(" ")
            for symbol in right_symbols:
                if symbol in simplified_grammar.variables:
                    if symbol not in V2:
                        V2.append(symbol)
                else:
                    if symbol not in T2:
                        T2.append(symbol)
        new_V2_size = len(V2)
        new_T2_size = len(T2)
        if new_V2_size > V2_size:
            V2_size = new_V2_size
            V2_growed = True
        else:
            V2_growed = False
        if new_T2_size > T2_size:
            T2_size = new_T2_size
            T2_growed = True
        else:
            T2_growed = False

    must_delete_rules = []
    must_delete_symbols = []
    for rule in simplified_grammar.production_rules:
        index = rule.find(">")
        right_of_production = rule[(index+2):]
        right_symbols = right_of_production.split(" ")
        for symbol in right_symbols:
            if symbol not in V2 and symbol not in T2:
                if rule not in must_delete_rules:
                    must_delete_rules.append(rule)
                if symbol not in must_delete_symbols:
                    must_delete_symbols.append(symbol)

    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)
    for symbol in must_delete_symbols:
        if symbol in simplified_grammar.variables:
            simplified_grammar.variables.remove(symbol)
        else:
            simplified_grammar.terminals.remove(symbol)

def chomsky_normal_form():


delete_empty_productions()
print(" New production rules after the exclusions of the empty productions:")
print("  P = { " + ",\n        ".join(production[:-2] for production in simplified_grammar.production_rules) + " }")
delete_unit_productions()
print(" \nNew production rules after the exclusions of the productions that substitute variables:")
print("  P = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")
delete_useless_symbols()
print(" \nNew production rules after the exclusions of useless symbols and productions:")
print("  P = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")

print("\n This is the new grammar after the process of simplification:\n")
print(" G' = (V', T', P', S)\n")
print(" Where\n")
print(" V' is all the variable symbols in the grammar after the simplification:")
print("  V' = {"+ ", ".join(variable for variable in simplified_grammar.variables) + "}")
print(" T' is all the terminal symbols in the grammar after the simplification:")
print("  T' = {"+ ", ".join(terminal for terminal in simplified_grammar.terminals) + "}")
print(" P' is all the production rules in the grammar after the simplification:")
print("  P' = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")
print(" S is the initial variable symbol in the grammar:")
print("  S = " + simplified_grammar.initial_symbol)
