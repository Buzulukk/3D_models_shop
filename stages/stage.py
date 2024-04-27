from typing import Any

from materials_files.materials import Materials
from stages import stageBase, stageQuest, stageMatter, stageContract


class BaseReified:
    name: str

    def __init__(self, name: str):
        self.name = name


class QuestReified:
    materials_set: []

    def __init__(self, materials_set: []):
        self.materials_set = materials_set


class MatterReified:
    price: int

    def __init__(self, price: int):
        self.price = price


type Action = stageBase.Action | stageQuest.Action | stageMatter.Action | stageContract.Action


def reduce(self, action: Action):
    return self.body.reduce(action)


def view(self):
    return self.body.view()


def view_files(self, material: Materials, materials_set: Any):
    return self.body.view_files(material, materials_set)


def get_set(self):
    return self.body.get_set()


def ask_info_for_contract(self):
    return self.body.ask_info_for_contract()


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
    view = view
    view_files = view_files
    get_set = get_set


class Matter:
    base: BaseReified
    quest: QuestReified
    body: stageMatter.Matter

    def __init__(self, base: BaseReified, quest: QuestReified, body: stageMatter.Matter):
        self.base = base
        self.quest = quest
        self.body = body

    reduce = reduce


class Contract:
    base: BaseReified
    quest: QuestReified
    matter: MatterReified
    body: stageContract.ContractInfo

    def __init__(self, base: BaseReified, quest: QuestReified, matter: MatterReified, body: stageContract.ContractInfo):
        self.base = base
        self.quest = quest
        self.matter = matter
        self.body = body

    reduce = reduce
    ask_info_for_contract = ask_info_for_contract


type Stage = Base | Quest | Matter | Contract
