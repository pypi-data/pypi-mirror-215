import pytest

from lean_dojo import *


def test_timeout_1(minif2f_repo: LeanGitRepo) -> None:
    thm = Theorem(minif2f_repo, "lean/src/test.lean", "amc12_2000_p6")
    with Dojo(thm) as (dojo, init_state):
        res = dojo.run_tac(
            init_state,
            "{ revert p q h₀ h₁ h₂, intros p q hpq, rintros ⟨hp, hq⟩, rintro ⟨h, h⟩, intro h, have h₁ := nat.prime.ne_zero hpq.1, have h₂ : q ≠ 0, { rintro rfl, simp * at * }, apply h₁, revert hpq, intro h, simp * at *, apply h₁, have h₃ : q = 10 * q, apply eq.symm, all_goals { dec_trivial! } }",
        )
        assert isinstance(res, TimeoutError)


# https://leanprover.zulipchat.com/#narrow/stream/270676-lean4/topic/How.20to.20set.20tactic.20timeout.20in.20Lean.204.3F
@pytest.mark.skip()
def test_timeout_2(mathlib4_repo: LeanGitRepo) -> None:
    thm = Theorem(
        mathlib4_repo,
        "Mathlib/LinearAlgebra/Matrix/BilinearForm.lean",
        "mem_selfAdjointMatricesSubmodule'",
    )
    with Dojo(thm) as (dojo, init_state):
        res = dojo.run_tac(init_state, "repeat {skip}")
        assert isinstance(res, TimeoutError)
