import time


def start(context, end_exercise):
    time.sleep(4)

    end_exercise()
    return context
