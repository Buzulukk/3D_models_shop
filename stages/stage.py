from stages import stageBase, stageQuest, stageMatter


class BaseReified:
    name: str

    def __init__(self, name: str):
        self.name = name


class QuestReified:
    materials_set: []

    def __init__(self, materials_set: []):
        self.materials_set = materials_set


type Action = stageBase.Action | stageQuest.Action | stageMatter.Action


def reduce(self, action: Action):
    return self.body.reduce(action)
    # match action:
    #     case stageBase.Action():
    #         self.body
    #     case stageQuest.Action():
    #         pass
    #     case stageMatter.Action():
    #         pass


class Base:
    body: stageBase.Base

    def __init__(self, body: stageBase.Base):
        self.body = body

    reduce = reduce


class Quest:
    base: BaseReified
    body: stageQuest.Quest

    def __init__(self, base: BaseReified, body: stageQuest.Quest):
        self.base = base
        self.body = body

    reduce = reduce


class Matter:
    base: BaseReified
    quest: QuestReified
    body: stageMatter.Matter

    def __init__(self, base: BaseReified, quest: QuestReified, body: stageMatter.Matter):
        self.base = base
        self.quest = quest
        self.body = body

    reduce = reduce


# def reduce(self, action: Action):
#     return self.reduce(action)


type Stage = Base | Quest | Matter

# Stage.reduce = reduce
