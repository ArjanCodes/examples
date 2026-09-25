# Memento pattern

Progressive, standalone examples for the Memento-pattern video.

1. `01_workflow.py` starts with an editable workflow that has no undo support.
2. `02_snapshot.py` introduces an immutable `WorkflowSnapshot` and lets the
   workflow restore itself.
3. `03_generic_history.py` adds a generic `History[T]` caretaker through the
   `Snapshotable[T]` protocol.
4. `04_undo_redo.py` adds redo and shows the snapshot boundary: editable
   configuration is restored, but runtime execution state is left alone.

Run all examples from this directory:

```bash
for example in [0-9][0-9]_*.py; do python "$example"; done
```
