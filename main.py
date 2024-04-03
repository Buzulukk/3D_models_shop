import uuid

import command
from materials_files import material, photos, drawings, closeups, drawingsWithCloseups, approval
import state
import effect

if __name__ == '__main__':
    main_state = state.State()

    some_user_id = uuid.uuid4()
    some_order_id = uuid.uuid4()
    some_order_name = "test name of order"

    command1 = command.Command(some_user_id, command.Start())
    command2 = command.Command(some_user_id, command.CreateOrder(some_order_id))
    command3 = command.Command(some_user_id, command.SetOrderName(some_order_id, some_order_name))

    commands = [command1, command2, command3]

    for run_command in commands:
        effects = main_state.reduce(run_command.transform())

        for some_effect in effects:
            match some_effect:
                case effect.Nothing():
                    pass
                case effect.Message(message=message):
                    print(message)
                case effect.QuestionnaireQuestion(message=message, buttons=buttons):
                    print(message)
                    print(buttons)
                case effect.MaterialsSet(materials_set=materials_set):
                    print(materials_set)

        print(main_state)

    command_get_set = command.Command(some_user_id, command.QuestionnaireCheck(some_order_id))

    command_ask = command.Command(some_user_id, command.QuestionnaireAsk(some_order_id))

    command_answer_1 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, photos.Response.ResponseYes()))
    command_answer_2 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, drawings.Response.ResponseYes()))
    command_answer_3 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, closeups.Response.ResponseYes()))
    command_answer_4 = command.Command(some_user_id,
                                       command.QuestionnaireAnswer(some_order_id, approval.Response.ResponseYes()))
    questionnaire_answers = [command_answer_1, command_answer_2, command_answer_3, command_answer_4]
    questionnaire_answers_it = 0

    while main_state.reduce(command_get_set.transform()) == set():
        effects = main_state.reduce(command_ask.transform())
        for some_effect in effects:
            match some_effect:
                case effect.Nothing():
                    pass
                case effect.Message(message=message):
                    print(message)
                case effect.QuestionnaireQuestion(message=message, buttons=buttons):
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

        print(questionnaire_answers[questionnaire_answers_it].action.response)
        main_state.reduce(questionnaire_answers[questionnaire_answers_it].transform())
        questionnaire_answers_it += 1

    print("truly end")
