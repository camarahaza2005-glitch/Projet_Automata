import pytest
from automata_extensions.fa.dfa import ExtendedDFA
from automata_extensions.fa.nfa import ExtendedNFA


def test_to_graphviz():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz()

    assert "q0" in graphe.source
    assert "q1" in graphe.source
    assert "a" in graphe.source
    assert "doublecircle" in graphe.source

def test_afficher_png(tmp_path):
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    chemin = automate.afficher(
        nom_fichier=str(tmp_path / "automate"),
        format="png"
    )

    assert chemin.endswith(".png")

def test_direction_graphe():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz()

    assert "rankdir=LR" in graphe.source

def test_direction_personnalisee():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz(direction="TB")

    assert "rankdir=TB" in graphe.source

def test_direction_invalide():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    with pytest.raises(ValueError):
        automate.to_graphviz(direction="XYZ")

def test_couleurs_etats():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz()

    assert "fillcolor=lightblue" in graphe.source
    assert "fillcolor=lightgreen" in graphe.source

def test_couleurs_personnalisees():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz(
        couleur_etat="yellow",
        couleur_final="red"
    )

    assert "fillcolor=yellow" in graphe.source
    assert "fillcolor=red" in graphe.source

def test_titre_graphe():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz(titre="Mon premier automate")

    assert "Mon premier automate" in graphe.source
    assert "labelloc=t" in graphe.source

def test_transition_epsilon():
    automate = ExtendedNFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"": {"q1"}},
            "q1": {"a": {"q1"}}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.to_graphviz()

    assert "ε" in graphe.source

def test_afficher_svg(tmp_path):
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    chemin = automate.afficher(
        nom_fichier=str(tmp_path / "automate"),
        format="svg"
    )

    assert chemin.endswith(".svg")

def test_afficher_pdf(tmp_path):
        automate = ExtendedDFA(
            states={"q0", "q1"},
            input_symbols={"a"},
            transitions={
                "q0": {"a": "q1"},
                "q1": {"a": "q1"}
            },
            initial_state="q0",
            final_states={"q1"}
        )

        chemin = automate.afficher(
            nom_fichier=str(tmp_path / "automate"),
            format="pdf"
        )

        assert chemin.endswith(".pdf")

def test_afficher_personnalise(tmp_path):
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    chemin = automate.afficher(
        nom_fichier=str(tmp_path / "automate_personnalise"),
        format="png",
        direction="TB",
        couleur_etat="yellow",
        couleur_final="pink",
        titre="Mon automate"
    )

    assert chemin.endswith(".png")

def test_format_invalide():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    with pytest.raises(ValueError):
        automate.afficher(format="jpg")

def test_display():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.display()

    assert graphe is not None
    assert graphe.source is not None
    assert "q0" in graphe.source
    assert "q1" in graphe.source

def test_display_personnalise():
    automate = ExtendedDFA(
        states={"q0", "q1"},
        input_symbols={"a"},
        transitions={
            "q0": {"a": "q1"},
            "q1": {"a": "q1"}
        },
        initial_state="q0",
        final_states={"q1"}
    )

    graphe = automate.display(
        direction="TB",
        couleur_etat="yellow",
        couleur_final="pink",
        titre="Mon automate"
    )

    assert "rankdir=TB" in graphe.source
    assert "yellow" in graphe.source
    assert "pink" in graphe.source
    assert "Mon automate" in graphe.source