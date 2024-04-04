from dataclasses import dataclass
from typing import Any

import effect
from materials_files import material
from materials_files import photos


class View:
    pass


class Change:
    response: Any

    def __init__(self, response: Any):
        self.response = response


class GetSet:
    pass


type Action = View | Change | GetSet


def view(self, deps):
    return self.photos.view(deps)


def action(self, response):
    self.photos = self.photos.action(response)
    return [
        effect.Nothing()
    ]


def get_set(self):
    materials_set = []

    list_of_materials = [material.MaterialPhotos(), material.MaterialDrawings(), material.MaterialCloseups()]
    for el in list_of_materials:
        if self.photos.get_set(el):
            materials_set.append(el)

    return [
        effect.MaterialsSet(materials_set)
    ]


def reduce(self, action: Action):
    match action:
        case View():
            return self.view({'get_set_func': self.get_set})
        case Change(response=response):
            return self.action(response)
        case GetSet():
            return self.get_set()


@dataclass
class Materials:
    photos: photos.Photos
    materials_set: []

    def __init__(self, photos: photos.Photos):
        self.photos = photos
        self.materials_set = []

    reduce = reduce
    view = view
    action = action
    get_set = get_set
