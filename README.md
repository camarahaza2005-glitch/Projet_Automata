# Projet Automata

## Présentation

Ce projet consiste à étendre la bibliothèque Python `automata-lib` afin d'ajouter de nouvelles fonctionnalités pour manipuler les automates finis, les langages et les grammaires.

L'objectif est de proposer des outils supplémentaires pour analyser, transformer, convertir et visualiser les automates finis.

Le projet est développé en Python et s'appuie sur la bibliothèque `automata-lib`.

## Technologies utilisées

- Python 3.13
- automata-lib 9.2.0
- pytest
- Graphviz
- Git et GitHub

## Installation

### 1. Cloner le dépôt

```bash
git clone URL_DU_DEPOT
cd Projet_Automata
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances

```bash
pip install automata-lib==9.2.0 pytest graphviz
```

**Remarque :** Graphviz doit également être installé sur le système pour permettre la génération des fichiers graphiques.


## Fonctionnalités

Le projet propose plusieurs fonctionnalités :

- Analyse des automates : états accessibles, coaccessibles et utiles.
- Calcul de la fermeture epsilon.
- Transformation et conversion des automates.
- Complémentation et complétion des DFA.
- Élagage des états inutiles (`trim`).
- Conversion entre DFA, NFA et GNFA.
- Conversion des automates en expressions régulières.
- Conversion entre automates et grammaires.
- Visualisation graphique des automates.

## Exemple d'utilisation

Voici un exemple de création d'un automate déterministe étendu (`ExtendedDFA`) :

```python
from automata_extensions.fa.dfa import ExtendedDFA

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

# Analyser les états accessibles
print(automate.accessibles())

# Afficher les états utiles
print(automate.utiles())

# Visualiser l'automate
automate.display()
```


## Visualisation des automates

Le projet permet de représenter graphiquement les automates finis grâce à la bibliothèque **Graphviz**.

### 1. Création d'un graphe

La méthode `to_graphviz()` transforme un automate en graphe Graphviz.

```python
graphe = automate.to_graphviz()
```

### 2. Exportation d'un automate

La méthode `afficher()` permet d'enregistrer le graphe dans différents formats : PNG, SVG et PDF.

```python
automate.afficher(
    nom_fichier="mon_automate",
    format="png"
)
```

### 3. Personnalisation du graphe

Il est possible de modifier la direction, les couleurs et le titre.

```python
automate.afficher(
    nom_fichier="mon_automate",
    format="png",
    direction="TB",
    couleur_etat="yellow",
    couleur_final="pink",
    titre="Mon automate"
)
```

Directions disponibles :

- `LR` : gauche vers droite.
- `RL` : droite vers gauche.
- `TB` : haut vers bas.
- `BT` : bas vers haut.

### 4. Affichage dans Jupyter Notebook

La méthode `display()` permet d'afficher directement le graphe dans un notebook Jupyter.

```python
automate.display()
```

### 5. Dépendances

La visualisation nécessite :

- Le paquet Python `graphviz`.
- Le logiciel Graphviz installé sur le système.

Installation du paquet Python :

```bash
pip install graphviz
```

## Tests

Le projet utilise `pytest` pour vérifier le bon fonctionnement des fonctionnalités.

Pour lancer les tests depuis la racine du projet :

```bash
python -m pytest
```
