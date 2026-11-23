from collections import deque
from collections.abc import Hashable
from typing import Optional, Set

class AnalyseMixin:
    """Méthodes d'analyse des automates finis."""

    
    def accessibles(self, depart=None):
        """Calcule les états accessibles dans un DFA ou un NFA."""

        if depart is None:
            depart = self.initial_state

        visites = set()
        file = deque([depart])

        while file:
            etat = file.popleft()

            if etat not in visites:
                visites.add(etat)

                for destinations in self.transitions[etat].values():

                    # Un DFA possède une destination unique.
                    if not isinstance(destinations, (set, frozenset)):
                        destinations = {destinations}

                    for suivant in destinations:
                        if suivant not in visites:
                            file.append(suivant)

        return visites


    
    def coaccessibles(self):
        """
        Calcule les états pouvant atteindre un état final
        dans un DFA ou un NFA.
        """

        predecesseurs = {
            etat: set() for etat in self.states
        }

        for etat in self.states:
            for destinations in self.transitions[etat].values():

                # Une transition peut avoir une ou plusieurs destinations.
                if isinstance(destinations, (set, frozenset)):
                    suivants = destinations
                else:
                    suivants = {destinations}

                for suivant in suivants:
                    predecesseurs[suivant].add(etat)

        visites = set(self.final_states)
        file = deque(self.final_states)

        while file:
            etat = file.popleft()

            for precedent in predecesseurs[etat]:
                if precedent not in visites:
                    visites.add(precedent)
                    file.append(precedent)

        return visites


    def utiles(self) -> Set[Hashable]:
        """
        Calcule les états utiles de l'automate.

        Un état utile est à la fois accessible
        et coaccessible.

        Returns:
            Un ensemble contenant les états utiles.

        Complexité : O(|Q| + |E|).
        """

        return self.accessibles() & self.coaccessibles()

    def epsilon_closure(self, etats):
        """Calcule les états accessibles par zéro ou plusieurs transitions epsilon."""

        fermeture = set(etats)
        file = list(etats)

        while file:
            etat = file.pop(0)

            destinations = self.transitions[etat].get("", set())

            if not isinstance(destinations, (set, frozenset)):
                destinations = {destinations}

            for destination in destinations:
                if destination not in fermeture:
                    fermeture.add(destination)
                    file.append(destination)

        return fermeture
        

        