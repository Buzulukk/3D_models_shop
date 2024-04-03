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


def reduce(self, action: Action):
    match action:
        case View():
            return self.photos.view()
        case Change(response=response):
            self.photos = self.photos.action(response)
            return [
                effect.Nothing()
            ]
        case GetSet():
            materials_set = set()

            list_of_materials = [material.MaterialPhotos(), material.MaterialDrawings(), material.MaterialCloseups()]
            for el in list_of_materials:
                if self.photos.get_set(el):
                    materials_set.add(el)

            return materials_set


@dataclass
class Materials:
    photos: photos.Photos
    materials_set: set[material.Material]

    def __init__(self, photos: photos.Photos):
        self.photos = photos
        self.materials_set = set[material.Material]()

    reduce = reduce
