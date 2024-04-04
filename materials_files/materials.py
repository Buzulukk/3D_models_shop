from dataclasses import dataclass
from typing import Any

import effect
from materials_files.material import *
from materials_files.photos import Photos


class View:
    pass


class Change:
    response: Any

    def __init__(self, response: Any):
        self.response = response


class GetSet:
    pass


class UploadFilesAsk:
    material: Material

    def __init__(self, material: Material):
        self.material = material


class UploadFilesMarkSaved:
    material: Material

    def __init__(self, material: Material):
        self.material = material


type Action = View | Change | GetSet | UploadFilesAsk | UploadFilesMarkSaved


def view(self, deps):
    return self.photos.view(deps)


def action(self, response):
    self.photos = self.photos.action(response)
    return [
        effect.Nothing()
    ]


def get_set(self):
    materials_set = []

    list_of_materials = [MaterialPhotos(), MaterialDrawings(), MaterialCloseups()]
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
        case UploadFilesAsk(material=material):
            match material:
                case MaterialPhotos():
                    return [
                        effect.Message("Пожалуйста, загрузите файлы фотографий и/или рендеров вашего товара")
                    ]
                case MaterialDrawings():
                    return [
                        effect.Message("Пожалуйста, загрузите файлы чертежей вашего товара")
                    ]
                case MaterialCloseups():
                    return [
                        effect.Message("Пожалуйста, загрузите файлы фотографий материалов вашего товара")
                    ]
        case UploadFilesMarkSaved(material=material):
            match material:
                case MaterialPhotos():
                    self.materials_saved.append(MaterialPhotos())
                    return [
                        effect.Nothing()
                    ]
                case MaterialDrawings():
                    self.materials_saved.append(MaterialDrawings())
                    return [
                        effect.Nothing()
                    ]
                case MaterialCloseups():
                    self.materials_saved.append(MaterialCloseups())
                    return [
                        effect.Nothing()
                    ]


@dataclass
class Materials:
    photos: Photos
    materials_set: []
    materials_saved: []

    def __init__(self, photos: Photos):
        self.photos = photos
        self.materials_set = []
        self.materials_saved = []

    reduce = reduce
    view = view
    action = action
    get_set = get_set
