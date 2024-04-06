from materials_files import materials, photos


class Materials:
    action: materials.Action

    def __init__(self, action: materials.Action):
        self.action = action


type Action = Materials


def reduce(self, action: Action):
    match action:
        case Materials(action=action):
            return self.materials.reduce(action)


class Quest:
    materials: materials.Materials

    def __init__(self):
        self.materials = materials.Materials(photos.PhotosUnknown())

    reduce = reduce
