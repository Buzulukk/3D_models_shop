import uuid
from dataclasses import dataclass
from typing import Any

from materials_files.materials import Materials
from stages import stage, stageBase, stageQuest, stageMatter, stageContract


class Stage:
    action: stage.Action

    def __init__(self, action: stage.Action):
        self.action = action


type Action = Stage


def reduce(self, action: Action):
    match self.stage:
        case stage.Base(body=stageBase.Base(name=name)):
            if name is not None:  # move to the next stage if name is not None
                self.stage = stage.Quest(stage.BaseReified(name), stageQuest.Quest())
        case stage.Quest(base=base, body=body):
            match body:
                case stageQuest.Quest(materials=materials):
                    match action.action:
                        case stageMatter.GetInfoFromManager():  # move to the next stage if command from the next stage are called
                            materials_set = materials.get_set()
                            self.stage = stage.Matter(base, stage.QuestReified(materials_set), stageMatter.Matter())
        case stage.Matter(base=base, quest=quest, body=body):
            match action.action:
                case stageContract.CreateContract(price=price):
                    self.stage = stage.Contract(base, quest, stage.MatterReified(price),
                                                stageContract.Contract(None, None))

    match action:
        case Stage(action=action):
            return self.stage.reduce(action)


def view(self):
    match self.stage:
        case stage.Base(body=stageBase.Base(name=name)):
            if name is not None:  # move to the next stage if name is not None
                self.stage = stage.Quest(stage.BaseReified(name), stageQuest.Quest())

    return self.stage.view()


def view_files(self, material: Materials, materials_set: Any):
    return self.stage.view_files(material, materials_set)


def get_set(self):
    return self.stage.get_set()


@dataclass
class Order:
    order_id: uuid.UUID
    stage: stage.Stage

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id
        self.stage = stage.Base(stageBase.Base(None))

    reduce = reduce
    view = view
    view_files = view_files
    get_set = get_set
