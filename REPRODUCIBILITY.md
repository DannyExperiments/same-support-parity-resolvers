# Reproducibility

Run from the repository root with Python 3.11 or later.

    python3 -I scripts/verify_repository.py
    python3 -I verification/src/replay.py

The standard-library replay checks both witnesses through 604 block laws, all 2,916 joint priority pairs for the two-block tests, and 128 grouped-word partial sums on the separating word. [Recorded replay](verification/results/replay.txt).

Open the [three-state explorer](visualization/three-state.html) in an offline browser or unzip its [self-contained ZIP](visualization/three-state-blocks-explorer.zip). [GIF rendering source](visualization/render_three_state.py) · [Original four-state explorer](visualization/index.html) · [PDF build](paper/BUILD.md).
