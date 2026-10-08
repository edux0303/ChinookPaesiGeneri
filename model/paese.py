from dataclasses import dataclass


@dataclass
class Paese:
    nome: str
    venduti: int = 0      # brani del genere scelto acquistati dai clienti del paese

    def __hash__(self):
        return hash(self.nome)

    def __eq__(self, other):
        return isinstance(other, Paese) and self.nome == other.nome

    def __str__(self):
        return self.nome