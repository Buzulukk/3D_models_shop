import uuid

import state
import user

if __name__ == '__main__':
    main_state = state.State()

    # test
    main_state.reduce(state.CreateUser(user_id=uuid.uuid4()))
    main_state.users[list(main_state.users.keys())[0]].reduce(user.CreateOrder(order_id=uuid.uuid4()))
    print(main_state)
