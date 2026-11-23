
import pytest
from automata_extensions.fa.nfa import ExtendedNFA


def test_from_grammar():
    grammaire = {
        "non_terminaux": {"q0", "q1"},
        "terminaux": {"a", "b"},
        "symbole_initial": "q0",
        "regles": {
            "q0": {"aq1"},
            "q1": {"bq1", ""}
        }
    }

    automate = ExtendedNFA.from_grammar(grammaire)

    assert automate.initial_state == "q0"

    assert automate.states == {"q0", "q1"}

    assert automate.final_states == {"q1"}

    assert automate.transitions["q0"]["a"] == {"q1"}

    assert automate.transitions["q1"]["b"] == {"q1"}


def test_from_grammar_transitions_multiples():
    grammaire = {
        "non_terminaux": {"q0", "q1", "q2"},
        "terminaux": {"a", "b"},
        "symbole_initial": "q0",
        "regles": {
            "q0": {"aq1", "aq2"},
            "q1": {"bq1", ""},
            "q2": {"bq2", ""}
        }
    }

    automate = ExtendedNFA.from_grammar(grammaire)

    assert automate.transitions["q0"]["a"] == {"q1", "q2"}

    assert automate.final_states == {"q1", "q2"}

    assert automate.accepts_input("a")
    assert automate.accepts_input("ab")
    assert automate.accepts_input("abb")


def test_from_grammar_transition_epsilon():
    grammaire = {
        "non_terminaux": {"q0", "q1"},
        "terminaux": {"a"},
        "symbole_initial": "q0",
        "regles": {
            "q0": {"q1"},
            "q1": {"a", ""}
        }
    }

    automate = ExtendedNFA.from_grammar(grammaire)

    assert automate.transitions["q0"][""] == {"q1"}

    assert automate.accepts_input("")
    assert automate.accepts_input("a")



def test_from_grammar_symbole_initial_invalide():
    grammaire = {
        "non_terminaux": {"q0", "q1"},
        "terminaux": {"a"},
        "symbole_initial": "q2",
        "regles": {
            "q0": {"aq1"},
            "q1": {""}
        }
    }

    with pytest.raises(ValueError, match="symbole initial"):
        ExtendedNFA.from_grammar(grammaire)


def test_from_grammar_regle_invalide():
    grammaire = {
        "non_terminaux": {"q0", "q1"},
        "terminaux": {"a"},
        "symbole_initial": "q0",
        "regles": {
            "q0": {"xyz"},
            "q1": {""}
        }
    }

    with pytest.raises(ValueError, match="Règle de grammaire invalide"):
        ExtendedNFA.from_grammar(grammaire)


def test_from_grammar_destination_inexistante():
    grammaire = {
        "non_terminaux": {"q0", "q1"},
        "terminaux": {"a"},
        "symbole_initial": "q0",
        "regles": {
            "q0": {"aq3"},
            "q1": {""}
        }
    }

    with pytest.raises(ValueError, match="Règle de grammaire invalide"):
        ExtendedNFA.from_grammar(grammaire)
