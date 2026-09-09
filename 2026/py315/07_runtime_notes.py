"""Report build-dependent 3.15 capabilities without pretending every build has them."""

import sys
import sysconfig


def main() -> None:
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    jit = getattr(sys, "_jit", None)

    print(f"Python: {sys.version.split()[0]}")
    print(f"GIL enabled in this interpreter? {gil_enabled}")
    print(f"Free-threaded build flag: {sysconfig.get_config_var('Py_GIL_DISABLED') or 0}")

    if jit is None:
        print("JIT controls are not exposed by this build.")
    else:
        print(f"JIT available in this build? {jit.is_available()}")
        print(f"JIT enabled in this process? {jit.is_enabled()}")
        print("Do not benchmark this while asking whether the JIT is active: that changes tracing.")


if __name__ == "__main__":
    main()
