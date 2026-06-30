# TeenyRogue

Pygame clone of the iOS roguelike *TinyRogue*. A single, flat Python package (no
monorepo, no backend/web services, no database). Entry point: `tnyrogue.py`
(`main()`), also exposed as the `tnyrogue` console script.

## Cursor Cloud specific instructions

### Services / how to run

This repo is one desktop game; there are no background services.

- Run the game: `python tnyrogue.py` (or the installed `tnyrogue` console script).
  Must be run from the repo root because all asset paths are relative (e.g.
  `images/player32.png`).
- Controls: arrow keys or vim `h/j/k/l` to move; number keys `1`-`9` select
  equipment; `p` prints player state; `q` quits.
- The game needs a display. A desktop X server is available on `DISPLAY=:1` —
  launch with `DISPLAY=:1 python tnyrogue.py`. For headless logic-only runs, use
  `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy`.
- ALSA "cannot find card" warnings on startup are harmless (no audio device in
  the VM); they do not affect gameplay.

### Tests

There is no pytest/unittest suite or CI. The `test_*.py` files are ad-hoc,
`print`-based diagnostic scripts, not assertion-based tests (they can print
`ERROR`/non-valid lines by design and still exit 0):

- `python test_GameMap.py` and `python test_utils.py` — headless, no display.
- `python test_decal.py` — opens a Pygame window (needs a display); quit with `q`.

### Lint

No linter is configured in the repo (`.pylintrc` is gitignored and not present).
Source uses `# noqa` hints suggesting flake8 was used historically, but it is not
a committed/required step.

### Gotchas

- The game writes `map_attempts.txt` (map-generation stats) to the CWD as a side
  effect — this is output, not required input.
- `sheet.py` is dead code (imports a missing `constants` module) and is not used
  by the game.
