import uuid

import command
from materials_files import material, photos, drawings, closeups, drawingsWithCloseups, approval, skipToCloseups, \
    skipToApproval
import state
import effect
import contract


def deal_with_effects(effects: []):
    for some_effect in effects:
        match some_effect:
            case effect.Nothing():
                pass
            case effect.Message(message=message):
                print(message)
            case effect.MessageWithButtons(message=message, buttons=buttons):
                print(message)
                print(buttons)
            case effect.Contract(contract=some_contract):
                match some_contract:
                    case contract.IndividualContract(full_name=full_name, birthday=birthday,
                                                     passport_number=passport_number, issued_by=issued_by,
                                                     issued_by_number=issued_by_number, address=address):
                        print(full_name, '•', birthday, '•', passport_number, '•', issued_by, '•', issued_by_number,
                              '•', address)
                    case contract.CompanyContract(full_name=full_name, position=position,
                                                  taxpayer_number=taxpayer_number):
                        print(full_name, '•', position, '•', taxpayer_number)


if __name__ == '__main__':
    main_state = state.State()

    some_user_id = uuid.uuid4()
    some_order_id = uuid.uuid4()
    some_order_name = "test name of order"
    some_price = 4200
    some_full_name = "Ryan Thomas Gosling"
    some_position = "Hollywood actor"
    some_taxpayer_number = "0123456789"

    command1 = command.Command(some_user_id, command.Start())
    command2 = command.Command(some_user_id, command.CreateOrder(some_order_id))
    command3 = command.Command(some_user_id, command.SetOrderName(some_order_id, some_order_name))

    commands = [command1, command2, command3]

    for run_command in commands:
        deal_with_effects(main_state.reduce(run_command.transform()))

    main_state_before_questionnaire_backup = main_state

    command_answer_1 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, photos.Response.ResponseYes()))
    command_answer_2 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, drawings.Response.ResponseYes()))
    command_answer_3 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id,
                                                                   closeups.Response.ResponseYes()))
    command_answer_4 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, approval.Response.ResponseYes()))
    questionnaire_answers = [command_answer_1, command_answer_2, command_answer_3, command_answer_4]
    questionnaire_answers_it = 0

    while True:
        questionnaire_question = main_state.view(some_user_id, some_order_id)

        print(questionnaire_question['message'])
        print(questionnaire_question.get('buttons'))

        if questionnaire_question['message'] == "Завершение опроса":
            break

        print(questionnaire_answers[questionnaire_answers_it].action.response)
        main_state.reduce(questionnaire_answers[questionnaire_answers_it].transform())
        questionnaire_answers_it += 1

    materials_set = main_state.get_set(some_user_id, some_order_id)
    for active_material in materials_set:
        deal_with_effects(main_state.view_files(some_user_id, some_order_id, active_material, materials_set))

        command_files_saved = command.Command(some_user_id, command.UploadFilesMarkSaved(some_order_id, active_material,
                                                                                         uuid.uuid4()))
        deal_with_effects(main_state.reduce(command_files_saved.transform()))

    command_files_ready = command.Command(some_user_id, command.UploadFilesReady(some_order_id, materials_set))
    deal_with_effects(main_state.reduce(command_files_ready.transform()))

    command4 = command.Command(some_user_id, command.GetInfoFromManager(some_order_id, some_price))
    command5 = command.Command(some_user_id, command.CreateContract(some_order_id, some_price))
    command6 = command.Command(some_user_id,
                               command.AsCompany(some_order_id, some_full_name, some_position, some_taxpayer_number))
    command7 = command.Command(some_user_id, command.SendContract(some_order_id))
    command8 = command.Command(some_user_id, command.SendContractToManager(some_order_id))
    command9 = command.Command(some_user_id, command.PrePayment(some_order_id, some_price))
    command10 = command.Command(some_user_id, command.PrePaymentComplete(some_order_id))
    commands = [command4, command5, command6, command7, command8, command9, command10]
    for run_command in commands:
        deal_with_effects(main_state.reduce(run_command.transform()))

    print()
    print(main_state)
    print("truly end")
