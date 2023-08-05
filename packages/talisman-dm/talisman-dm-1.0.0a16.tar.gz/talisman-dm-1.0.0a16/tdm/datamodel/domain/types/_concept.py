from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractDomainType, Identifiable


@dataclass(frozen=True)
class AbstractConceptType(Identifiable, AbstractDomainType):
    pass


@dataclass(frozen=True)
class ConceptType(AbstractConceptType):
    pass


@dataclass(frozen=True)
class DocumentType(AbstractConceptType):
    pass
