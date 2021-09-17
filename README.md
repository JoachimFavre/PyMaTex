# PyMaTex
## Table of content
1. [Aim](#Aim)
2. [How to define a new theorem or a new axiom](#How-to-define-a-new-theorem-or-a-new-axiom)
3. [Special case: evaluations](#Special-case-evaluations)
4. [Hijacks](#Hijacks)
5. [Important notes](#Important-notes)
6. [Ways to improve the program](#Ways-to-improve-the-program)

## Aim
The aim of this school project is to give (some kind of) library, which allows to write a simple mathematical proof, which will get completely verified and then saved in a LaTeX document. If you are interested in the idea behind this project, go take a look at [Metamath](http://us.metamath.org/), a program having the exact same idea but being much more complete. Note that this program has been done in collaboration with Alberts Reisons.

## How to define a new theorem or a new axiom
First, you have to know that, for the program, a theorem and a proof are (almost) the same thing. The main difference comes from the fact that an axiom is a theorem to which you give no proof. Moreover, for now, we can only work with direct equalities (show that (a + b)^3 = a^3 + 3a^2\*b + 3a\*b^2 + b^3, for example). Thus, all theorems (and axioms) inherit from the ```theorem.Equality``` class. To define an axiom we can do the following:
```python
class LeftDistributivity(theorem.Equality):
    def __init__(self, param_list):
        super().__init__(param_list,
                         name="the left distributivity of the product",
                         conclusion='a*(b + c) = a*b + a*c',
                         unknowns=['a', 'b', 'c'])
```

To cut this down: we are calling the constructor of the super class (```theorem.Equality```), giving it a ```param_list``` which has been given to this constructor, a name that will be used when generating the LaTeX, the equality we want to prove (or that we assume to be true if it is an axiom, and the list of unknowns which are used for this theorem (note that unknowns must be one character long).

Now, let's say we want to define a theorem (and not an axiom). Let's define the right distributivity of the product, using the axiom defined right above, and the product commutativity. 
```python
class RightDistributivity(theorem.Equality):
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
```

We are doing everything exactly as if we were defining an axiom, but we also overload the ```get_proof(self)``` method. In it, we instanciate a ```proof.Proof``` class, to which we give a reference to the theorem we want to show (```self```), and the beginning point of the proof. We can then make the equality "evolve", giving the ```Proof.evolve_equality``` methods the following parameters: the new step of the equality, the sole substitution that we did to get to the new step, and the theorem (or axiom) we used. In other words, we must do one (and exactly one, no more, no less) substitution to a previous equality step (it doesn't matter which, but I guess it's more readable if you only use the last step), and we must have a theorem that proves that our substitution is allowed. When giving the theorem to this method, we need to instanciate it using a ```param_list``` as long as the ```unknown_list``` defined in the constructor of the theorem (or axiom). This ```param_list``` must contain the substituions we want to do in the theorem. If we have a theorem stating that (a + b)^2 = a^2 + 2\*a\*b + b^2, with ```unknown_list=['a', 'b']```, and that we want to use this theorem to show that (b + 1)^2 = b^2 + 2\*b\*1 + 1^2. we can give a ```param_list``` of ```['b', '1']```.

Two things are verified while calling ```Proof.evolve_equality```: we have done exactly one substitution, and that it is proven to be true by the theorem.

To finish with, do not forget to call the ```proof.conclude()``` method (which will verify that we have indeed reached the conclusion we gave in the constructor), and to return the proof.

## Special case: evaluations
There is a special case in which we actually need to evaluate some values. For example, if we want to prove the litteral addition, we can do:
```python
class LitteralAddition(theorem.Equality):
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
```

We are using the ```proof.use_simplification``` method, giving it the new step (which has had one and exactly one substitution) and the substituion we used. Note that the simplifications must also be defined in the constructor of the theorem (or axiom). 

This means that, in our theorem conclusion, we are saying that a\*x + b\*x = c\*x, but while using this theorem, the user can only set the a, b, and x variables to whatever he or she wants; however, the program will verify that a + b is indeed equal to the c value (thus a and b need to be numbers).

## Hijacks
There are some hijacks defined in the ```hijacks.py``` module. Those are some proofs that were designed to break the program and prove something wrong. However, the program will not accept them as proofs; they are basically here to present the verifications we added to the program. 

## Important notes
- Unknowns must be one character long (as mentionned before).
- You cannot have implied multiplication, you must use the '\*' symbol.
- Lots of functionalities missing.

## Missing functionalities
- Only works with direct equalities.
- No soustraction, division or roots working.

## Ways to improve the program
- Implement more types of proves, such as direct implications (A => B and A <=> B), proof by contrapositive, by contradiction and by induction.
- Implement more mathematical objects, and make their implementation easier. This basically goes with (mathematical) definitions: we want to be able to define a - b = a + (-b), with (-b) defined such that b + (-b) = 0, or what an integral or a matrix is. 

## Note
Well you've read this document through (or just skipped to the end). Let me give you a tip: what if you tried to execute the code without giving the program any proof to verify?
