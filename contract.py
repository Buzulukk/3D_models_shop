import datetime


class IndividualContract:
    full_name: str
    birthday: datetime.datetime
    passport_number: str
    issued_by: str
    issued_by_number: str
    address: str

    def __init__(self, full_name: str, birthday: datetime.datetime, passport_number: str, issued_by: str,
                 issued_by_number: str, address: str):
        self.full_name = full_name
        self.birthday = birthday
        self.passport_number = passport_number
        self.issued_by = issued_by
        self.issued_by_number = issued_by_number
        self.address = address


class CompanyContract:
    full_name: str
    position: str
    taxpayer_number: str

    def __init__(self, full_name: str, position: str, taxpayer_number: str):
        self.full_name = full_name
        self.position = position
        self.taxpayer_number = taxpayer_number


type Contract = IndividualContract | CompanyContract
