from __future__ import annotations

from enum import Enum, auto
from collections import OrderedDict

class Term:
    class Type (Enum):
        Quarter     = auto()
        Semester    = auto()
        Trimester   = auto()

class Course:
    id:             Course.ID
    department:     Course.Department
    prefix:         Course.Prefix
    number:         str
    title:          str
    units:          Course.Units
    offering:       Course.Offering
    crosslisted:    list[Course.ID]
    outline:        bool

    class ID:
        id:     int
        stable: int

    class Prefix:
        id:     int
        code:   str
        name:   str

    class Department:
        id:     str
        name:   str

    class Units:
        min:    float
        max:    float

    class Offering:
        start:  Term
        end:    Optional[Term]
        active: bool

    class Transferrable:
        CSU:    bool
        UC:     bool

    def __eq__(self, other):
        match other:
            case Course():  return self.id.id == other.id.id
            case _:         raise NotImplementedError    

class Institution:
    id:         int
    code:       str
    names:      OrderedDict[Term, str]
    type:       Institution.Type
    terms:      OrderedDict[Term, Term.Type]
    start:      Term
    location:   Institution.Location

    class Location:
        latitude:   float
        longitude:  float

    class Type (Enum):
        Community   = auto()
        University  = auto()


class Agreement: ...