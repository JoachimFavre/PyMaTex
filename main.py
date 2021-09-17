# -*- coding: utf-8 -*-
"""
The main file for this project.

You can write which proofs will be saved in this file, set the seed for the
random numbers, or define the name of the file in which the proof will be
saved. There are also some hijacks which you can uncomment (ctrl+1 in Spyder),
to see that this program has many protections, even against proofs that
are trying to break it.

Created on Fri Apr 16 16:44:16 2021
@author: Joachim Favre & Alberts Reisons
"""
import time
import random as rng

from theorem_group import TheoremGroup
import theorem_set as thmset
import hijacks


beginning_time = time.time()
rng.seed(1729)  # can be set to be always different (using beginning_time)

theorem_group = TheoremGroup("A set of proofs that definitely deserve a 6")

# theorem_group.add_theorem(hijacks.Hijack1)
# theorem_group.add_theorem(hijacks.Hijack2)
# theorem_group.add_theorem(hijacks.Hijack3)
# theorem_group.add_theorem(hijacks.Hijack4)

# The following lines are not necessary since we use add_all_theorems(thmset),
# but we use this to give some kind of order to the generated document.
theorem_group.add_theorem(thmset.Addition)
theorem_group.add_theorem(thmset.Product)
theorem_group.add_theorem(thmset.Power)

theorem_group.add_theorem(thmset.FirstIdentityWithTwist)
theorem_group.add_theorem(thmset.TripleRightDistributivity)
theorem_group.add_theorem(thmset.CubeRightDistribution)
theorem_group.add_theorem(thmset.CubeRemarkableIdentity)

# Add the last that have not been added yet, so that we are not missing any.
theorem_group.add_all_theorems(thmset)

theorem_group.save("result")

print("Finished in {:.2f} seconds!".format(time.time() - beginning_time))
