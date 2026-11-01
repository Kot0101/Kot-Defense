"""
Local override for python-for-android's ``pygame`` recipe.

python-for-android generates pygame's build ``Setup`` file from
``buildconfig/Setup.Android.SDL2.in``. In pygame 2.5.x that template lists

    surface src_c/surface.c src_c/alphablit.c src_c/surface_fill.c ...

but forgets ``src_c/simd_blitters_sse2.c``. As a result ``surface.so``
references ``alphablit_alpha_sse2_argb_surf_alpha`` while nothing defines it,
and the app dies on the phone with:

    dlopen failed: cannot locate symbol "alphablit_alpha_sse2_argb_surf_alpha"

On arm64 ``simd_blitters.h`` enables the NEON (sse2neon) variant by itself,
so simply adding the missing sources is enough - this is the upstream
workaround from pygame issue #4394.

We patch the generated ``Setup`` right after the stock recipe writes it.
"""

import os

from pythonforandroid.recipes.pygame import Pygame2Recipe


class KotDefensePygameRecipe(Pygame2Recipe):
    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)

        setup_path = os.path.join(self.get_build_dir(arch.arch), "Setup")
        with open(setup_path, "r") as handle:
            text = handle.read()

        if "simd_blitters_sse2.c" in text:
            return

        fixed = text.replace(
            "surface src_c/surface.c",
            "surface src_c/simd_blitters_sse2.c "
            "src_c/simd_blitters_avx2.c "
            "src_c/surface.c",
        )
        if fixed == text:
            raise RuntimeError(
                "pygame Setup template changed: 'surface src_c/surface.c' not found"
            )

        with open(setup_path, "w") as handle:
            handle.write(fixed)


recipe = KotDefensePygameRecipe()
