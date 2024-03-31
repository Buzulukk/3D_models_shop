import uuid

import command
import state
import effect

if __name__ == '__main__':
    main_state = state.State()

    # test
    # main_state.reduce(state.CreateUser(user_id=uuid.uuid4()))
    # main_state.users[list(main_state.users.keys())[0]].reduce(user.CreateOrder(order_id=uuid.uuid4()))
    # print(main_state)

    some_user_id = uuid.uuid4()
    some_order_id = uuid.uuid4()
    some_order_name = "test name of order"

    command1 = command.Command(some_user_id, command.Start())
    command2 = command.Command(some_user_id, command.CreateOrder(some_order_id))
    command3 = command.Command(some_user_id, command.SetOrderName(some_order_id, some_order_name))

    commands = [command1, command2, command3]

    for command in commands:
        effects = main_state.reduce(command.transform())

        for some_effect in effects:
            match some_effect:
                case effect.Nothing():
                    pass
                case effect.Message(message=message):
                    print(message)

        print(main_state)
