# -*- coding: utf-8 -*-
"""
Gives function to modify strings.

CONSTANTS
*********
- OPERATION_ORDER: Give the order of operation for the defined operators.
- PARENTHESIS_ORDER: Gives how much parenthesis add to the order of operations.
- IMPOSSIBLE_CHARACTER: A sequence of chararacters that can never show up in a
                        mathematical expression. It is therefore safe to
                        use as a temporary expression.

Created on Fri Apr 16 18:30:42 2021
@author: Joachim Favre & Alberts Reisons
"""


OPERATION_ORDER = {'+': 0, '*': 1, '^': 2}
PARENTHESIS_ORDER = 3

IMPOSSIBLE_CHARACTER = "+#@=={}==@#+"


def full_concatenate(str_list):
    """
    Takes a list of string in parameters and returns the full concatenation
    of those strings.
    """
    result = ""
    for element in str_list:
        result += element
    return result


def remove_spaces(string):
    """
    Returns the string given in parameters without any spaces.
    """
    return string.replace(' ', '')


def split_list(str_list, splitter):
    """
    Splits strings in a list according to some splitter, and returns a list
    of strings containings those splits.
    """
    result = []
    for element in str_list:
        for split_element in element.split(splitter):
            result.append(split_element)
    return result


def compute_first_order_operation(expression, left_2_right=True):
    """
    Computes the order of operation of the first operator it meets in the
    expression given in parameters. We can also define whether we want
    to read the expression from left to right or from right to left.
    """
    augmenting_parenthesis = "("
    diminishing_parenthesis = ")"

    if not left_2_right:
        temp = augmenting_parenthesis
        augmenting_parenthesis = diminishing_parenthesis
        diminishing_parenthesis = temp
        expression = expression[::-1]

    order = 0
    for character in expression:
        if character == augmenting_parenthesis:
            order += PARENTHESIS_ORDER
        elif character == diminishing_parenthesis:
            order -= PARENTHESIS_ORDER
        elif character in OPERATION_ORDER:
            order += OPERATION_ORDER[character]
            break
    return order


def verify_order_operation(left, center, right):
    """
    Verifies that the "center" variable can be replaced (using a modification
    in a proof). The left and right parts are relative to the center, the
    modification. For example, we could have:
        left = "a +"
        middle = "b*c"
        right = "^d"
        (complete expression = "a + b*c^d")
    Which would False, since we cannot safely replace b*c by something else,
    because of the ^d.
    """
    if (len(center) == 1 or (center[0] == "(" and center[-1] == ")")
            or (left != "" != right and left[-1] == "(" and right[0] == ")")):
        return True

    # closest_order_left = compute_first_order_operation(left, False)
    if left == "":
        closest_order_left = 0
    else:
        operator = remove_spaces(left)[-1]
        if operator != "(":
            try:
                closest_order_left = OPERATION_ORDER[operator]
                closest_order_left_c = compute_first_order_operation(
                    center, True)
                if closest_order_left_c < closest_order_left:
                    return False
            except KeyError:
                return False

    if right == "":
        closest_order_right = 0
    else:
        operator = remove_spaces(right)[0]
        if operator != ")":
            try:
                closest_order_right = OPERATION_ORDER[operator]
                closest_order_right_c = compute_first_order_operation(
                    center, False)
                if closest_order_right_c < closest_order_right:
                    return False
            except KeyError:
                return False

    return True


def only_one_modification(old_statement, new_statement, modification):
    """
    Verifies that there was only one modification from the old statement
    to the new one. The modification it verifies is the one given in
    parameters. Also verifies if the modification can be done according
    to a basic test with order of operations.
    This only works for equalities.
    """
    modification = modification.split('=')
    if len(modification) != 2:
        return False

    possibilities = old_statement.count(modification[0])

    for possibility in range(possibilities):
        formatted_old_stmt = old_statement.replace(modification[0], '{}')

        modifications = [modification[0]]*(possibilities - 1)
        modifications.insert(possibility, modification[1])

        if formatted_old_stmt.format(*modifications) == new_statement:
            modifications = [modification[0]]*(possibilities - 1)
            modifications.insert(possibility, IMPOSSIBLE_CHARACTER)

            formatted_old_stmt = formatted_old_stmt.format(*modifications)
            lhs, rhs = formatted_old_stmt.split(IMPOSSIBLE_CHARACTER)

            return verify_order_operation(lhs, modification[1], rhs)
    return False


def replace_using_dict(string, replacement_dictionary):
    """
    Replaces a string using a replacement dictionary. For example,
    "a + b = 7" with {"a": "x", "b": y} becomes "x + y = 7".
    Does a temporary step in order to be careful with dictionaries such
    as {'a': 'b', 'b': 'a'} (that switch values).
    """
    # we need to do a temporary step to be careful with a dictionary such as
    # {'a': 'b', 'b': 'a'}
    string_2_temp = {}
    temp_2_result = {}
    for index, key in enumerate(replacement_dictionary):
        result = replacement_dictionary[key]
        temp_key = IMPOSSIBLE_CHARACTER.format(index)
        string_2_temp[key] = temp_key
        temp_2_result[temp_key] = result

    # temp step
    for key in string_2_temp:
        replacement = string_2_temp[key]
        string = string.replace(key, replacement)

    # end step
    for key in temp_2_result:
        replacement = temp_2_result[key]
        string = string.replace(key, replacement)

    return string


def upper_case_first_letter(text):
    """
    Returns some text with the first letter upper-cased.
    """
    result = text[0].upper()
    result += text[1:]
    return result


def evaluate_expression(expression):
    """
    Evaluate a mathematical expression (such as 1+2). Pylint say that
    eval(expression) should be replaced by ast.literal_eval(expression), but
    this function does nto evaluate decimals.
    """
    expression = expression.replace('^', '**')
    # It is said that eval(expression) should be replaced by
    # ast.literal_eval(expression) ; however, it does not evaluate decimals.
    return eval(expression)


def is_number(character):
    """
    Returns whether the character is a number.
    [Note from like 6 months after having finished this code: I have learned
     that there exists a character.isdecimal() function. But hey! The try
     catch method is great! xD]
    """
    try:
        int(character)
        return True
    except ValueError:
        return False


def is_letter(character):
    """
    Returns whether the character is a letter.
    """
    is_smaller_case = ord('a') <= ord(character) <= ord('z')
    is_upper_case = ord('A') <= ord(character) <= ord('Z')
    return is_smaller_case or is_upper_case


def is_operator(character):
    """
    Returns whether the character is an operator (in other words, if it is
    in OPERATION_ORDER or if it is an "=" sign).
    """
    return character in OPERATION_ORDER or character == '='


def character_code(character):
    """
    Converts a character following the code hereinafter:
        - nothing -> 0
        - number -> 1
        - letter -> 2
        - operator -> 3
        - opening_parenthesis -> 4
        - closing_parenthesis -> 5
    """
    if character == '':
        return 0
    if is_number(character):
        return 1
    if is_letter(character):
        return 2
    if is_operator(character):
        return 3
    if character == "(":
        return 4
    if character == ")":
        return 5
    return None


def verify_maths(expression):
    """
    Verifies that an expression makes sense mathematically speaking. It
    looks at two characters following each others, and defines whether it
    makes sense or not using a matrix. It also verifies if there is the
    same number of opening parenthesis as closing ones. Make sure
    to use this function on both sides of an equality to avoid things such as:
        (a + b = c) * d
    """

    if expression.count('(') != expression.count(')'):
        return False

    # allowed[a, b] : a -> last character / b -> new character
    # indices using character_code
    # "empty" = beginning / end of expression
    allowed = [[True,  True,  True,  False, True,  False],
               [True,  True,  False, True,  False, True],
               [True,  False, False, True,  False, True],
               [False, True,  True,  False, True,  False],
               [False, True,  True,  False, True,  False],
               [True,  False, False, True,  False, True]]

    last_character = 0

    for character in remove_spaces(expression):
        character = character_code(character)
        if character is None:
            return False
        if not allowed[last_character][character]:
            return False
        last_character = character

    # Can finish on this character ?
    return allowed[last_character][0]


def extract_unknowns(expression):
    """
    Extracts the unknowns from an expression.
    """
    unknowns = []
    for character in remove_spaces(expression):
        if is_letter(character) and character not in unknowns:
            unknowns.append(character)
    return unknowns
