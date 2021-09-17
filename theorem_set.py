"""
Set of theorems.

Define all the theorems and axioms that are verified and then written
in the LaTeX file.

Created on Wed May  5 14:35:12 2021
@author: Joachim Favre & Alberts Reisons
"""

import theorem as thm
from proof import Proof


class RemovalOfParenthesis(thm.Equality):
    """
    Axiom that states that (a) = a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the removal of parenthesis",
                         conclusion="(a) = a",
                         unknowns=['a'])


class AdditionCommutativity(thm.Equality):
    """
    Axiom that states that a + b = b + a.
    The order of the unknowns is the following: a, b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the commutativity of the addition",
                         conclusion='a + b = b + a',
                         unknowns=['a', 'b'])


class ProductCommutativity(thm.Equality):
    """
    Axiom that states that a*b = b*a.
    The order of the unknowns is the following: a, b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the commutativity of the product",
                         conclusion='a*b = b*a',
                         unknowns=['a', 'b'])


class LeftDistributivity(thm.Equality):
    """
    Axiom that states that a*(b + c) = a*b + a*c.
    The order of the unknowns is the following: a, b, c.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the left distributivity of the product",
                         conclusion='a*(b + c) = a*b + a*c',
                         unknowns=['a', 'b', 'c'])


class RightDistributivity(thm.Equality):
    """
    Theorem that states that (a + b)*c = a*c + b*c.
    The order of the unknowns is the following: a, b, c.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the right distributivity of the product",
                         conclusion='(a + b)*c = a*c + b*c',
                         unknowns=['a', 'b', 'c'])

    def get_proof(self):
        proof = Proof(self, '(a + b)*c')

        proof.evolve_equality('c*(a + b)',
                              '(a + b)*c = c*(a + b)',
                              ProductCommutativity(['(a+b)', 'c']))

        proof.evolve_equality('c*a + c*b',
                              'c*(a + b) = c*a + c*b',
                              LeftDistributivity(['c', 'a', 'b']))

        proof.evolve_equality('a*c + c*b',
                              'c*a = a*c',
                              ProductCommutativity(['c', 'a']))

        proof.evolve_equality('a*c + b*c',
                              'c*b = b*c',
                              ProductCommutativity(['b', 'c']))

        proof.conclude()

        return proof


class TripleLeftDistributivity(thm.Equality):
    """
    Theorem that states that a*(b + c + d) = a*b + a*c + a*d.
    The order of the unknowns is the following: a, b, c, d.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the triple left distributivity of the product",
                         conclusion='a*(b + c + d) = a*b + a*c + a*d',
                         unknowns=['a', 'b', 'c', 'd'])

    def get_proof(self):
        proof = Proof(self, 'a*(b + c + d)')

        proof.evolve_equality('a*(b + (c+d))',
                              'c + d = (c + d)',
                              RemovalOfParenthesis(['c + d']))

        proof.evolve_equality('a*b + a*(c+d)',
                              'a*(b + (c+d)) = a*b + a*(c+d)',
                              LeftDistributivity(['a', 'b', '(c+d)']))

        proof.evolve_equality('a*b + a*c + a*d',
                              'a*(c + d) = a*c + a*d',
                              LeftDistributivity(['a', 'c', 'd']))

        proof.conclude()

        return proof


class TripleRightDistributivity(thm.Equality):
    """
    Theorem that states that (a + b + c)*d = a*d + b*d + c*d.
    The order of the unknowns is the following: a, b, c, d.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the triple right distributivity of the product",
                         conclusion='(a + b + c)*d = a*d + b*d + c*d',
                         unknowns=['a', 'b', 'c', 'd'])

    def get_proof(self):
        proof = Proof(self, '(a + b + c)*d')

        proof.evolve_equality('d*(a + b + c)',
                              '(a + b + c)*d = d*(a + b + c)',
                              ProductCommutativity(['(a + b + c)', 'd']))

        proof.evolve_equality('d*a + d*b + d*c',
                              'd*(a + b + c) = d*a + d*b + d*c',
                              TripleLeftDistributivity(['d', 'a', 'b', 'c']))

        proof.evolve_equality('a*d + d*b + d*c',
                              'd*a = a*d',
                              ProductCommutativity(['d', 'a']))

        proof.evolve_equality('a*d + b*d + d*c',
                              'd*b = b*d',
                              ProductCommutativity(['d', 'b']))

        proof.evolve_equality('a*d + b*d + c*d',
                              'd*c = c*d',
                              ProductCommutativity(['d', 'c']))

        proof.conclude()

        return proof


class LitteralAddition(thm.Equality):
    """
    Theorem that states that a*x + b*x = c*x.
    The order of the unknowns is the following: a, b, x.
    The following simplification is applied: c = a + b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the litteral addition",
                         conclusion='a*x + b*x = c*x',
                         unknowns=['a', 'b', 'x'],
                         simplifications=[['c', 'a+b']])

    def get_proof(self):
        proof = Proof(self, 'a*x + b*x')

        proof.evolve_equality('(a+b)*x',
                              'a*x + b*x = (a+b)*x',
                              RightDistributivity(['a', 'b', 'x']))

        proof.use_simplification('(c)*x', 'a+b = c')

        proof.evolve_equality('c*x',
                              '(c) = c',
                              RemovalOfParenthesis('c'))

        proof.conclude()

        return proof


class LeftMultiplicationByIdentity(thm.Equality):
    """
    Axiom that states that 1*a = a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the left multiplication by the identity",
                         conclusion='1*a = a',
                         unknowns=['a'])


class RightMultiplicationByIdentity(thm.Equality):
    """
    Theorem that states that a*1 = a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the right multiplication by the identity",
                         conclusion='a*1 = a',
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a*1')

        proof.evolve_equality('1*a',
                              'a*1 = 1*a',
                              ProductCommutativity(['a', '1']))

        proof.evolve_equality('a',
                              '1*a = a',
                              LeftMultiplicationByIdentity(['a']))

        proof.conclude()

        return proof


class IdentityExponent(thm.Equality):
    """
    Axiom that states that a^1 = a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the identity exponent",
                         conclusion='a^1 = a',
                         unknowns=['a'])


class Addition(thm.Equality):
    """
    Theorem that states that a + b = c.
    The order of the unknowns is the following: a, b.
    The following simplification is applied: c = a + b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the addition",
                         conclusion='a + b = c',
                         unknowns=['a', 'b'],
                         simplifications=[['c', 'a + b']])

    def get_proof(self):
        proof = Proof(self, 'a+b')

        proof.use_simplification('c', 'a+b = c')

        proof.conclude()

        return proof


class Product(thm.Equality):
    """
    Theorem that states that a*b = c.
    The order of the unknowns is the following: a, b.
    The following simplification is applied: c = a*b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the product",
                         conclusion='a * b = c',
                         unknowns=['a', 'b'],
                         simplifications=[['c', 'a * b']])

    def get_proof(self):
        proof = Proof(self, 'a*b')

        proof.use_simplification('c', 'a*b = c')

        proof.conclude()

        return proof


class Power(thm.Equality):
    """
    Theorem that states that a^b = c.
    The order of the unknowns is the following: a, b.
    The following simplification is applied: c = a^b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the power",
                         conclusion='a^b = c',
                         unknowns=['a', 'b'],
                         simplifications=[['c', 'a^b']])

    def get_proof(self):
        proof = Proof(self, 'a^b')

        proof.use_simplification('c', 'a^b = c')

        proof.conclude()

        return proof


class PowerDistribution(thm.Equality):
    """
    Axiom that states that b^x * b^y = b^(x + y).
    The order of the unknowns is the following: b, x, y.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the power distribution",
                         conclusion="b^x * b^y = b^(x + y)",
                         unknowns=['b', 'x', 'y'])


class SquareDistribution(thm.Equality):
    """
    Theorem that states that a^2 = a*a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the distribution of the square",
                         conclusion='a^2 = a*a',
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a^2')

        proof.evolve_equality('a^(2)',
                              '2 = (2)',
                              RemovalOfParenthesis(['2']))

        proof.evolve_equality('a^(1 + 1)',
                              '2 = 1 + 1',
                              Addition(['1', '1']))

        proof.evolve_equality('a^1 * a^1',
                              'a^(1 + 1) = a^1 * a^1',
                              PowerDistribution(['a', '1', '1']))

        proof.evolve_equality('a * a^1',
                              'a^1 = a',
                              IdentityExponent(['a']))

        proof.evolve_equality('a * a',
                              'a^1 = a',
                              IdentityExponent(['a']))

        proof.conclude()

        return proof


class CubeLeftDistribution(thm.Equality):
    """
    Theorem that states that a^3 = a^2*a.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the left distribution of the cube",
                         conclusion='a^3 = a^2*a',
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a^3')

        proof.evolve_equality('a^(3)',
                              '3 = (3)',
                              RemovalOfParenthesis(['3']))

        proof.evolve_equality('a^(2 + 1)',
                              '3 = 2 + 1',
                              Addition(['2', '1']))

        proof.evolve_equality('a^2 * a^1',
                              'a^(2 + 1) = a^2 * a^1',
                              PowerDistribution(['a', '2', '1']))

        proof.evolve_equality('a^2 * a',
                              'a^1 = a',
                              IdentityExponent(['a']))

        proof.conclude()

        return proof


class CubeRightDistribution(thm.Equality):
    """
    Theorem that states that a^3 = a*a^2.
    The order of the unknowns is the following: a.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the right distribution of the cube",
                         conclusion='a^3 = a*a^2',
                         unknowns=['a'])

    def get_proof(self):
        proof = Proof(self, 'a^3')

        proof.evolve_equality('a^2*a',
                              'a^3 = a^2*a',
                              CubeLeftDistribution(['a']))

        proof.evolve_equality('a*a^2',
                              'a^2*a = a*a^2',
                              ProductCommutativity(['a^2', 'a']))

        proof.conclude()

        return proof


class FirstRemarkableIdentity(thm.Equality):
    """
    Theorem that states that (a + b)^2 = a^2 + 2*a*b + b^2.
    The order of the unknowns is the following: a, b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the first remarkable identity",
                         conclusion="(a+b)^2 = a^2 + 2*a*b + b^2",
                         unknowns=['a', 'b'])

    def get_proof(self):
        proof = Proof(self, '(a + b)^2')

        proof.evolve_equality('(a + b)*(a + b)',
                              '(a + b)^2 = (a + b)*(a + b)',
                              SquareDistribution(['(a + b)']))

        proof.evolve_equality('a*(a + b) + b*(a + b)',
                              '(a + b)*(a + b) = a*(a + b) + b*(a + b)',
                              RightDistributivity(['a', 'b', '(a + b)']))

        proof.evolve_equality('a*a + a*b + b*(a + b)',
                              'a*(a + b) = a*a + a*b',
                              LeftDistributivity(['a', 'a', 'b']))

        proof.evolve_equality('a*a + a*b + b*a + b*b',
                              'b*(a + b) = b*a + b*b',
                              LeftDistributivity(['b', 'a', 'b']))

        proof.evolve_equality('a*a + a*b + a*b + b*b',
                              'b*a = a*b',
                              ProductCommutativity(['a', 'b']))

        proof.evolve_equality('a*a + 1*a*b + a*b + b*b',
                              'a*b = 1*a*b',
                              LeftMultiplicationByIdentity(['a*b']))

        proof.evolve_equality('a*a + 1*a*b + 1*a*b + b*b',
                              'a*b = 1*a*b',
                              LeftMultiplicationByIdentity(['a*b']))

        proof.evolve_equality('a*a + 2*a*b + b*b',
                              '1*a*b + 1*a*b = 2*a*b',
                              LitteralAddition(['1', '1', 'a*b']))

        proof.evolve_equality('a^2 + 2*a*b + b*b',
                              'a*a = a^2',
                              SquareDistribution(['a']))

        proof.evolve_equality('a^2 + 2*a*b + b^2',
                              'b*b = b^2',
                              SquareDistribution(['b']))

        proof.conclude()

        return proof


class FirstIdentityWithTwist(thm.Equality):
    """
    Theorem that states that (x + 1)^2 = x^2 + 2*x + 1.
    The order of the unknowns is the following: x.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the first identity with a twist",
                         conclusion="(x + 1)^2 = x^2 + 2*x + 1",
                         unknowns=['x'])

    def get_proof(self):
        proof = Proof(self, '(x + 1)^2')

        proof.evolve_equality('x^2 + 2*x*1 + 1^2',
                              '(x + 1)^2 = x^2 + 2*x*1 + 1^2',
                              FirstRemarkableIdentity(['x', '1']))

        proof.evolve_equality('x^2 + 2*x + 1^2',
                              '2*x*1 = 2*x',
                              RightMultiplicationByIdentity(['2*x']))

        proof.evolve_equality('x^2 + 2*x + 1',
                              '1^2 = 1',
                              Power(['1', '2']))

        proof.conclude()

        return proof


class CubeRemarkableIdentity(thm.Equality):
    """
    Theorem that states that (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3.
    The order of the unknowns is the following: a, b.
    """

    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the cube remarkable identity",
                         conclusion=("(a + b)^3 = "
                                     "a^3 + 3*a^2*b + 3*a*b^2 + b^3"),
                         unknowns=['a', 'b'])

    def get_proof(self):
        proof = Proof(self, '(a + b)^3')

        proof.evolve_equality('(a + b)^2 * (a + b)',
                              '(a + b)^3 = (a + b)^2 * (a + b)',
                              CubeLeftDistribution(['(a + b)']))

        proof.evolve_equality('((a + b)^2) * (a + b)',
                              '(a + b)^2 = ((a + b)^2)',
                              RemovalOfParenthesis(['(a + b)^2']))

        proof.evolve_equality('(a^2 + 2*a*b + b^2) * (a + b)',
                              '(a + b)^2 = a^2 + 2*a*b + b^2',
                              FirstRemarkableIdentity(['a', 'b']))

        modif = ('(a^2 + 2*a*b + b^2) * (a + b) = ' +
                 '(a^2 + 2*a*b + b^2)*a + (a^2 + 2*a*b + b^2)*b')
        proof.evolve_equality('(a^2 + 2*a*b + b^2)*a + (a^2 + 2*a*b + b^2)*b',
                              modif,
                              LeftDistributivity(['(a^2 + 2*a*b + b^2)', 'a',
                                                  'b']))

        new_eq = 'a^2*a + 2*a*b*a + b^2*a + (a^2 + 2*a*b + b^2)*b'
        modif = '(a^2 + 2*a*b + b^2)*a = a^2*a + 2*a*b*a + b^2*a'
        proof.evolve_equality(new_eq, modif,
                              TripleRightDistributivity(['a^2', '2*a*b', 'b^2',
                                                         'a']))

        new_eq = 'a^2*a + 2*a*b*a + b^2*a + a^2*b + 2*a*b*b + b^2*b'
        modif = '(a^2 + 2*a*b + b^2)*b = a^2*b + 2*a*b*b + b^2*b'
        proof.evolve_equality(new_eq, modif,
                              TripleRightDistributivity(['a^2', '2*a*b',
                                                         'b^2', 'b']))

        new_eq = 'a^3 + 2*a*b*a + b^2*a + a^2*b + 2*a*b*b + b^2*b'
        proof.evolve_equality(new_eq,
                              'a^2*a = a^3',
                              CubeLeftDistribution(['a']))

        proof.evolve_equality('a^3 + 2*a*b*a + b^2*a + a^2*b + 2*a*b*b + b^3',
                              'b^2*b = b^3',
                              CubeLeftDistribution(['b']))

        proof.evolve_equality('a^3 + 2*a*b*a + a^2*b + b^2*a + 2*a*b*b + b^3',
                              'b^2*a + a^2*b = a^2*b + b^2*a',
                              AdditionCommutativity(['b^2*a', 'a^2*b']))

        proof.evolve_equality('a^3 + 2*a*a*b + a^2*b + b^2*a + 2*a*b*b + b^3',
                              'b*a = a*b',
                              ProductCommutativity(['a', 'b']))

        proof.evolve_equality('a^3 + 2*a^2*b + a^2*b + b^2*a + 2*a*b*b + b^3',
                              'a*a = a^2',
                              SquareDistribution(['a']))

        new_eq = 'a^3 + 2*a^2*b + 1*a^2*b + b^2*a + 2*a*b*b + b^3'
        proof.evolve_equality(new_eq,
                              'a^2*b = 1*a^2*b',
                              LeftMultiplicationByIdentity(['a^2*b']))

        proof.evolve_equality('a^3 + 3*a^2*b + b^2*a + 2*a*b*b + b^3',
                              '2*a^2*b + 1*a^2*b = 3*a^2*b',
                              LitteralAddition(['2', '1', 'a^2*b']))

        proof.evolve_equality('a^3 + 3*a^2*b + a*b^2 + 2*a*b*b + b^3',
                              'b^2*a = a*b^2',
                              ProductCommutativity(['b^2', 'a']))

        proof.evolve_equality('a^3 + 3*a^2*b + a*b^2 + 2*a*b^2 + b^3',
                              'b*b = b^2',
                              SquareDistribution(['b']))

        proof.evolve_equality('a^3 + 3*a^2*b + 1*a*b^2 + 2*a*b^2 + b^3',
                              'a*b^2 = 1*a*b^2',
                              LeftMultiplicationByIdentity(['a*b^2']))

        proof.evolve_equality('a^3 + 3*a^2*b + 3*a*b^2 + b^3',
                              '1*a*b^2 + 2*a*b^2 = 3*a*b^2',
                              LitteralAddition(['1', '2', 'a*b^2']))

        proof.conclude()

        return proof
