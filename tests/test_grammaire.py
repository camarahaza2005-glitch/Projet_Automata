from automata_extensions.fa.dfa import ExtendedDFA


def test_to_grammar():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"b": "q1"}
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )

    grammaire = automate.to_grammar()

    assert grammaire["symbole_initial"] == "q0"

    assert grammaire["non_terminaux"] == {"q0", "q1"}

    assert grammaire["terminaux"] == {"a", "b"}

    assert "aq1" in grammaire["regles"]["q0"]

    assert "bq1" in grammaire["regles"]["q1"]

    assert "" in grammaire["regles"]["q1"]