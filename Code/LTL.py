# E/φ: emtpy set
# N/¬: not
# A/∧: and
# O/∨: or
# X/◦: next
# U/𝒰: until
# R/𝓡: release

# W/•: weak next
# F/◇: finally/eventually
# G/□: globallly/always

import re

def simplify_symbols_LTL(LTL):
    replacement_dictionary = {"φ":"E", "¬":"N", "∧":"A", "∨":"O", "◦":"X", "𝒰":"U", "•":"W", "𝓡":"R", "◇":"F", "□":"G"}

    for key in replacement_dictionary:
        LTL = re.sub(fr'(?<! ){key}(?! )', f' {replacement_dictionary[key]} ', LTL)
    
    return LTL


def LTL_remove_non_base_symbols(LTL):
    # Remove weak next
    LTL = re.sub('W', 'N X N', LTL)

    # Remove eventually
    LTL = re.sub('F', 'true U')

    # Remove globally
    LTL = re.sub('G', 'false R')

    return LTL

def LTL_to_LDL(LTL):

    # Rule 1
    LTL = re.sub(r'tr\((.*?)\)', r'<\1>tt', LTL)

    # Rule 2
    LTL = re.sub(r'tr\((\w+) (\d+)\)', r'\1 tr(\2)', LTL)

    # Rule 3
    LTL = re.sub(r'tr\(([^)]+) A ([^)]+)\)', r'tr(\1) A tr(\2)', LTL)

    # Rule 4
    LTL = re.sub(r'tr\(([^)]+) O ([^)]+)\)', r'tr(\1) O tr(\2)', LTL)

    
    return False