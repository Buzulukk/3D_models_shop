import uuid

import command
import state

if __name__ == '__main__':
    main_state = state.State()

    # test
    # main_state.reduce(state.CreateUser(user_id=uuid.uuid4()))
    # main_state.users[list(main_state.users.keys())[0]].reduce(user.CreateOrder(order_id=uuid.uuid4()))
    # print(main_state)

    some_user_id = uuid.uuid4()

    command1 = command.Command(some_user_id, command.Start())

    commands = [command1]

    for command in commands:
        main_state.reduce(command.transform())

    print(main_state)
