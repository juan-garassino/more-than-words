from __future__ import annotations


def test_existing_modules_import():
    from generator.constraints_compiler import ConstraintMask  # noqa: F401
    from trainer.structured_scene_model_v2 import LoraLinear  # noqa: F401
