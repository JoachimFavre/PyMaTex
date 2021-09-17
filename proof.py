# -*- coding: utf-8 -*-
"""
Gives the Proof class.

Created on Fri Apr 16 18:29:36 2021
@author: Joachim Favre & Alberts Reisons
"""
import random as rng

import text_gestion as tg
import latex_gestion as tex
import synonyms


MODIFICATION_NOT_VALID_MESSAGE = ("The parameters given to the theorem may "
                                  "not be the one you should have given, or "
                                  "maybe your modification does not hold "
                                  "according to this theorem.")

WRONG_MODIFICATION_MESSAGE = ("The modification you just gave is not valid. "
                              "This means that it holds, but that it cannot "
                              "be applied to this statement id or that it "
                              "could not be placed in the equality because "
                              "of the order of operations.")

FALSE_THEOREM_MESSAGE = ("The theorem you are trying to use is not proven. "
                         "This means that it has a proof, but that it was not "
                         "concluded. Do not forget to use proof.conclude().")

WRONG_SIMPLIFICATION_MESSAGE = ("The simplification you want to use is not "
                                "valid. It may not be registered in the "
                                "theorem, it may make no sense, or it may not "
                                "be appliable to any other equality so "
                                "that we get the new one.")

CANNOT_CONCLUDE_MESSAGE = "This proof could not get concluded."


class ModificationNotValidError(Exception):
    """
    An exception that is thrown when the modification cannot be verified
    by the theorem given.
    """

    def __init__(self):
        """
        Calls its super-constructor to display {MODIFICATION_NOT_VALID_MESSAGE}
        """
        super().__init__(MODIFICATION_NOT_VALID_MESSAGE)


class WrongModificationError(Exception):
    """
    An exception that is thrown when the modification works with the theorem
    given, but does not allow to go from an old equality to the new one.
    """

    def __init__(self):
        """
        Calls its super-constructor to display {WRONG_MODIFICATION_MESSAGE}
        """
        super().__init__(WRONG_MODIFICATION_MESSAGE)


class TheoremNotPovenError(Exception):
    """
    An exception that is thrown when the theorem used is not proven.
    """

    def __init__(self):
        """
        Calls its super-constructor to display {FALSE_THEOREM_MESSAGE}
        """
        super().__init__(FALSE_THEOREM_MESSAGE)


class WrongSimplificationError(Exception):
    """
    An exception that is thrown when the simplification could not be used
    to go to the new equality.
    """

    def __init__(self):
        super().__init__(WRONG_SIMPLIFICATION_MESSAGE)


class CannotConcludeError(Exception):
    """
    An exception that is thrown when one tried to conclude a proof, and that
    the program could not find both sides of the conclusion in the equality.
    """

    def __init__(self):
        super().__init__(CANNOT_CONCLUDE_MESSAGE)


class Proof():
    """
    Proof class. This is what is used to prove the theorem we want. It only
    supports equalities.

    Attributes
    **********
    - theorem: the theorem it tries to prove.
    - conclusion_aim: the goal of this proof. It used to verify that we can
                      conclude this proof when the user asks to do it.
    - equalities: a list of mathematical expressions that are equal.
    - is_finished: specifies whether this proofs was finished by calling
                   the conclude() method.
    - dependencies: instance of theorems in the order this proof uses them.
                    This is latter used to make reference throughout the
                    LaTeX code, between theorems.
    - latex_code: a string containing the LaTeX code of this proof.
    """

    def __init__(self, theorem, starting_equality):
        """
        Instanciates the attributes and starts the LaTeX code.
        """
        self.theorem = theorem
        self.conclusion_aim = tg.remove_spaces(theorem.conclusion).split('=')

        self.equalities = []
        self.is_finished = False
        self.dependencies = []  # theorems instance in order used

        self.latex_code = ""
        if len(theorem.unknowns) > 0:
            unknowns = [tex.convert_2_latex(unknown)
                        for unknown in theorem.unknowns]
            self.latex_code += ("Let " + tex.write_as_list(unknowns)
                                + " be unknown (or known). ")

        if len(theorem.simplifications) > 0:
            simplifications = [tex.convert_2_latex(equality[0]
                                                   + "=" + equality[1])
                               for equality in theorem.simplifications]
            self.latex_code += ("Let "
                                + tex.write_as_list(simplifications)
                                + " be ")
            if len(theorem.simplifications) > 1:
                self.latex_code += "simplifications (as numbers). "
            else:
                self.latex_code += "a simplification (as a number). "

        # Manage starting_equality
        starting_equality = tg.remove_spaces(starting_equality)
        self.theorem.verify_has_instantiated_every_character(starting_equality)

        self.equalities = [starting_equality]
        self.latex_code += rng.choice(synonyms.LET_US_START_WITH) + "\n"
        line = r"\[{}\]".format(tex.convert_2_latex(starting_equality))
        self.latex_code += line + "\n\n"

    def find_old_equality(self, new_equality, modif):
        """
        Finds the equality from which the user started to get to the new one;
        using the modification he or she gives. Returns None if none is found.
        """
        for old_equ_candidate in self.equalities:
            if tg.only_one_modification(old_equ_candidate, new_equality,
                                        modif):
                return old_equ_candidate
        return None

    def evolve_equality(self, new_equality, modif, theorem):
        """
        Makes the equality evolve evolve. It uses new_equality and modif (the
        modification done in order to get to the new equality) in order to
        find the old equality that was used to get to the new one.

        It thus verifies whether modif is allowed according to the theorem
        given (using the theorem.is_held() method) and whether there indeed
        was a old equality such that, after applying the modification, we get
        to the new one.

        Finally, it has some verifications concerning the order of operations.

        When it has all verified, it stores this step in LaTeX.
        """
        new_equality = tg.remove_spaces(new_equality)
        modif = tg.remove_spaces(modif)

        if not theorem.is_proven():
            raise TheoremNotPovenError

        if not theorem.is_held(modif):
            raise ModificationNotValidError

        self.theorem.verify_has_instantiated_every_character(new_equality)
        self.theorem.verify_has_instantiated_every_character(modif)

        old_equality = self.find_old_equality(new_equality, modif)
        if old_equality is None:
            raise WrongModificationError

        # equality is ok
        self.dependencies.append(theorem)
        self.equalities.append(new_equality)

        entire_line = old_equality + "=" + new_equality
        if modif == entire_line:
            line = rng.choice(synonyms.BY_HAVE_THAT)
        else:
            line = rng.choice(synonyms.BY_HAVE_THAT_THEREFORE)

        line = line.format(theorem.name,
                           "{" + "}",
                           tex.convert_2_latex(modif))
        self.latex_code += line + "\n"

        line = r"\[{}\]".format(tex.convert_2_latex(entire_line))
        self.latex_code += line + "\n\n"

    def use_simplification(self, new_equality, simplification):
        """
        Similarly to evolve_equality(), it makes the equality evolve. Instead
        of using a theorem, this uses a simplification stated in the theorem.
        """
        simplification = tg.remove_spaces(simplification)
        new_equality = tg.remove_spaces(new_equality)

        splitted_simplification = simplification.split('=')
        if len(splitted_simplification) != 2:
            raise WrongSimplificationError

        valid = False
        for possible_simplification in self.theorem.simplifications:
            lhs, rhs = possible_simplification
            if (lhs in splitted_simplification
                    and rhs in splitted_simplification):
                valid = True
                break

        if not valid:
            raise WrongSimplificationError

        old_equality = self.find_old_equality(new_equality, simplification)
        if old_equality is None:
            raise WrongSimplificationError

        # equality is ok
        self.equalities.append(new_equality)

        entire_line = old_equality + "=" + new_equality
        simplification = tex.convert_2_latex(simplification)
        self.latex_code += "We have let ${}$, so\n".format(simplification)
        self.latex_code += r"\[{}\]".format(tex.convert_2_latex(entire_line))
        self.latex_code += "\n\n"

    def conclude(self):
        """
        Verifies that this proof can be concluded and finished it. Adds
        some line of LaTeX for its conclusion. Throws an exception if it
        cannot conclude.
        """
        if self.is_finished:
            return

        conclusion_lhs, conclusion_rhs = self.conclusion_aim
        if (conclusion_lhs not in self.equalities
                or conclusion_rhs not in self.equalities):
            raise CannotConcludeError

        self.is_finished = True

        self.latex_code += rng.choice(synonyms.CONCLUSION) + "\n"
        left_hand_side = tex.convert_2_latex(self.conclusion_aim[0])
        right_hand_side = tex.convert_2_latex(self.conclusion_aim[1])
        self.latex_code += r"\[{} = {}\]".format(left_hand_side,
                                                 right_hand_side)
        self.latex_code += "\n"
        self.latex_code += tex.concatenate_lines([r"\begin{flushright}",
                                                 "QED",
                                                  r"\end{flushright}"])
