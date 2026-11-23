
from automata_extensions.fa.dfa import ExtendedDFA
from automata_extensions.fa.nfa import ExtendedNFA


def test_conversion_aller_retour():
    automate_initial = ExtendedDFA(
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

    # Étape 1 : automate vers grammaire
    grammaire = automate_initial.to_grammar()

    # Étape 2 : grammaire vers automate
    nouvel_automate = ExtendedNFA.from_grammar(grammaire)

    # Étape 3 : comparer les mots acceptés
    mots = ["", "a", "ab", "abb", "b", "aa", "ba"]

    for mot in mots:
        assert (
            automate_initial.accepts_input(mot)
            == nouvel_automate.accepts_input(mot)
        )

