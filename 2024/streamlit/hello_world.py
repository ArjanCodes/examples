import streamlit as st
from py_wanderer import ALGORITHMS, HEURISTICS


def configure_page() -> None:
    st.set_page_config(page_title="Maze and Pathfinding Visualizer", layout="wide")


def configure_overview() -> None:
    st.markdown("## Overview")
    st.markdown(
        "This app generates a maze and visualizes the pathfinding algorithms solving it."
    )
    st.markdown(
        "The aim is to compare the performance of different algorithms and heuristics."
    )


def configure_available_algo_heuristics() -> None:
    st.markdown("## Algorithms and Heuristics")
    st.markdown("The following algorithms and heuristics are available:")

    with st.expander("Algorithms and Heuristics"):
        left, right = st.columns(2)
        left.markdown("### Algorithms")
        for algorithm in ALGORITHMS:
            left.markdown(f"- {algorithm.__name__}")

        right.markdown("### Heuristics")
        for heuristic in HEURISTICS:
            right.markdown(f"- {heuristic.__name__.title()}")


def main() -> None:
    configure_page()
    configure_overview()
    configure_available_algo_heuristics()


if __name__ == "__main__":
    main()
