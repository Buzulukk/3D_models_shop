import effect

from materials_files.drawings import *
from materials_files.drawingsWithCloseups import *
from materials_files.material import *


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def view(self, deps):
    match self:
        case PhotosPresent(drawings=drawings):
            return drawings.view(deps)
        case PhotosAbsent(drawings_with_closeups=drawings_with_closeups):
            return drawings_with_closeups.view(deps)
        case PhotosUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "Есть ли у вас на данный момент качественные фотографии или рендеры вашего товара со всех сторон?",
                    ["Да", "Нет"]
                )
            ]


def action(self, response):
    match self:
        case PhotosPresent(drawings=drawings):
            return PhotosPresent(drawings.action(response))
        case PhotosAbsent(drawings_with_closeups=drawings_with_closeups):
            return PhotosAbsent(drawings_with_closeups.action(response))
        case PhotosUnknown():
            match response:
                case Response.ResponseYes():
                    return PhotosPresent(DrawingsUnknown())
                case Response.ResponseNo():
                    return PhotosAbsent(DrawingsWithCloseupsUnknown())


def get_set(self, material: Material):
    material_is_photos = False
    match material:
        case MaterialPhotos():
            material_is_photos = True

    match self:
        case PhotosPresent(drawings=drawings):
            return None if drawings.get_set(material) is None \
                else drawings.get_set(material) or material_is_photos
        case PhotosAbsent(drawings_with_closeups=drawings_with_closeups):
            return None if drawings_with_closeups.get_set(material) is None \
                else drawings_with_closeups.get_set(material) or not material_is_photos
        case PhotosUnknown():
            return None


class PhotosPresent:
    drawings: Drawings

    def __init__(self, drawings: Drawings):
        self.drawings = drawings

    view = view
    get_set = get_set
    action = action


class PhotosAbsent:
    drawings_with_closeups: DrawingsWithCloseups

    def __init__(self, drawings_with_closeups: DrawingsWithCloseups):
        self.drawings_with_closeups = drawings_with_closeups

    view = view
    get_set = get_set
    action = action


class PhotosUnknown:
    view = view
    get_set = get_set
    action = action


type Photos = PhotosPresent | PhotosAbsent | PhotosUnknown
