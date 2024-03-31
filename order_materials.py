from dataclasses import dataclass

import effect


def reduce(self, answer: str):
    match self:
        case OrderMaterials(None, None, None):
            if answer == "":
                return [effect.QuestionnaireQuestion(
                    "Есть ли у вас на данный момент качественные фотографии или рендеры вашего товар со всех сторон?",
                    ["Да", "Нет"])
                ]
            else:
                match answer:
                    case "Да":
                        self.has_product_photos = True
                        return [
                            effect.Nothing
                        ]
                    case "Нет":
                        self.has_product_photos = False
                        return [
                            effect.Nothing
                        ]
        case OrderMaterials(True, None, None):
            if answer == "":
                return [
                    effect.QuestionnaireQuestion(
                        "Есть ли у вас чертежи товара с указанием размеров?",
                        ["Да", "Нет"])
                ]
            else:
                match answer:
                    case "Да":
                        self.has_drawings = True
                        return [
                            effect.Nothing
                        ]
                    case "Нет":
                        self.has_drawings = False
                        return [
                            effect.Nothing
                        ]


@dataclass
class OrderMaterials:
    has_product_photos: bool
    has_drawings: bool
    has_material_photos: bool

    def __init__(self, has_product_photos: bool, has_drawings: bool, has_material_photos: bool):
        self.has_product_photos = has_product_photos
        self.has_drawings = has_drawings
        self.has_material_photos = has_material_photos

    reduce = reduce
