import uuid
from dataclasses import dataclass
from typing import Any

import command
import effect
from materials_files.material import *
from materials_files.photos import Photos
from materials_files.file import File


class Change:
    response: Any

    def __init__(self, response: Any):
        self.response = response


class UploadFilesMarkSaved:
    file_id: uuid.UUID
    material: Material

    def __init__(self, file_id: uuid.UUID, material: Material):
        self.file_id = file_id
        self.material = material


class UploadFilesReady:
    materials_set: []

    def __init__(self, materials_set: []):
        self.materials_set = materials_set


type Action = Change | UploadFilesMarkSaved | UploadFilesReady


def view(self):
    return self.photos.view({'get_set_func': self.get_set})


def view_files(self, material: Material, materials_set: Any):
    match material:
        case MaterialPhotos():
            self.active_files_type = MaterialPhotos()

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
            self.active_files_type = MaterialDrawings()

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
            self.active_files_type = MaterialCloseups()

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


def action(self, response):
    self.photos = self.photos.action(response)
    return [
        effect.View()
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
        case UploadFilesReady(materials_set=materials_set):
            for el in materials_set:
                match el:
                    case MaterialPhotos():
                        if len(self.files['photos']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы фотографий вашего товара. Нажмите на соответствующую кнопку в меню и загрузите файлы"
                                )
                            ]
                    case MaterialDrawings():
                        if len(self.files['drawings']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы чертежей вашего товара. Нажмите на соответствующую кнопку в меню и загрузите файлы"
                                )
                            ]
                    case MaterialCloseups():
                        if len(self.files['closeups']) == 0:
                            return [
                                effect.Message(
                                    "Вы не загрузили файлы фотографий материалов. Нажмите на соответствующую кнопку в меню и загрузите файлы"
                                )
                            ]
            self.files_ready = True
            return [
                effect.Message(
                    "Отлично! Ваш заказ принят на расчёт стоимости. Мы свяжемся с вами в течении одного рабочего дня."),
                effect.SendInfoToManager()
            ]


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match tg_message["message"]["text"]:
        case "Загрузить фотографии товара":
            return command.Command(user_id, command.ViewFiles(MaterialPhotos()))
        case "Загрузить файлы чертежей":
            return command.Command(user_id, command.ViewFiles(MaterialDrawings()))
        case "Загрузить фотографии материалов":
            return command.Command(user_id, command.ViewFiles(MaterialCloseups()))
        case "Готово":
            return command.Command(user_id, command.UploadFilesReady(active_order, self.get_set()))
        case _:
            return self.photos.response(active_order, tg_message)


@dataclass
class Materials:
    active_files_type: Material
    photos: Photos
    files: dict
    files_ready: bool

    def __init__(self, photos: Photos):
        self.photos = photos
        self.files = {'photos': [], 'drawings': [], 'closeups': []}
        self.files_ready = False

    reduce = reduce
    response = response
    view = view
    view_files = view_files
    action = action
    get_set = get_set
