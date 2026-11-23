import pytest
from automata_extensions.fa.nfa import ExtendedNFA
from automata_extensions.fa.dfa import ExtendedDFA
from automata_extensions.fa.gnfa import ExtendedGNFA

def test_reverse_nfa():
    automate = ExtendedNFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {'b': {'q2'}},
            'q2': {}
        },
        initial_state='q0',
        final_states={'q2'}
    )

    inverse = automate.reverse()

    assert inverse.initial_state == "q_initial_inverse"
    assert inverse.final_states == {'q0'}
    assert inverse.accepts_input("ba")
    assert not inverse.accepts_input("ab")

def test_reverse_dfa():
    automate = ExtendedDFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a': 'q2', 'b': 'q2'}
        },
        initial_state='q0',
        final_states={'q2'}
    )

    inverse = automate.reverse()

    assert inverse.initial_state == "q_initial_inverse"
    assert inverse.final_states == {'q0'}
    assert inverse.accepts_input("ba")
    assert not inverse.accepts_input("ab")

def test_reverse_sans_etat_final():
    automate = ExtendedNFA(
        states={'q0', 'q1'},
        input_symbols={'a'},
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {}
        },
        initial_state='q0',
        final_states=set()
    )

    inverse = automate.reverse()

    assert inverse.initial_state == "q_initial_inverse"
    assert inverse.final_states == {'q0'}
    assert not inverse.accepts_input("")
    assert not inverse.accepts_input("a")

def test_reverse_conflit_nom_etat_initial():
    automate = ExtendedNFA(
        states={'q0', 'q1', 'q_initial_inverse'},
        input_symbols={'a'},
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {},
            'q_initial_inverse': {}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    inverse = automate.reverse()

    assert inverse.initial_state == "q_initial_inverse_"
    assert "q_initial_inverse_" in inverse.states
    assert "q_initial_inverse" in inverse.states
    assert inverse.accepts_input("a")

def test_reverse_retourne_extended_nfa():
    automate = ExtendedNFA(
        states={'q0', 'q1'},
        input_symbols={'a'},
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    inverse = automate.reverse()

    assert isinstance(inverse, ExtendedNFA)
    assert hasattr(inverse, "accessibles")
    assert hasattr(inverse, "coaccessibles")
    assert hasattr(inverse, "utiles")

def test_reverse_retourne_extended_nfa():
    automate = ExtendedNFA(
        states={'q0', 'q1'},
        input_symbols={'a'},
        transitions={
            'q0': {'a': {'q1'}},
            'q1': {}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    inverse = automate.reverse()

    assert isinstance(inverse, ExtendedNFA)
    assert hasattr(inverse, "accessibles")
    assert hasattr(inverse, "coaccessibles")
    assert hasattr(inverse, "utiles")

def test_complete_dfa_incomplet():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"b": "q0"}
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )

    resultat = automate.complete()

    assert "q_puits" in resultat.states
    assert resultat.transitions["q0"]["b"] == "q_puits"
    assert resultat.transitions["q1"]["a"] == "q_puits"
    assert resultat.transitions["q_puits"]["a"] == "q_puits"
    assert resultat.transitions["q_puits"]["b"] == "q_puits"

def test_complete_dfa_deja_complet():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1", "b": "q0"},
            "q1": {"a": "q1", "b": "q0"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    resultat = automate.complete()

    assert resultat is automate
    assert resultat.states == automate.states

def test_complete_refuse_nfa():
    automate = ExtendedNFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1"}},
            "q1": {"b": {"q0"}}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    with pytest.raises(TypeError, match="réservée aux DFA"):
        automate.complete()

def test_complete_conflit_nom_q_puits():
    automate = ExtendedDFA(
        states={"q0", "q1", "q_puits"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"b": "q0"},
            "q_puits": {"a": "q_puits", "b": "q_puits"}
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )

    resultat = automate.complete()

    assert "q_puits_" in resultat.states
    assert resultat.transitions["q0"]["b"] == "q_puits_"

def test_complement_dfa():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1", "b": "q0"},
            "q1": {"a": "q1", "b": "q0"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    resultat = automate.complement()

    assert resultat.initial_state == "q0"
    assert resultat.final_states == {"q0"}

    assert automate.accepts_input("a")
    assert not resultat.accepts_input("a")

    assert not automate.accepts_input("b")
    assert resultat.accepts_input("b")

def test_trim_dfa():
    automate = ExtendedDFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1", "b": "q2"},
            "q1": {"a": "q1"},
            "q2": {"b": "q2"},
            "q3": {"a": "q3", "b": "q3"}
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )

    resultat = automate.trim()

    assert resultat.states == {"q0", "q1"}
    assert resultat.final_states == {"q1"}
    assert "q2" not in resultat.states
    assert "q3" not in resultat.states

def test_trim_nfa():
    automate = ExtendedNFA(
        states={"q0", "q1", "q2"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1", "q2"}},
            "q1": {"b": {"q1"}},
            "q2": {"b": {"q2"}}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    resultat = automate.trim()

    assert resultat.states == {"q0", "q1"}
    assert resultat.final_states == {"q1"}
    assert resultat.transitions["q0"]["a"] == {"q1"}

def test_trim_dfa_sans_etat_final():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states=set()
    )

    resultat = automate.trim()

    assert resultat.states == {"q0"}
    assert resultat.final_states == set()
    assert resultat.transitions["q0"] == {}

def test_to_dfa():
    automate = ExtendedNFA(
        states={"q0", "q1", "q2"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1", "q2"}},
            "q1": {"b": {"q1"}},
            "q2": {"b": {"q2"}}
        },
        initial_state="q0",
        final_states={"q2"}
    )

    resultat = automate.to_dfa()

    assert resultat.initial_state == frozenset({"q0"})
    assert frozenset({"q1", "q2"}) in resultat.states
    assert frozenset({"q1", "q2"}) in resultat.final_states

def test_to_dfa_avec_epsilon():
    automate = ExtendedNFA(
        states={"q0", "q1", "q2"},
        input_symbols={"a"},
        transitions={
            "q0": {"": {"q1"}},
            "q1": {"": {"q2"}},
            "q2": {"a": {"q2"}}
        },
        initial_state="q0",
        final_states={"q2"}
    )

    resultat = automate.to_dfa()

    etat_initial = frozenset({"q0", "q1", "q2"})
    etat_suivant = frozenset({"q2"})

    assert resultat.initial_state == etat_initial
    assert etat_initial in resultat.final_states
    assert resultat.transitions[etat_initial]["a"] == etat_suivant
    assert etat_suivant in resultat.final_states

def test_to_nfa():
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

    resultat = automate.to_nfa()

    assert isinstance(resultat, ExtendedNFA)
    assert resultat.states == {"q0", "q1"}
    assert resultat.initial_state == "q0"
    assert resultat.final_states == {"q1"}
    assert resultat.transitions["q0"]["a"] == {"q1"}
    assert resultat.transitions["q1"]["b"] == {"q1"}

def test_to_gnfa_dfa():
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

    resultat = automate.to_gnfa()

    from automata.fa.gnfa import GNFA

    assert isinstance(resultat, GNFA)
    assert resultat.initial_state in resultat.states
    assert resultat.final_state in resultat.states
    assert resultat.initial_state != resultat.final_state
    assert isinstance(resultat, ExtendedGNFA)

def test_to_gnfa_nfa():
    automate = ExtendedNFA(
        states={"q0", "q1", "q2"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1", "q2"}},
            "q1": {"b": {"q2"}},
            "q2": {}
        },
        initial_state="q0",
        final_states={"q2"}
    )

    resultat = automate.to_gnfa()

    assert isinstance(resultat, ExtendedGNFA)
    assert resultat.initial_state in resultat.states
    assert resultat.final_state in resultat.states
    assert resultat.initial_state != resultat.final_state

def test_to_regex():
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

    resultat = automate.to_regex()

    assert isinstance(resultat, str)
    assert resultat != ""