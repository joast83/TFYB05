"""Keep the students' common field-law workflow in integral form."""
from dataclasses import fields
import re

import numpy as np
import pytest

from em_visualisering.core import EPS0
from em_visualisering.guidance import GUIDANCE_BY_CLASS
from em_visualisering.starting_laws import LAWS
from em_visualisering.problems.ch02 import UniformSpaceChargePlates


def test_all_starting_laws_avoid_spatial_differential_forms():
    for pid, law in LAWS.items():
        assert not any(token in ' '.join(law) for token in (r'\nabla', '∇', 'differentialform')), pid
    for pid in ('2.13', '2.19'):
        assert LAWS[pid][0:2] == LAWS['2.8'][0:2]


def test_all_guidance_avoids_divergence_and_field_law_curls():
    # Potential gradients and the explicitly requested curl of A in 6.1 are
    # calculations, not alternative formulations of Gauss/Ampere laws.
    for guide in GUIDANCE_BY_CLASS.values():
        for field in fields(guide):
            value = getattr(guide, field.name)
            text = ' '.join(value) if isinstance(value, tuple) else value
            assert not re.search(r'\\nabla\s*\\cdot|∇\s*·|divergens|differentialform|Poisson', text), (guide.problem_id, field.name)
            if guide.problem_id != '6.1':
                assert not re.search(r'\\nabla\s*\\times|∇\s*×|curl', text), (guide.problem_id, field.name)
    for pid in ('2.13', '2.19', '5.7', '3.18', '8.12', '8.13', '10.3'):
        guide = next(g for g in GUIDANCE_BY_CLASS.values() if g.problem_id == pid)
        assert r'\oint' in ' '.join(guide.hints), pid


@pytest.mark.parametrize('rho', [-1e-8, 0., 1e-8])
@pytest.mark.parametrize('voltage', [-50., 0., 50.])
def test_plate_box_flux_matches_volume_charge(rho, voltage):
    # The new box argument must include both end faces, irrespective of the
    # potential-dependent constant field or the sign of the cloud charge.
    d, area = .1, .03
    x = np.array([.01, .04, .08])
    e, _ = UniformSpaceChargePlates.profiles(x, rho, voltage, d)
    e0, _ = UniformSpaceChargePlates.profiles(0., rho, voltage, d)
    np.testing.assert_allclose(EPS0 * area * (e-e0), rho * area * x, atol=1e-25)
