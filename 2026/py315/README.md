# Python 3.15 examples

Standalone, standard-library examples for the Python 3.15 video. The project is
pinned through `.python-version` to **Python 3.15.0rc2**, the latest release
candidate available on 2026-09-09. `pyproject.toml` limits the project to the
3.15 series; the companion uv pin selects the exact release candidate. Python
package metadata does not support a usable exact prerelease interpreter
constraint in uv's resolver.

From this directory, run an example with:

```bash
uv run python 01_lazy_imports.py
```

Run all regular examples:

```bash
for example in [0-9][0-9]_*.py; do uv run python "$example"; done
```

Tachyon is a sampling profiler intended to be run from the command line. It
needs platform support for attaching/sampling, so use it separately:

```bash
uv run python -m profiling.sampling run --duration 1 06_profile_workload.py
```

On macOS, Tachyon may require elevated permission to inspect process memory;
follow its on-screen guidance (normally `sudo -E`) if the command reports a
permission error. The workload itself still runs normally without it.

`07_runtime_notes.py` reports what the particular interpreter build supports;
it deliberately does not claim a benchmark win for the JIT or free-threading.
