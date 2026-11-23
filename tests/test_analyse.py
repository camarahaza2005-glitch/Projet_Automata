from automata_extensions.fa.dfa import ExtendedDFA
from automata_extensions.fa.nfa import ExtendedNFA

def creer_automate():
    return ExtendedDFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q2"},
            "q2": {"a": "q2"},
            "q3": {"a": "q3"}
        },
        initial_state="q0",
        final_states={"q2"}
    )


def test_accessibles():
    automate = creer_automate()

    assert automate.accessibles() == {"q0", "q1", "q2"}


def test_coaccessibles():
    automate = creer_automate()

    assert automate.coaccessibles() == {"q0", "q1", "q2"}


def test_utiles():
    automate = creer_automate()

    assert automate.utiles() == {"q0", "q1", "q2"}

def test_aucun_etat_final():
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

    assert automate.coaccessibles() == set()
    assert automate.utiles() == set() 

def test_etat_inaccessible():
    automate = ExtendedDFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q2"},
            "q2": {"a": "q2"},
            "q3": {"a": "q3"}
        },
        initial_state="q0",
        final_states={"q2"}
    )

    assert automate.accessibles() == {"q0", "q1", "q2"}
    assert "q3" not in automate.accessibles()       

def test_plusieurs_chemins():
    automate = ExtendedDFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": "q1", "b": "q2"},
            "q1": {"a": "q3", "b": "q3"},
            "q2": {"a": "q3", "b": "q3"},
            "q3": {"a": "q3", "b": "q3"}
        },
        initial_state="q0",
        final_states={"q3"}
    )

    assert automate.accessibles() == {"q0", "q1", "q2", "q3"}


def creer_nfa():
    return ExtendedNFA(
        states={"q0", "q1", "q2", "q3", "q4"},
        input_symbols={"a", "b"},
        transitions={
            "q0": {"a": {"q1", "q2"}},
            "q1": {"b": {"q3"}},
            "q2": {"b": {"q4"}},
            "q3": {},
            "q4": {}
        },
        initial_state="q0",
        final_states={"q3", "q4"}
    )

def test_accessibles_nfa():
    automate = creer_nfa()

    assert automate.accessibles() == {"q0", "q1", "q2", "q3", "q4"}

def test_coaccessibles_nfa():
    automate = creer_nfa()

    assert automate.coaccessibles() == {
        "q0", "q1", "q2", "q3", "q4"
    }

def test_utiles_nfa():
    automate = creer_nfa()

    assert automate.utiles() == {
        "q0", "q1", "q2", "q3", "q4"
    }

def creer_nfa_avec_etat_inutile():
    return ExtendedNFA(
        states={"q0", "q1", "q2", "q3", "q4", "q5"},
        input_symbols={"a", "b", "c"},
        transitions={
            "q0": {"a": {"q1", "q2"}, "c": {"q5"}},
            "q1": {"b": {"q3"}},
            "q2": {"b": {"q4"}},
            "q3": {},
            "q4": {},
            "q5": {}
        },
        initial_state="q0",
        final_states={"q3", "q4"}
    )

def test_accessibles_nfa_avec_etat_inutile():
    automate = creer_nfa_avec_etat_inutile()

    assert automate.accessibles() == {
        "q0", "q1", "q2", "q3", "q4", "q5"
    }

def test_coaccessibles_nfa_avec_etat_inutile():
    automate = creer_nfa_avec_etat_inutile()

    assert automate.coaccessibles() == {
        "q0", "q1", "q2", "q3", "q4"
    }

def test_utiles_nfa_avec_etat_inutile():
    automate = creer_nfa_avec_etat_inutile()

    assert automate.utiles() == {
        "q0", "q1", "q2", "q3", "q4"
    }

def test_epsilon_closure():
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

    resultat = automate.epsilon_closure({"q0"})

    assert resultat == {"q0", "q1", "q2"}