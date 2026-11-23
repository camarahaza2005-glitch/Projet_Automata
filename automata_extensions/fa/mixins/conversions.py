class ConversionMixin:
    """Fournit les méthodes de conversion des automates."""

    def reverse(self):
        """Construit un automate reconnaissant le langage inversé."""
        from ..nfa import ExtendedNFA

        etats = set(self.states)
        nouvelle_transitions = {etat: {} for etat in etats}

        # Inverser les transitions
        for etat, transitions in self.transitions.items():
            for symbole, destinations in transitions.items():
                if isinstance(destinations, (set, frozenset)):
                    suivants = destinations
                else:
                    suivants = {destinations}

                for destination in suivants:
                    nouvelle_transitions[destination].setdefault(
                        symbole, set()
                    ).add(etat)

        # Créer le nouvel état initial
        nouvel_etat_initial = "q_initial_inverse"

        while nouvel_etat_initial in etats:
            nouvel_etat_initial += "_"

        etats.add(nouvel_etat_initial)

        nouvelle_transitions[nouvel_etat_initial] = {
            "": set(self.final_states)
        }
        return ExtendedNFA(
            states=etats,
            input_symbols=self.input_symbols,
            transitions=nouvelle_transitions,
            initial_state=nouvel_etat_initial,
            final_states={self.initial_state}
        )

    def complete(self):
        """Complète un automate déterministe."""

        from automata.fa.dfa import DFA

        if not isinstance(self, DFA):
            raise TypeError("La méthode complete() est réservée aux DFA.")

        transitions_manquantes = []

        for etat in self.states:
            for symbole in self.input_symbols:
                if symbole not in self.transitions[etat]:
                    transitions_manquantes.append((etat, symbole))

        if not transitions_manquantes:
            return self

        # Création de l'état puits
        etat_puits = "q_puits"

        while etat_puits in self.states:
            etat_puits += "_"
        nouveaux_etats = set(self.states)
        nouveaux_etats.add(etat_puits)

        nouvelles_transitions = {
            etat: dict(transitions)
            for etat, transitions in self.transitions.items()
        }
        for etat, symbole in transitions_manquantes:
            nouvelles_transitions[etat][symbole] = etat_puits
        nouvelles_transitions[etat_puits] = {
            symbole: etat_puits
            for symbole in self.input_symbols
        }
        from ..dfa import ExtendedDFA

        return ExtendedDFA(
            states=nouveaux_etats,
            input_symbols=self.input_symbols,
            transitions=nouvelles_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )

    def complement(self):
        """Construit le complément du langage reconnu par un DFA."""

        from automata.fa.dfa import DFA
        from ..dfa import ExtendedDFA

        if not isinstance(self, DFA):
            raise TypeError("La méthode complement() est réservée aux DFA.")

        automate_complet = self.complete()

        nouveaux_etats_finaux = (
            automate_complet.states - automate_complet.final_states
        )

        return ExtendedDFA(
            states=automate_complet.states,
            input_symbols=automate_complet.input_symbols,
            transitions=automate_complet.transitions,
            initial_state=automate_complet.initial_state,
            final_states=nouveaux_etats_finaux
        )

    def trim(self):
        """Supprime les états inutiles de l'automate."""

        etats_utiles = self.utiles()

        if not etats_utiles:
            etats_utiles = {self.initial_state}

        nouvelles_transitions = {}

        for etat in etats_utiles:
            nouvelles_transitions[etat] = {}

            for symbole, destinations in self.transitions[etat].items():
                if isinstance(destinations, (set, frozenset)):
                    suivants = destinations & etats_utiles
                    if suivants:
                        nouvelles_transitions[etat][symbole] = suivants
                elif destinations in etats_utiles:
                    nouvelles_transitions[etat][symbole] = destinations

        nouveaux_etats_finaux = self.final_states & etats_utiles

        from automata.fa.dfa import DFA

        arguments = {
            "states": etats_utiles,
            "input_symbols": self.input_symbols,
            "transitions": nouvelles_transitions,
            "initial_state": self.initial_state,
            "final_states": nouveaux_etats_finaux
        }

        if isinstance(self, DFA):
            return self.__class__(**arguments, allow_partial=True)

        return self.__class__(**arguments)

    def to_dfa(self):
        """Convertit un NFA en DFA par la construction des sous-ensembles."""

        from automata.fa.nfa import NFA
        from ..dfa import ExtendedDFA

        if not isinstance(self, NFA):
            raise TypeError("La méthode to_dfa() est réservée aux NFA.")

        # Fermeture epsilon de l'état initial
        etat_initial = frozenset(
            self.epsilon_closure({self.initial_state})
        )

        etats = {etat_initial}
        transitions = {}
        file = [etat_initial]

        while file:
            etat = file.pop(0)
            transitions[etat] = {}

            for symbole in self.input_symbols:
                destinations = set()

                # Rassembler les destinations
                for sous_etat in etat:
                    suivantes = self.transitions[sous_etat].get(
                        symbole, set()
                    )

                    if not isinstance(suivantes, (set, frozenset)):
                        suivantes = {suivantes}

                    destinations.update(suivantes)

                # Calculer la fermeture epsilon des destinations
                if destinations:
                    destinations = self.epsilon_closure(destinations)

                nouvel_etat = frozenset(destinations)

                if nouvel_etat:
                    transitions[etat][symbole] = nouvel_etat

                    if nouvel_etat not in etats:
                        etats.add(nouvel_etat)
                        file.append(nouvel_etat)

        # Déterminer les états finaux
        etats_finaux = {
            etat for etat in etats
            if etat & self.final_states
        }

        return ExtendedDFA(
            states=etats,
            input_symbols=self.input_symbols,
            transitions=transitions,
            initial_state=etat_initial,
            final_states=etats_finaux,
            allow_partial=True
        )

    def to_nfa(self):
        """Convertit un DFA en NFA."""

        from automata.fa.dfa import DFA
        from ..nfa import ExtendedNFA

        if not isinstance(self, DFA):
            raise TypeError("La méthode to_nfa() est réservée aux DFA.")

        nouvelles_transitions = {}

        for etat, transitions in self.transitions.items():
            nouvelles_transitions[etat] = {}

            for symbole, destination in transitions.items():
                nouvelles_transitions[etat][symbole] = {destination}

        return ExtendedNFA(
            states=self.states,
            input_symbols=self.input_symbols,
            transitions=nouvelles_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )

    def to_gnfa(self):
        """Convertit un DFA ou un NFA en GNFA."""

        from automata.fa.dfa import DFA
        from automata.fa.nfa import NFA
        from ..gnfa import ExtendedGNFA
        from automata.fa.gnfa import GNFA

        if isinstance(self, DFA):
            automate_gnfa = GNFA.from_dfa(self)

        elif isinstance(self, NFA):
            automate_gnfa = GNFA.from_nfa(self)

        else:
            raise TypeError(
                "La méthode to_gnfa() est réservée aux DFA et aux NFA."
            )

        return ExtendedGNFA(
            states=automate_gnfa.states,
            input_symbols=automate_gnfa.input_symbols,
            transitions=automate_gnfa.transitions,
            initial_state=automate_gnfa.initial_state,
            final_state=automate_gnfa.final_state
        )

    def to_regex(self):
        """Convertit un automate en expression régulière."""

        from automata.fa.gnfa import GNFA
        from ..gnfa import ExtendedGNFA

        if isinstance(self, ExtendedGNFA):
            automate_gnfa = self
        else:
            automate_gnfa = self.to_gnfa()

        return GNFA.to_regex(automate_gnfa)