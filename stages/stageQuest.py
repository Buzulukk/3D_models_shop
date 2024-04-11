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


def view(self):
    return self.materials.view()


def get_set(self):
    return self.materials.get_set()


class Quest:
    materials: materials.Materials

    def __init__(self):
        self.materials = materials.Materials(photos.PhotosUnknown())

    reduce = reduce
    view = view
    get_set = get_set
