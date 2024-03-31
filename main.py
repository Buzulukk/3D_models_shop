import uuid

import command
import order_materials
import state
import effect

if __name__ == '__main__':
    main_state = state.State()

    # test
    some_user_id = uuid.uuid4()
    some_order_id = uuid.uuid4()
    some_order_name = "test name of order"

    # questionnaire answers
    answer_1 = "Да"
    answer_2 = "Да"

    command_start = command.Command(some_user_id, command.Start())
    command_create_order = command.Command(some_user_id, command.CreateOrder(some_order_id))
    command_set_order_name = command.Command(some_user_id, command.SetOrderName(some_order_id, some_order_name))
    command_questionnaire_1 = command.Command(some_user_id, command.Questionnaire(some_order_id, ""))
    command_questionnaire_2 = command.Command(some_user_id, command.Questionnaire(some_order_id, answer_1))
    command_questionnaire_3 = command.Command(some_user_id, command.Questionnaire(some_order_id, ""))
    command_questionnaire_4 = command.Command(some_user_id, command.Questionnaire(some_order_id, answer_2))

    commands = [command_start, command_create_order, command_set_order_name, command_questionnaire_1,
                command_questionnaire_2, command_questionnaire_3, command_questionnaire_4]

    for command in commands:
        effects = main_state.reduce(command.transform())

        for some_effect in effects:
            match some_effect:
                case effect.Nothing():
                    pass
                case effect.Message(message=message):
                    print(message)
                case effect.QuestionnaireQuestion(message=message, buttons=buttons):
                    print(message)
                    print(buttons)

        print(main_state)
