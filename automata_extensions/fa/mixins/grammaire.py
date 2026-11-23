class GrammaireMixin:
    """
    Fournit les méthodes liées aux grammaires.

    Cette classe regroupera les méthodes permettant
    de convertir un automate en grammaire et inversement.
    """

    def to_grammar(self):
        """Convertit un automate en grammaire régulière à droite."""

        regles = {}

        for etat in self.states:
            regles[etat] = set()

            for symbole, destinations in self.transitions[etat].items():

                if isinstance(destinations, (set, frozenset)):
                    suivants = destinations
                else:
                    suivants = {destinations}

                for suivant in suivants:
                    regles[etat].add(symbole + str(suivant))

            if etat in self.final_states:
                regles[etat].add("")

        return {
            "non_terminaux": self.states,
            "terminaux": self.input_symbols,
            "symbole_initial": self.initial_state,
            "regles": regles
        }


    @classmethod
    def from_grammar(cls, grammaire):
        """Construit un automate non déterministe à partir d'une grammaire."""

        from ..nfa import ExtendedNFA

        non_terminaux = grammaire["non_terminaux"]
        terminaux = grammaire["terminaux"]
        symbole_initial = grammaire["symbole_initial"]
        if symbole_initial not in non_terminaux:
            raise ValueError(
                "Le symbole initial doit appartenir aux non-terminaux."
            )
        regles = grammaire["regles"]

        transitions = {
            etat: {}
            for etat in non_terminaux
        }

        etats_finaux = set()

        for etat, productions in regles.items():
            for production in productions:

                # Une règle vide indique un état final.
                if production == "":
                    etats_finaux.add(etat)
                    continue

                # Une règle composée uniquement d'un non-terminal
                # correspond à une transition epsilon.
                if production in non_terminaux:
                    transitions[etat].setdefault("", set()).add(production)
                    continue
                # Une règle composée uniquement d'un terminal
                # mène vers un nouvel état final.
                if production in terminaux:
                    etat_final = f"{etat}_final"

                    while etat_final in non_terminaux:
                        etat_final += "_"

                    non_terminaux = set(non_terminaux) | {etat_final}
                    transitions[etat_final] = {}
                    etats_finaux.add(etat_final)

                    transitions[etat].setdefault(production, set()).add(etat_final)
                    continue

                # On recherche le terminal au début de la règle.
                correspondance = None

                for symbole in sorted(terminaux, key=len, reverse=True):
                    if production[:len(symbole)] == symbole:
                        destination = production[len(symbole):]

                        if destination in non_terminaux:
                            correspondance = (symbole, destination)
                            break

                if correspondance is None:
                    raise ValueError(
                        f"Règle de grammaire invalide : {production}"
                    )

                symbole, destination = correspondance

                transitions[etat].setdefault(symbole, set()).add(destination)

        return ExtendedNFA(
            states=non_terminaux,
            input_symbols=terminaux,
            transitions=transitions,
            initial_state=symbole_initial,
            final_states=etats_finaux
        )
