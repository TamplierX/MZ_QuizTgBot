from aiogram.filters.state import State, StatesGroup


class FSMQuiz(StatesGroup):
    quiz_state = State()


class FSMAsk(StatesGroup):
    ask_state = State()


class FSMFeedback(StatesGroup):
    feedback_state = State()
