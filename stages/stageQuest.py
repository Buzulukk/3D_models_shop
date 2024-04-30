from typing import Any

from materials_files import materials, photos


class Materials:
    action: materials.Action

    def __init__(self, action: materials.Action):
        self.action = action


type Action = Materials


def reduce(self, action: Action):
    return self.materials.reduce(action.action)


def response(self, active_order, tg_message):
    return self.materials.response(active_order, tg_message)


def view(self):
    return self.materials.view()


def view_files(self, material: Materials, materials_set: Any):
    return self.materials.view_files(material, materials_set)


def get_set(self):
    return self.materials.get_set()


class Quest:
    materials: materials.Materials

    def __init__(self):
        self.materials = materials.Materials(photos.PhotosUnknown())

    reduce = reduce
    response = response
    view = view
    view_files = view_files
    get_set = get_set
