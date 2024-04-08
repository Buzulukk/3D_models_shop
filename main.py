import uuid

import command
from materials_files import material, photos, drawings, closeups, drawingsWithCloseups, approval, skipToCloseups, \
    skipToApproval
import state
import effect


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

    command_get_set = command.Command(some_user_id, command.QuestionnaireCheck(some_order_id))
    command_ask = command.Command(some_user_id, command.QuestionnaireAsk(some_order_id))

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

    flag = True
    while flag:
        effects = main_state.reduce(command_ask.transform())
        for some_effect in effects:
            match some_effect:
                case effect.Nothing():
                    pass
                case effect.Message(message=message):
                    print(message)
                case effect.MessageWithButtons(message=message, buttons=buttons):
                    print(message)
                    print(buttons)
                case effect.MaterialsSet(materials_set=materials_set):
                    for el in materials_set:
                        match el:
                            case material.MaterialPhotos():
                                print("• Фото товара")
                            case material.MaterialDrawings():
                                print("• Чертежи товара")
                            case material.MaterialCloseups():
                                print("• Фото материалов")
                case effect.StopQuestionnaire():
                    flag = False
                case effect.RepeatQuestionnaire():
                    main_state = main_state_before_questionnaire_backup
                    flag = False

        if not flag:
            break

        print(questionnaire_answers[questionnaire_answers_it].action.response)
        main_state.reduce(questionnaire_answers[questionnaire_answers_it].transform())
        questionnaire_answers_it += 1

    materials_set = main_state.reduce(command_get_set.transform())[0].materials_set
    for active_material in materials_set:
        command_files = command.Command(some_user_id,
                                        command.UploadFilesAsk(some_order_id, active_material, materials_set))
        deal_with_effects(main_state.reduce(command_files.transform()))

        command_files_saved = command.Command(some_user_id, command.UploadFilesMarkSaved(some_order_id, active_material,
                                                                                         uuid.uuid4()))

    command4 = command.Command(some_user_id, command.SendInfoToManager(some_order_id))
    command5 = command.Command(some_user_id, command.GetInfoFromManager(some_order_id, some_price))
    command6 = command.Command(some_user_id, command.CreateContract(some_order_id, some_price))
    command7 = command.Command(some_user_id,
                               command.AsCompany(some_order_id, some_full_name, some_position, some_taxpayer_number))
    commands = [command4, command5, command6, command7]
    for run_command in commands:
        deal_with_effects(main_state.reduce(run_command.transform()))

    print(main_state)
    print("truly end")
