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

    for rule in simplified_grammar.production_rules:                            # Search empty productions in the production rules
        if " V " in rule:                                                       # Search the symbol that represents the empty in each production
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

    for rule in simplified_grammar.production_rules:
        updated_rule = rule + "¬"                                               # This add a mark in the final of the production rules, just to make easy to find unit productions in the next function
        index = simplified_grammar.production_rules.index(rule)
        simplified_grammar.production_rules[index] = updated_rule

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
Exclusion of the productions that substitute variables
"""

def delete_unit_productions():
    unit_variables = {}                                                         # Creates a dictionary that every symbol is relacionated with their unit production_rules
    for variable in simplified_grammar.variables:
        unit_variables[variable] = []                                           # Each variable in this dictionary has a list relacionated
    unit_found = False                                                          # Boolean that represents if a unit production has been found
    must_delete_rules = []                                                      # List of production rules that will be deleted from the grammar
    for rule in simplified_grammar.production_rules:                            # Search the production rules with unit productions
        for variable in simplified_grammar.variables:                           # For each variable that can be a unit production
            if ("> " + variable + " ¬") in rule:                                # The rule must have this form to be a unit production
                index = rule.find(" >")                                         # Finds the index of ">"
                left_variable = rule[:index]                                    # Variable that generates the production
                unit_variables[left_variable].append(variable)                  # Add the right variable to the list relacionated to the left variable
                unit_found = True                                               # The unit production has been found in the rule
        if unit_found:                                                          # If the unit porduction was found
            must_delete_rules.append(rule)                                      # Add the rule to the list of productio nrules that must be removed
            unit_found = False                                                  # Set the boolean to false
    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)                        # Removes the production rules from the grammar

    for symbol in unit_variables:                                               # For each Symbol that generates unit productions,
        for variable in unit_variables[symbol]:                                 # for each variable that is a unit production of that symbol
            for rule in simplified_grammar.production_rules:                    # and for each rule in the grammar,
                if (variable + " >") in rule:
                    index = rule.find(" >")
                    new_rule = symbol + rule[index:]                            # The productions of the variable will be added to the symbol that generates that variable by a unit production
                    simplified_grammar.production_rules.append(new_rule)        # If any rule will be created in that way, this new rule will be added to the grammar

    for rule in simplified_grammar.production_rules:                            # For all rules in the grammar
        updated_rule = rule[:-2]                                                # Removes the "¬" mark from the rule
        index = simplified_grammar.production_rules.index(rule)                 # Checks the index of that rule in the grammar
        simplified_grammar.production_rules[index] = updated_rule               # Update the rule without the mark
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
Exclusion of useless symbols
"""

def delete_useless_symbols():
    # First Step (Symbols that produces terminals):
    V1 = []                                                                     # Creates the list of symbols that can generate a terminal directly or indirectly
    V1_size = 0                                                                 # Represents the size of the V1 symbols' list
    V1_growed = True                                                            # Boolean that represents if the V1 symbols' list has growed up or not. For now this one is True
    while(V1_growed):                                                           # Checks if the V1 growed up to continue the loop
        # Detects if the symbol generates a terminal directly:
        for rule in simplified_grammar.production_rules:                        # Search in the grammar's rules
            index = rule.find(">")                                              # Finds the index of ">"
            right_of_production = rule[(index+2):]                              # String that will be the right of the production
            left_of_production = rule[:(index-1)]                               # String that will be the left of the production
            if right_of_production in simplified_grammar.terminals or right_of_production in V1: # If the production generates a terminal or a variable that is already in V1
                if left_of_production not in V1:
                    V1.append(left_of_production)                               # The symbol that generates the production will be put on V1's list
        # Detects if the symbol generates a terminal indirectly:
        for rule in simplified_grammar.production_rules:                        # Search in the grammar's rules
            index = rule.find(">")                                              # Finds the index of ">"
            right_of_production = rule[(index+2):]                              # String that will be the right of the production
            right_of_production = right_of_production.split(" ")                # Creates a list of the symbols in the right of the production
            left_of_production = rule[:(index-1)]                               # String that will be the left of the production
            for symbol in right_of_production:                                  # For each symbol in the production,
                if symbol in V1:                                                # if the symbol is in V1
                    if left_of_production not in V1:
                        V1.append(left_of_production)                           # the symbol that generates the production will be put on V1 list

        new_V1_size = len(V1)                                                   # Calculates the new size of the V1 list

        if new_V1_size > V1_size:                                               # Checks if V1 has growed up
            V1_size = new_V1_size                                               # if has growed up, replaces the original size
            V1_growed = True                                                    # and indicates that has growed up by the boolean True
        else:
            V1_growed = False                                                   # If haven't growed up, the boolean now is False

    must_delete_variables = []                                                  # List of the variables that will be deleted from the grammar
    must_delete_rules = []                                                      # List of production rules that will be deleted from the grammar
    for variable in simplified_grammar.variables:                               # For each variable in the grammar,
        if variable not in V1:                                                  # if it's not on the V1 list
            must_delete_variables.append(variable)                              # Add the variable in the list of variables that must be removed from the grammar
            for rule in simplified_grammar.production_rules:                    # If a rule generates that variable
                if variable in rule:
                    must_delete_rules.append(rule)                              # Add the rule in the list of rules that will be removed from the grammar

    for variable in must_delete_variables:
        simplified_grammar.variables.remove(variable)                           # Removes the variables from the grammar
    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)                        # Removes the production rules from the grammar

    # Second Step (Symbols that can't be reached by the initial symbol):
    T2 = []                                                                     # Creates a list of terminals that can be reached
    V2 = []                                                                     # Creates a list of variables that can be reached
    V2.append(simplified_grammar.initial_symbol)                                # Add the initial symbol in V2 list
    V2_size = 1                                                                 # Represents the size of the V2 variables' list
    T2_size = 0                                                                 # Represents the size of the T2 terminals' list
    V2_growed = True                                                            # Boolean that represents if the V2 variables' list has growed up or not. For now this one is True
    T2_growed = True                                                            # Boolean that represents if the T2 terminals' list has growed up or not. For now this one is True
    while(V2_growed or T2_growed):                                              # Checks if the V2 or T2 growed up to continue the loop
        for rule in simplified_grammar.production_rules:                        # Search in the grammar's rules
            index = rule.find(">")                                              # Finds the index of ">"
            right_of_production = rule[(index+2):]                              # String that will be the right of the production
            right_symbols = right_of_production.split(" ")                      # Creates a list of the symbols in the right of the production
            for symbol in right_symbols:                                        # For each symbol generated by the production,
                if symbol in simplified_grammar.variables:                      # if symbol is a variable
                    if symbol not in V2:
                        V2.append(symbol)                                       # the symbol will be put on V2 list
                else:                                                           # if the symbol is a terminal
                    if symbol not in T2:
                        T2.append(symbol)                                       # the symbol will be put on T2 list
        print(V2)
        new_V2_size = len(V2)                                                   # Calculates the new size of the V2 list
        new_T2_size = len(T2)                                                   # Calculates the new size of the T2 list
        if new_V2_size > V2_size:                                               # Checks if V2 has growed up
            V2_size = new_V2_size                                               # if has growed up, replaces the original size
            V2_growed = True                                                    # and indicates that has growed up by the boolean True
        else:
            V2_growed = False                                                   # If haven't growed up, the boolean now is False

        if new_T2_size > T2_size:                                               # Checks if T2 has growed up
            T2_size = new_T2_size                                               # if has growed up, replaces the original size
            T2_growed = True                                                    # and indicates that has growed up by the boolean True
        else:
            T2_growed = False                                                   # If haven't growed up, the boolean now is False

    must_delete_rules = []                                                      # List of production rules that will be deleted from the grammar
    must_delete_symbols = []                                                    # List of symbols that will be deleted from the grammar
    for rule in simplified_grammar.production_rules:                            # Search in the grammar's rules
        index = rule.find(">")                                                  # Finds the index of ">"
        right_of_production = rule[(index+2):]                                  # String that will be the right of the production
        left_of_production = rule[:(index-1)]                                   # String that will be the symbol in the left of the production
        right_symbols = right_of_production.split(" ")                          # Creates a list of the symbols in the right of the production
        for symbol in right_symbols:                                            # For each symbol generated by the production,
            if symbol not in V2 and symbol not in T2:                           # if the symbol is neither a variable from V2 list and a terminal from T2 list
                if rule not in must_delete_rules:
                    must_delete_rules.append(rule)                              # Add the rule in the list of rules that will be removed from the grammar
                if symbol not in must_delete_symbols:
                    must_delete_symbols.append(symbol)                          # Add the symbol in the list of symbols that will be removed from the grammar
        if left_of_production not in V2:                                        # If the symbol that generates the production is not in V2 list
            if rule not in must_delete_rules:
                must_delete_rules.append(rule)                                  # Add the rule in the list of rules that will be removed from the grammar
                must_delete_symbols.append(symbol)                              # Add the symbol in the list of symbols that will be removed from the grammar

    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)                        # Removes the production rules from the grammar
    for symbol in must_delete_symbols:
        if symbol in simplified_grammar.variables:
            simplified_grammar.variables.remove(symbol)                         # Removes the variables from the grammar
        else:
            simplified_grammar.terminals.remove(symbol)                         # Removes the terminals from the grammar

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
Chomsky Normal Form
"""

def chomsky_normal_form():
    extra_variables_v = 1                                                       # Counter for the extra variables that produces 2 variables that will be added to the grammar
    must_delete_rules = []                                                      # List of production rules that will be deleted from the grammar

    # Creates the variables that generates only one terminal
    for terminal in simplified_grammar.terminals:                               # Creates new production rules. Each one produces one terminal
        new_variable = "C{0}".format(terminal)                                  # Creates the new variable
        new_rule = new_variable + " > " + terminal                              # Creates the new rule
        simplified_grammar.variables.append(new_variable)                       # Put the new variable in the list of variables of the grammar
        simplified_grammar.production_rules.append(new_rule)                    # Put the new rule in the list of production of the grammar

    # If a production generates 3 or more symbols and at least on of them is a terminal, it's replaced by "C" with the index of the terminal
    for rule in simplified_grammar.production_rules:                            # Search in all the production rules
        index = rule.find(">")                                                  # Finds the index of ">"
        right_of_production = rule[(index+2):]                                  # The right of the production will be the string after "> "
        right_symbols = right_of_production.split(" ")                          # Each symbol of resulting production is in a list
        number_of_symbols = len(right_symbols)                                  # Represents the number of symbols that the rule produces
        if number_of_symbols > 2:
            for symbol in right_symbols:
                if symbol in simplified_grammar.terminals:
                    new_rule = rule.replace(symbol, ("C" + symbol))             # Replaces the ocorrence of the terminal symbol withthe variable that produces the terminal
                    must_delete_rules.append(rule)                              # Add the old rule in the list of rules that must be removed from the grammar
                    simplified_grammar.production_rules.append(new_rule)        # Add the new rule to the grammar

    for rule in simplified_grammar.production_rules:                            # Search in all the production rules
        index = rule.find(">")
        right_of_production = rule[(index+2):]
        right_symbols = right_of_production.split(" ")                          # Each symbol of resulting production is in a list
        number_of_symbols = len(right_symbols)

        # If the production generates 3 or more symbols, the last two symbols will be transformed in an extra variable
        if number_of_symbols > 2:
            new_variable = "V{0}".format(extra_variables_v)
            simplified_grammar.variables.append(new_variable)                   # Add the new variable in the grammar
            new_rule = new_variable + " > " + right_symbols[number_of_symbols - 2] + " " + right_symbols[number_of_symbols - 1] # Creates the new rule
            must_delete_rules.append(rule)                                      # Add the old rule in the list of rules that must be removed from the grammar
            simplified_grammar.production_rules.append(new_rule)                # Add the new rule to the grammar
            new_rule = rule[:(index+2)]
            for i in range (0,(number_of_symbols - 2)):                         # The old rule now it will be "A > a Vx" | a ε V
                new_rule = new_rule + right_symbols[i] + " "
            new_rule = new_rule + new_variable
            simplified_grammar.production_rules.append(new_rule)                # Add the new rule to the grammar
            extra_variables_v += 1                                              # Increases the index of the next variable

        # If the production generates 2 symbols, and at least one of them is a terminal, it replaces it with the Variable that generates only that terminal
        if number_of_symbols == 2:                                              # If a production with 2 symbols in the right has a terminal,
            for terminal in simplified_grammar.terminals:                       # this Variable will be replaced by the variable "C" with the index of the terminal
                if terminal == right_symbols[0]:                                # If the terminal is in the first symbol
                    new_rule = rule[:(index + 2)] + "C" + terminal + " " + right_symbols[1] # Creates the new rule
                    must_delete_rules.append(rule)                              # Add the old rule in the list of rules that must be removed from the grammar
                    simplified_grammar.production_rules.append(new_rule)        # Add the new rule to the grammar
                if terminal == right_symbols[1]:                                # If the terminal is in the second symbol
                    new_rule = rule[:(index + 2)] + right_symbols[0] + " " + "C" + terminal # Creates the new rule
                    must_delete_rules.append(rule)                              # Add the old rule in the list of rules that must be removed from the grammar
                    simplified_grammar.production_rules.append(new_rule)        # Add the new rule to the grammar
            if right_symbols[0] in simplified_grammar.terminals and right_symbols[1] in simplified_grammar.terminals: # If there are two temrinals in the production
                new_rule = rule[:(index + 2)] + "C" + right_symbols[0] + " " + "C" + right_symbols[1] # Creates the new rule
                must_delete_rules.append(rule)                                  # Add the old rule in the list of rules that must be removed from the grammar
                simplified_grammar.production_rules.append(new_rule)            # Add the new rule to the grammar

    for rule in must_delete_rules:
        simplified_grammar.production_rules.remove(rule)                        # Removes from the grammar the rules of must_delete_rules' list

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
Main
"""

delete_empty_productions()
print(" \nNew production rules after the exclusions of the empty productions:")
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

chomsky_normal_form()
# The useless symbols algorithm will be running again in the code just in case that if there's a grammar that is already in the normal form before the normal form algorithm.
# This is because the normal form process can create useless symbols and productions, and the useless symbols algorithm do not alterate the normal form one.
delete_useless_symbols()
print("\n This is the new grammar after the Chomsky normal form process:\n")
print(" G'' = (V'', T'', P'', S)\n")
print(" Where\n")
print(" V'' is all the variable symbols in the normal form grammar:")
print("  V'' = {"+ ", ".join(variable for variable in simplified_grammar.variables) + "}")
print(" T'' is all the terminal symbols in the normal form grammar:")
print("  T'' = {"+ ", ".join(terminal for terminal in simplified_grammar.terminals) + "}")
print(" P'' is all the production rules in the normal form grammar:")
print("  P'' = { " + ",\n        ".join(production for production in simplified_grammar.production_rules) + " }")
print(" S is the initial variable symbol in the normal form grammar:")
print("  S = " + simplified_grammar.initial_symbol)
