# -*- coding: utf-8 -*-
"""
List of synonyms.

Different synonyms for the LaTeX code generation, for it to be less brutal.

Created on Wed May  5 19:20:08 2021
@author: Joachim Favre & Alberts Reisons
"""

# Pure synonyms
ASSUME = ["assume {}",
          "assume {} to be true",
          "assume that {} is true",
          "suppose {}",
          "suppose {} to be true",
          "suppose that {} is true",
          "take {} as an axiom"]


FOLLOWING_EQUALITY = ["the following equality",
                      "the following affirmation",
                      "the following proposition",
                      "this equality",
                      "this affirmation",
                      "this proposition"]

WANT_TO_SHOW = ["want to prove",
                "aim to prove",
                "want to show",
                "aim to show",
                "are trying to prove",
                "are trying to show",
                "are aiming to prove",
                "are aiming to show"]

START_WITH = ["start with",
              "begin with",
              "take this as a beginning point",
              "take this as a starting point"]

BY = ["By",
      "According to",
      "Using",
      "From"]

HAVE_THAT = ["have that",
             "have",
             "get that",
             "get",
             "know that"]

THEREFORE_BEGIN_SENTENCE = ["Therefore,",
                            "Thus,",
                            "This means that:",
                            "This allows us to infer that:"]

WHICH = ["Which",
         "This proof"]

THEREFORE_MID_SENTENCE = ["therefore ",
                          "thus ",
                          ""]

ALLOWS_TO_CONCLUDE = ["allows us to conclude",
                      "allows us to be convinced",
                      "makes us sure"]


# Used in LaTeX code generation:
AXIOM_INTRO = ["We " + assume.format(following_equality) + ":"
               for assume in ASSUME
               for following_equality in FOLLOWING_EQUALITY]


TRYING_TO_SHOW = ["We " + want_to_show + " " + following_equality + ":"
                  for want_to_show in WANT_TO_SHOW
                  for following_equality in FOLLOWING_EQUALITY + ["that"]]


LET_US_START_WITH = ["Starting with the following expression:",
                     "We will begin our proof with the following expression:",
                     "We will start our proof with the following expression:",
                     "We can start with:",
                     "We can begin with:",
                     "The following expression can be our starting point:",
                     'Let us start with:',
                     'Let us begin with:',
                     'Let us take this as a starting point:',
                     "A friend of mine told me to start with:"]

BY_HAVE_THAT = [by + " {} (section {}), we " + have_that
                for by in BY
                for have_that in HAVE_THAT]

BY_HAVE_THAT_THEREFORE = [by + " {} (section {}), we " + have_that
                          + " ${}$. " + therefore
                          for by in BY
                          for have_that in HAVE_THAT
                          for therefore in THEREFORE_BEGIN_SENTENCE]

CONCLUSION = [which + " " + therefore + allows_to_conclude + that + ":"
              for which in WHICH
              for therefore in THEREFORE_MID_SENTENCE
              for allows_to_conclude in ALLOWS_TO_CONCLUDE
              for that in [" that", ""]]
