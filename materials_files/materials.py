import uuid
from dataclasses import dataclass
from typing import Any

import effect
from materials_files.material import *
from materials_files.photos import Photos
from materials_files.file import File


class Change:
    response: Any

    def __init__(self, response: Any):
        self.response = response


class UploadFilesAsk:
    material: Material
    materials_set: []

    def __init__(self, material: Material, materials_set: []):
        self.material = material
        self.materials_set = materials_set


class UploadFilesMarkSaved:
    file_id: uuid.UUID
    material: Material

    def __init__(self, file_id: uuid.UUID, material: Material):
        self.file_id = file_id
        self.material = material


class UploadFilesReady:
    pass


type Action = Change | UploadFilesAsk | UploadFilesMarkSaved | UploadFilesReady


def view(self):
    return self.photos.view({'get_set_func': self.get_set})


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

    return materials_set


def reduce(self, action: Action):
    match action:
        case Change(response=response):
            return self.action(response)
        case UploadFilesAsk(material=material, materials_set=materials_set):
            match material:
                case MaterialPhotos():
                    buttons = []
                    for el in materials_set:
                        match el:
                            case MaterialDrawings():
                                buttons.append("Загрузить файлы чертежей")
                            case MaterialCloseups():
                                buttons.append("Загрузить фотографии материалов")
                    buttons.append("Готово")
                    return [
                        effect.MessageWithButtons(
                            "Пожалуйста, загрузите файлы фотографий и/или рендеров вашего товара",
                            buttons
                        )
                    ]
                case MaterialDrawings():
                    buttons = []
                    for el in materials_set:
                        match el:
                            case MaterialPhotos():
                                buttons.append("Загрузить фотографии товара")
                            case MaterialCloseups():
                                buttons.append("Загрузить фотографии материалов")
                    buttons.append("Готово")
                    return [
                        effect.MessageWithButtons(
                            "Пожалуйста, загрузите файлы чертежей вашего товара",
                            buttons
                        )
                    ]
                case MaterialCloseups():
                    buttons = []
                    for el in materials_set:
                        match el:
                            case MaterialPhotos():
                                buttons.append("Загрузить фотографии товара")
                            case MaterialDrawings():
                                buttons.append("Загрузить файлы чертежей")
                    buttons.append("Готово")
                    return [
                        effect.MessageWithButtons(
                            "Пожалуйста, загрузите файлы фотографий материалов вашего товара",
                            buttons
                        )
                    ]
        case UploadFilesMarkSaved(file_id=file_id, material=material):
            match material:
                case MaterialPhotos():
                    self.files['photos'].append(File(file_id))
                    return [
                        effect.Nothing()
                    ]
                case MaterialDrawings():
                    self.files['drawings'].append(File(file_id))
                    return [
                        effect.Nothing()
                    ]
                case MaterialCloseups():
                    self.files['closeups'].append(File(file_id))
                    return [
                        effect.Nothing()
                    ]
        case UploadFilesReady():
            for el in self.materials_set:
                match el:
                    case MaterialPhotos():
                        if len(self.files['photos']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы фотографий вашего товара. Загрузите их, чтобы продолжить."
                                )
                            ]
                    case MaterialDrawings():
                        if len(self.files['drawings']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы чертежей вашего товара. Загрузите их, чтобы продолжить."
                                )
                            ]
                    case MaterialCloseups():
                        if len(self.files['closeups']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы фотографий материалов. Загрузите их, чтобы продолжить."
                                )
                            ]


@dataclass
class Materials:
    photos: Photos
    files: dict

    def __init__(self, photos: Photos):
        self.photos = photos
        self.files = {'photos': [], 'drawings': [], 'closeups': []}

    reduce = reduce
    view = view
    action = action
    get_set = get_set
