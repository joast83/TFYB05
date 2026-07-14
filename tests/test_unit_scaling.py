import math
import unittest

from em_visualisering.registry import PROBLEMS
from em_visualisering.unit_scaling import display_scale_for, suggested_step


class UnitScalingTests(unittest.TestCase):
    def test_charge_is_shown_in_nanocoulombs(self):
        scale = display_scale_for("Laddning Q [C]", 3e-8)
        self.assertEqual(scale.display_unit, "nC")
        self.assertAlmostEqual(scale.to_display(3e-8), 30.0)
        self.assertAlmostEqual(scale.to_si(30.0), 3e-8)

    def test_compound_unit_keeps_denominator(self):
        scale = display_scale_for("Linjeladdningstäthet λ [C/m]", 1e-9)
        self.assertEqual(scale.display_unit, "nC/m")
        self.assertAlmostEqual(scale.to_display(1e-9), 1.0)

    def test_area_prefix_has_squared_factor(self):
        scale = display_scale_for("Tvärsnitt S [m²]", 2e-4)
        self.assertEqual(scale.display_unit, "cm²")
        self.assertAlmostEqual(scale.factor, 1e-4)
        self.assertAlmostEqual(scale.to_display(2e-4), 2.0)

    def test_every_problem_default_round_trips(self):
        for problem in PROBLEMS:
            for key, label, default in problem.parameters:
                with self.subTest(problem=problem.name, parameter=key):
                    default = float(default)
                    scale = display_scale_for(label, default)
                    shown = scale.to_display(default)
                    restored = scale.to_si(shown)
                    self.assertTrue(math.isfinite(shown))
                    self.assertAlmostEqual(restored, default, delta=max(1e-15, abs(default) * 1e-12))
                    self.assertGreater(scale.factor, 0.0)
                    self.assertGreater(suggested_step(shown), 0.0)


if __name__ == "__main__":
    unittest.main()
