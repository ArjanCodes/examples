# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import office
from hypothesis import given, strategies as st


@given(size=st.integers())
def test_fuzz_generate_random_team(size):
    office.generate_random_team(size=size)

