# Reproducibility

Run from the repository root with Python 3.11 or later.

    python3 -I scripts/verify_repository.py
    python3 -I verification/src/replay.py

The standard-library replay propagates both row laws through 25 block lengths, checks the reset factorization and evaluates the geometric series with exact fractions. [Recorded replay](verification/results/replay.txt).

Extract the [offline explorer](visualization/parity-blocks-explorer.zip) and open index.html. The [GIF renderer](visualization/render.py) uses Python and Pillow with supplied font paths. [Build the paper](paper/BUILD.md).
