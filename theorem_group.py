# -*- coding: utf-8 -*-
"""
Defines the TheoremGroup class.

Defines the TheoremGroup class, that allows to group different theorems
to make compile them in one LaTeX file. This uses randomness for synonyms,
so do not hesitate to fix random.seed(number) to always get the same result.

Created on Mon May  3 21:25:18 2021
@author: Joachim Favre & Alberts Reisons
"""
import random as rng

import sys
import inspect

import latex_gestion as tex
import text_gestion as tg
import theorem as thm
import theorem_set as thmset

import synonyms


PROOF_NOT_FINISHED_MESSAGE = ("You are trying to add a theorem which proof "
                              "was not finished.")


class ProofNotFinishedError(Exception):
    """
    An exception that is thrown when the user is trying to add a theorem which
    proof is not finished to a TheoremGroup object.
    """

    def __init__(self):
        super().__init__(PROOF_NOT_FINISHED_MESSAGE)


class TheoremGroup:
    """
    A class that allows the user to group different theorems (or axiom)
    together, in order to save them in a document.

    When adding a theorem, it also adds all its dependencies (axioms and
    theorems).

    This class uses some randomness to have synonyms in the proof. Do not
    hesitate to use random.see(number) to set the see and always have
    the same result.

    Attributes
    **********
    - title: the title of the generated LaTeX document
    - author: the author of the generated LaTeX document
    - already_saved: a list of Theorem class name which have already been
                     saved.
    - axioms_latex: the LaTeX code of the axioms. It is splitted from the
                    theorems to have two distinct parts in the generated
                    document.
    - theorems_latex: the LaTeX code of the theorems. It is splitted from the
                      axioms to have two distinct parts in the generated
                      document.
    """

    def __init__(self, title, author=r"Joachim Favre \& Alberts Reisons"):
        """
        Instanciates the attributes of this object.
        """
        self.title = title
        self.author = author
        self.already_saved = []
        self.axioms_latex = ""
        self.theorems_latex = ""

    def add_theorem(self, theorem):
        """
        Adds a theorem to this list of theorem. If it has dependencies,
        also adds its dependecies, and writes the right LaTeX code accordingly.
        """
        if isinstance(theorem, type):
            theorem = theorem(None)

        if not theorem.is_proven():
            raise ProofNotFinishedError

        if type(theorem) in self.already_saved:
            return
        self.already_saved.append(type(theorem))
        number_already_saved = len(self.already_saved)

        if not theorem.is_axiom():
            for dependency in theorem.proof.dependencies:
                self.add_theorem(dependency)

        if theorem.is_axiom():
            colour = r""
        else:
            colour = r""

        latex_code = ("\n\n"
                      + r"\section{" + colour
                      + tg.upper_case_first_letter(theorem.name)
                      + r"\label{"
                      + str(number_already_saved - 1)
                      + "}}\n")

        goal = tex.convert_2_latex(theorem.conclusion)
        if theorem.is_axiom():
            latex_code += (rng.choice(synonyms.AXIOM_INTRO) + "\n"
                           + r"\[" + goal + r"\]" + "\n")
        else:
            latex_code += (r"\subsection{Theorem}" + "\n"
                           + rng.choice(synonyms.TRYING_TO_SHOW) + "\n"
                           + r"\[" + goal + r"\]" + "\n")

        number_unknowns = len(theorem.unknowns)
        number_simp = len(theorem.simplifications)
        if number_unknowns > 0:

            unknowns = [tex.convert_2_latex(unknown)
                        for unknown in theorem.unknowns]
            latex_code += ("with " +
                           tex.write_as_list(unknowns)
                           + " being unknown ")

            if isinstance(theorem, thmset.RemovalOfParenthesis):
                latex_code += "or known"
            else:
                latex_code += "(or known)"

            if number_simp > 0:
                latex_code += ", and "
            else:
                latex_code += "."

        if number_simp > 0:
            simps = [tex.convert_2_latex(equality[0] + "=" + equality[1])
                     for equality in theorem.simplifications]
            latex_code += ("with "
                           + tex.write_as_list(simps)
                           + " getting simplified ")
            if number_simp > 1:
                latex_code += "(as numbers)."
            else:
                latex_code += "(as a number)."

        if not theorem.is_axiom():
            proof_latex = theorem.proof.latex_code
            for dependency in theorem.proof.dependencies:
                label_number = self.already_saved.index(type(dependency))
                ref_call = r"\ref{" + str(label_number) + "}"
                proof_latex = proof_latex.replace("{}", ref_call, 1)
            latex_code += (r"\subsection{Proof}" + "\n"
                           + proof_latex)

        latex_code += "\n"
        if theorem.is_axiom():
            self.axioms_latex += latex_code
        else:
            self.theorems_latex += latex_code

    def add_all_theorems(self, module):
        """
        Adds all the theorems from a python module. This is a good way to be
        sure that every theorem has been taken; however, it is recommended to
        give some guidlines to the TheoremGroup when saving theorems, to have
        some kind of structure in the document.
        """
        for _, obj in inspect.getmembers(sys.modules[module.__name__]):
            if inspect.isclass(obj):
                if issubclass(obj, thm.Theorem):
                    self.add_theorem(obj)

    def save(self, file_name=None):
        """
        Uses the write_to_file() function present in latex_gestion.py.

        The file name must not have any file extension (no .pdf nor .tex). If
        no file name is specified, uses the proof title after replacing
        spaces by underscores.

        Note: there might be something happening if we try to save a document
              without any theorem nor axiom.
        """
        if file_name is None:
            file_name = self.title.replace(' ', '_')
        if len(file_name) > 4 and file_name[-4:] == '.tex':
            file_name = file_name[:-4]

        latex_code = tex.init_latex_code(self.title, self.author)
        if self.axioms_latex != "":
            latex_code += r"\part{Axioms}" + "\n"
            latex_code += self.axioms_latex
            latex_code += r"\newpage" + "\n\n"

        if self.theorems_latex != "":
            latex_code += r"\part{Theorems}"
            latex_code += self.theorems_latex

        if self.axioms_latex == self.theorems_latex == "":
            latex_code = tex.concatenate_lines([r"\documentclass{article}",
                                                r"\begin{document}",
                                                ""])
            latex_code += ("Since there is no proof to save, let me speak "
                           "about 1729, the Hardy-Ramanujan number. It "
                           "is clearly the greatest number.")
            latex_code += (r"\begin{center}"
                           + r"\textit{One number to rule them all,}\\"
                           + r"\textit{One number to find them,}\\"
                           + r"\textit{One number to bring them all}\\"
                           + r"\textit{And in the darkness bind them.}\\"
                           + r"\end{center}")

        tex.write_to_file(latex_code, file_name, True)
