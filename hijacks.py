# -*- coding: utf-8 -*-
"""
Shows some attacks that can be done against this program.

The different Hijacks were attacks to which we defended. This program is surely
vulnerable to many possible attacks, but not these ones.

Created on Wed May  5 18:02:12 2021
@author: Joachim Favre & Alberts Reisons
"""
import theorem_set as thmset
import theorem as thm
from proof import Proof


class Hijack1(thm.Equality):
    """
    (False) theorem that states that a + b^2 = a + b*a + b.
    The order of the unknowns is the following: a, b.

    It tries to use the fact that the order of operations may not be defined.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="hijack 1",
                         conclusion="a + b^2 = a + b*a + b",
                         unknowns=['a', 'b'])

    def get_proof(self):
        proof = Proof(self, 'a + b^2')

        proof.evolve_equality('a + b*a + b',
                              "a + b^2 = a + b*a + b",
                              thmset.SquareDistribution(['a + b']))

        proof.conclude()

        return proof


class Hijack2(thm.Equality):
    """
    (False) theorem that states that 2*x + 3*x^2 = 5*x^2.
    The order of the unknowns is the following: x.

    It tries to use the fact that the order of operations may not be defined.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="hijack 2",
                         conclusion="2*x + 3*x^2 = 5*x^2",
                         unknowns=['x'])

    def get_proof(self):
        proof = Proof(self, '2*x + 3*x^2')

        proof.evolve_equality('5*x^2',
                              '2*x + 3*x = 5*x',
                              thmset.LitteralAddition(['2', '3', 'x']))

        proof.conclude()

        return proof


class Hijack3(thm.Equality):
    """
    (False) theorem that states that (a + b)^2 = a + b^2.
    The order of the unknowns is the following: a, b.

    It tries to use the fact that the order of operations may not be defined.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="hijack 3",
                         conclusion="(a + b)^2 = a + b^2",
                         unknowns=['a', 'b'])

    def get_proof(self):
        proof = Proof(self, '(a + b)^2')

        proof.evolve_equality('a + b^2',
                              '(a+b) = a + b',
                              thmset.RemovalOfParenthesis(['a+b']))

        proof.conclude()

        return proof


class Hijack4(thm.Equality):
    """
    (False) theorem that states that a^2 = a.
    The order of the unknowns is the following: a, b.

    It tries to use the fact that it may be able to use another theorem to
    prove itself, while the other theorem uses this one for its proof. This
    other theorem is Hijack4Bis.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="hijack 4",
                         conclusion="a^2 = a",
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a^2')

        proof.evolve_equality('a',
                              'a^2 = a',
                              Hijack4Bis(['a']))

        proof.conclude()

        return proof


class Hijack4Bis(thm.Equality):
    """
    (False) theorem that states that a^2 = a.
    The order of the unknowns is the following: a, b.

    It tries to use the fact that it may be able to use another theorem to
    prove itself, while the other theorem uses this one for its proof. This
    other theorem is Hijack4.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="hijack 4 bis",
                         conclusion="a^2 = a",
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a^2')

        proof.evolve_equality('a',
                              'a^2 = a',
                              Hijack4(['a']))

        proof.conclude()

        return proof
