from graphviz import Digraph
class VisualisationMixin:
    """
    Fournit les méthodes permettant de visualiser les automates.

    Cette classe regroupera les méthodes d'exportation
    des automates vers différents formats graphiques.
    """

    def to_graphviz(
        self,
        direction="LR",
        couleur_etat="lightblue",
        couleur_final="lightgreen",
        titre="Automate fini"
    ):
        """
        Transforme l'automate en graphe Graphviz.

        Les états sont représentés par des cercles.
        Les états finaux ont un double cercle.
        Les transitions sont représentées par des flèches.
        """
        directions_valides = {"LR", "RL", "TB", "BT"}

        if direction not in directions_valides:
            raise ValueError(
                "Direction invalide. Choisissez LR, RL, TB ou BT."
            )

        graphe = Digraph(
            graph_attr={
                "rankdir": direction,
                "label": titre,
                "labelloc": "t"
            }
        )

        # Définir la forme des états
        for etat in self.states:

            if etat in self.final_states:
                forme = "doublecircle"
            else:
                forme = "circle"

            couleur = (
                couleur_final
                if etat in self.final_states
                else couleur_etat
            )

            graphe.node(
                str(etat),
                shape=forme,
                style="filled",
                fillcolor=couleur
            )

        # Ajouter une flèche vers l'état initial
        graphe.node("__depart__", shape="none", label="")
        graphe.edge("__depart__", str(self.initial_state))

        # Ajouter les transitions
        for etat, transitions in self.transitions.items():

            for symbole, destinations in transitions.items():

                if isinstance(destinations, (set, frozenset)):
                    suivants = destinations
                else:
                    suivants = {destinations}

                for suivant in suivants:
                    graphe.edge(
                        str(etat),
                        str(suivant),
                        label=str(symbole) if symbole else "ε"
                    )

        return graphe

    def afficher(
        self,
        nom_fichier="automate",
        format="png",
        nettoyer=True,
        direction="LR",
        couleur_etat="lightblue",
        couleur_final="lightgreen",
        titre="Automate fini"
    ):
        """
        Exporte l'automate dans un fichier graphique.

        Permet de personnaliser la direction, les couleurs
        et le titre du graphe.
        """
        formats_valides = {"png", "svg", "pdf"}

        if format not in formats_valides:
            raise ValueError(
                "Format invalide. Choisissez png, svg ou pdf."
            )

        graphe = self.to_graphviz(
            direction=direction,
            couleur_etat=couleur_etat,
            couleur_final=couleur_final,
            titre=titre
        )

        return graphe.render(
            filename=nom_fichier,
            format=format,
            cleanup=nettoyer
        )

    def display(
        self,
        direction="LR",
        couleur_etat="lightblue",
        couleur_final="lightgreen",
        titre="Automate fini"
    ):
        """
        Affiche directement l'automate dans un notebook Jupyter.
        """

        graphe = self.to_graphviz(
            direction=direction,
            couleur_etat=couleur_etat,
            couleur_final=couleur_final,
            titre=titre
        )

        return graphe