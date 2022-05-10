# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import office
from hypothesis import given, strategies as st


@given(team=st.lists(st.sampled_from(office.Employee)))
def test_fuzz_fire_random_employee(team):
    office.fire_random_employee(team=team)

