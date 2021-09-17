# -*- coding: utf-8 -*-
"""
Defines the Theorem and Equality classes.

The Equality class inherits from the Theorem one, which may sound silly since
there is no other class inheriting the Theorem class and the latter is
never used on its own. This was just done to show the opening of this program
to other kind of proofs (even direct proofs), such as implications (with
if and only if's).

Created on Fri Apr 16 18:31:01 2021
@author: Joachim Favre & Alberts Reisons
"""
import text_gestion as tg


NOT_RIGHT_NUMBER_PARAMETERS_MESSAGE = ("You did not give the right number of "
                                       "parameters. This theorem expected {} "
                                       "parameters and you gave {}. Do not "
                                       "forget to give them as a list, even "
                                       "if you only give one parameter.")


NOT_A_NUMBER_MESSAGE = ("You did not give a number when it was expected for a "
                        "simplification.")

PROOF_NOT_FINISHED_MESSAGE = ("You gave to a theorem a proof which was "
                              "not finished. Do not forget to call "
                              "proof.conclude().")

BAD_OPERATION_ORDER_IN_REPLACEMENT_MESSAGE = ("You tried to replace an unkown "
                                              "by something which had a too "
                                              "low operation priority. Do not "
                                              "hesitate to add parenthesis.")


EQUALITY_SIDE_NOT_OK_FOR_MATHS = ("A side of this equality does not make "
                                  "sense. Verify that you use the right "
                                  "characters.")


BAD_UNKNOWN_NAME = ("An unknown has a bad name. Their name must be "
                    "exactly one (upper case or lower case) letter.")


NON_EXISTING_UNKNOWN_MESSAGE = ("You are trying to use the unknown {}, which "
                                "was not listed in the unknown or the "
                                "simplifications of this theorem.")


THEOREM_RECURSION_MESSAGE = ("You are using a theorem A to prove a theorem B "
                             "and B to prove A (or you have a huge depth of "
                             "theorem using other theorems for their proof; "
                             "in that case, you may want to consider to "
                             "increase the recursion depth). You cannot do "
                             "that, that's illegal!")


class NotRightNumberOfParametersError(Exception):
    """
    An exception that is thrown when a theorem did not get enough parameters
    in its param_list.
    """

    def __init__(self, required_number, given_number):
        message = NOT_RIGHT_NUMBER_PARAMETERS_MESSAGE
        message = message.format(required_number, given_number)
        super().__init__(message)


class NotANumberError(Exception):
    """
    An exception that is thrown when the program was expecting a number in
    order to make a simplification, but it was given an unknown.
    """

    def __init__(self):
        super().__init__(NOT_A_NUMBER_MESSAGE)


class ProofNotFinishedError(Exception):
    """
    An exception that is thrown when a theorem's proof was not concluded. This
    means that it was not finished.
    """

    def __init__(self):
        super().__init__(PROOF_NOT_FINISHED_MESSAGE)


class BadOperationOrderInReplacementError(Exception):
    """
    An exception that is thrown when it could not make the modification
    the user gave because of a bad operation order when replacing an unknown.
    """

    def __init__(self):
        super().__init__(BAD_OPERATION_ORDER_IN_REPLACEMENT_MESSAGE)


class EqualitySideNotOkForMathsError(Exception):
    """
    An exception that is thrown when a side of an equality from a theorem
    does not make sense concerning maths.
    """

    def __init__(self):
        super().__init__(EQUALITY_SIDE_NOT_OK_FOR_MATHS)


class BadUnknownNameError(Exception):
    """
    An exception that is thrown when an unknown does not have a correct name,
    that is it is not one letter long.
    """

    def __init__(self):
        super().__init__(BAD_UNKNOWN_NAME)


class NonExistingUnknownError(Exception):
    """
    An exception that is thrown when the user wants to use an unknown
    which is not defined in the theorem.
    """

    def __init__(self, unknown):
        message = NON_EXISTING_UNKNOWN_MESSAGE
        message = message.format(unknown)
        super().__init__(message)


class TheoremRecursionError(Exception):
    """
    An exception that is thrown after max recursion depth has been reached.
    It is very probable that it comes from the user trying to prove
    theorem A with theorem B and B with A.
    """

    def __init__(self):
        super().__init__(THEOREM_RECURSION_MESSAGE)


class Theorem():
    """
    Theorem "abstract" class. As mentioned in the main docstring, it is not
    merged with the Equality class to show an opening with an Implication
    class.

    Attributes
    **********
    - name: the name of this theorem. It is used for LaTeX code generation.
    - conclusion: the conclusion of this theorem; what it says.
    - unknowns: the unknowns of this theorem.
    - simplifications: the simplification that must be done mathematically
                       (such c = 1 + 2) for this theorem. They are under the
                       form of list of lists: [[name, expression], ...]
    """

    def __init__(self, name=None, conclusion=None, unknowns=None,
                 simplifications=None):
        """
        Constructor method of the Theorem class. Instanciates attributes
        and verifies that they make sense.
        """
        if name is None:
            name = "[undefined theorem name]"
        self.name = name

        if conclusion is None:
            conclusion = ""
        self.conclusion = conclusion

        if unknowns is None:
            unknowns = []
        else:
            for unknown in unknowns:
                if len(unknown) != 1 or not tg.is_letter(unknown):
                    raise BadUnknownNameError

        self.unknowns = unknowns

        if simplifications is None:
            simplifications = []
        else:
            for simpl_name, _ in simplifications:
                if len(simpl_name) != 1 or not tg.is_letter(simpl_name):
                    raise BadUnknownNameError

        simpl_no_space = []
        for simplification in simplifications:
            simplification[1] = tg.remove_spaces(simplification[1])
            simpl_no_space.append(simplification)
        self.simplifications = simpl_no_space

        self.verify_has_instantiated_every_character(conclusion)

        try:
            # It is normal to get a None from this proof.
            # This is not an error...
            self.proof = self.get_proof()
        except RecursionError:
            raise TheoremRecursionError

    def get_proof(self):
        """
        "Virtual" method that need to be redefined by children that are not
        axioms and which have a proof. This must then return their proof.
        """
        # The self needs to be here...
        return None

    def is_proven(self):
        """
        Returns whether this theorem is proven.
        """
        return self.is_axiom() or self.proof.is_finished

    def is_axiom(self):
        """
        Returns whether this theorem is actually an axiom (it has no proof).
        """
        return self.proof is None

    def has_instantiated_character(self, character):
        """
        Returns whether this character makes sense in the context of this
        theorem; whether it is in the unknowns or the simplifications.
        """
        if character in self.unknowns:
            return True
        for simplification in self.simplifications:
            if simplification[0] == character:
                return True
        return False

    def verify_has_instantiated_every_character(self, expression):
        """
        Returns whether every character from this expression makes sense in
        the context of this theorem; whether it is in the unknowns or the
        simplifications.
        """
        for character in tg.extract_unknowns(expression):
            if not self.has_instantiated_character(character):
                raise NonExistingUnknownError(character)


class Equality(Theorem):
    """
    Equality "abstract" class, which inherits from the Theorem class. As
    mentioned in the main docstring, it is not merged with the Theorem class
    to show an opening with an Implication class.

    Attributes (not inherited from Theorem)
    ***************************************
    - left_hand_side: left hand side of the conclusion
    - right_hand_side: right hand side of the conclusion
    """

    def __init__(self, param_list=None, name=None, conclusion=None,
                 unknowns=None, simplifications=None):
        """
        Constructor of the Equality class. Instanciates attributes, and
        makes the right replacements using the parm_list.
        """
        super().__init__(name, conclusion, unknowns, simplifications)

        if param_list is None:
            param_list = ['0']*len(self.unknowns)
        elif len(self.unknowns) != len(param_list):
            raise NotRightNumberOfParametersError(len(self.unknowns),
                                                  len(param_list))

        lhs, rhs = self.conclusion.split('=')
        lhs = tg.remove_spaces(lhs)
        rhs = tg.remove_spaces(rhs)

        if not (tg.verify_maths(lhs) and tg.verify_maths(rhs)):
            raise EqualitySideNotOkForMathsError

        if param_list is None:
            if len(self.simplifications) != 0:
                raise NotANumberError
        else:
            replacement_dictionary = {}
            for unknown, param in zip(self.unknowns, param_list):
                replacement_dictionary[unknown] = tg.remove_spaces(param)

            for simplification in self.simplifications:
                unknown, equality = simplification
                equality = tg.replace_using_dict(equality,
                                                 replacement_dictionary)
                try:
                    evaluation = tg.evaluate_expression(equality)
                    replacement_dictionary[unknown] = str(evaluation)
                except NameError:
                    raise NotANumberError

            lhs = tg.replace_using_dict(lhs, replacement_dictionary)
            rhs = tg.replace_using_dict(rhs, replacement_dictionary)

            for side in [lhs, rhs]:
                for key in replacement_dictionary:
                    replaced_by = replacement_dictionary[key]
                    side_splitted = side.split(replaced_by)
                    for index in range(len(side_splitted) - 1):
                        left = side_splitted[index]

                        if index == len(side_splitted) - 1:
                            right = ""
                        else:
                            right = side_splitted[index + 1]

                        if not tg.verify_order_operation(left, replaced_by,
                                                         right):
                            raise BadOperationOrderInReplacementError

        self.left_hand_side = lhs
        self.right_hand_side = rhs

        if not (tg.verify_maths(lhs) and tg.verify_maths(rhs)):
            raise EqualitySideNotOkForMathsError

    def is_held(self, equality):
        """
        Verifies if an equality is held. This uses the left_hand_side and
        right_hand_side attributes.
        """
        splitted_equality = equality.split('=')
        if len(splitted_equality) != 2:
            return False

        lhs = self.left_hand_side
        rhs = self.right_hand_side
        return lhs in splitted_equality and rhs in splitted_equality
