import uuid
from dataclasses import dataclass

from stages import stage, stageBase, stageQuest, stageMatter


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
                    materials_set = materials.get_set()[0].materials_set
                    match action.action:
                        case stageMatter.SendInfoToManager():  # move to the next stage if command from the next stage are called
                            self.stage = stage.Matter(base, stage.QuestReified(materials_set), stageMatter.Matter())

    match action:
        case Stage(action=action):
            return self.stage.reduce(action)


@dataclass
class Order:
    order_id: uuid.UUID
    stage: stage.Stage

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id
        self.stage = stage.Base(stageBase.Base(None))

    reduce = reduce
