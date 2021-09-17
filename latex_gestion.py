# -*- coding: utf-8 -*-
"""
Gives functions related to LaTeX generation.

Created on Fri Apr 16 18:43:50 2021
@author: Joachim Favre & Alberts Reisons
"""
from datetime import datetime
import os

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

RESULT_DIRECTORY = "result"


def format_day(day_number):
    """
    Adds the good extension to a number to make the 'day' part of a date.
    """
    result = str(day_number)
    if result[-1] == '1' and day_number != 11:
        return result + "st"
    if result[-1] == '2' and day_number != 12:
        return result + "nd"
    if result[-1] == '3' and day_number != 13:
        return result + "rd"
    return result + "th"


def get_date():
    """
    Returns the current date, well formatted.
    """
    current_time = datetime.now()
    result = (format_day(current_time.day) + " " + MONTHS[current_time.month-1]
              + " " + str(current_time.year))
    return result


def concatenate_lines(lines):
    """
    Takes a list of lines (strings) in parameters and returns the full
    concatenation.
    Differs from full_concatenate(str_list) from text_gestion.py since it adds
    a carriage return at the end of each line. This function is thus more used
    for LaTeX code generation.
    """
    result = ""
    for line in lines:
        result += line + "\n"
    return result


def write_as_list(expression_list):
    """
    Takes a list of mathematical expressions and write it well formated (as
    "elem1, elem2, elem3, ..., elemn and elemem" (mostly for the comas and
    the "and" at the end)).
    """
    if len(expression_list) == 0:
        return ""
    result = "${}$"
    if len(expression_list) > 1:
        result += ", ${}$"*(len(expression_list) - 2)
        result += " and ${}$"
    result = result.format(*expression_list)
    return result


def convert_2_latex(text):
    """
    Takes some text that the user may have given and that is used by the
    program when verifying the proof, and replaces the right things by
    LaTeX commands. For example, '(' becomes '\\left('.
    """
    result = ""
    closing_bracket_in = []
    for index, character in enumerate(text):
        if character == "(":
            for index_bckt, how_many_left in enumerate(closing_bracket_in):
                closing_bracket_in[index_bckt] = how_many_left + 1
            result += "("
        elif character == ")":
            result += ")"
            for index_bckt, how_many_left in enumerate(closing_bracket_in):
                how_many_left -= 1
                closing_bracket_in[index_bckt] = how_many_left
                if how_many_left == 0:
                    closing_bracket_in.remove(0)  # only one can be at 0
                    result += "}"
        elif character == "*":
            try:
                int(text[index+1])
                result += "\\cdot"
            except ValueError:
                pass
        elif character == '^' and text[index+1] == "(":
            result += '^{'
            closing_bracket_in.append(0)
        else:
            result += character

    # result = result.replace("*", "\\cdot ")
    # result = result.replace("*", "")
    result = result.replace("(", "\\left(")
    result = result.replace(")", "\\right)")
    # result = result.replace("**", "^")

    return result


def init_latex_code(title, author):
    """
    Returns the header of a LaTeX file.
    """
    lines = [r"\documentclass[a4paper]{article}",
             r"\usepackage[T1]{fontenc}",
             r"\usepackage[utf8]{inputenc}",
             r"\usepackage[left=2.5cm, right=2.5cm, top=2.5cm, "
             "bottom=2.5cm]{geometry}",
             r"\usepackage[breaklinks, hidelinks]{hyperref}",
             r"\usepackage{xcolor}",
             r"\usepackage{titlesec}",
             r"\usepackage{tocloft}",
             r"\usepackage{fancyhdr}",
             r"\usepackage{ifthen}",
             "",
             r"\titleformat*{\section}{\large\bfseries}",
             r"\titleformat*{\subsection}{\normalsize\bfseries}",
             "",
             r"\setcounter{tocdepth}{1}",
             r"\renewcommand{\cftsecfont}{\normalfont}",
             r"\renewcommand{\cftsecpagefont}{\normalfont}",
             r"\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}",
             r"\setlength{\cftsecindent}{0.5cm}",
             r"\let\oldpart\part",
             r"\newcommand{\parttitle}{}",
             r"\renewcommand{\part}[1]{\oldpart{#1}"
             + r"\renewcommand{\parttitle}{#1}}",
             "",
             r"\pagestyle{fancy}",
             r"\lhead{\ifthenelse{\equal{\thepart}{}}{Contents}"
             + r"{Part \thepart~---~\parttitle}}",
             r"\rhead{" + author + "}",
             "",
             r"\title{" + title + "}",
             r"\author{" + author + "}",
             r"\date{" + get_date() + "}",
             "",
             r"\begin{document}",
             r"\maketitle",
             r"\tableofcontents",
             r"\newpage",
             ""]

    return concatenate_lines(lines)


def end_latex_code():
    """
    Returns the last necessary lines of a LaTeX file.
    """
    lines = ["",
             r"\end{document}"]
    return concatenate_lines(lines)


def write_to_file(latex_code, file_name, no_ending=False):
    """
    Writes some LaTeX code to a file at ./RESULT_DIRECTORY/{file_name} and
    compiles it. TThe no_ending parameter can be used to tell
    this function to add an ending to the latex_code, using end_latex_code().
    """
    if no_ending:
        latex_code += end_latex_code()

    result_path = RESULT_DIRECTORY + '/' + file_name

    with open(result_path + '.tex', 'w', encoding='utf-8') as file:
        file.write(latex_code)

    compil_cmd = ("pdflatex -output-directory "
                  + RESULT_DIRECTORY + " " + result_path + ".tex")

    print("Compiling the first time...")
    if os.system(compil_cmd) != 0:
        print("There was a problem during the first LaTeX compilation. Do "
              "not hesitate to take a look to the .log file to see what "
              "wnet wrong. You may have kept the pdf document opened, for "
              "example.")
        return

    print("Compiling the second time...")
    if os.system(compil_cmd) != 0:
        print("There was a problem during the second LaTeX compilation. Do "
              "not hesitate to take a look to the .log file to see what "
              "went wrong.")
        return
