from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

class Cards:
    def __init__(self, card=None, set=None, type=None, supertype=None, subtype=None, changelog=None):
        self.card = Card.find(card)
        self.set = set
        self.type = type
        self.supertype = supertype
        self.subtype = subtype
        self.changelog = changelog
