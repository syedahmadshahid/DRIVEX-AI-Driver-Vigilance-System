import time

distraction_start = None

def check_distraction(head_status):

    global distraction_start

    if head_status in ["Left", "Right"]:

        if distraction_start is None:
            distraction_start = time.time()

        elapsed = time.time() - distraction_start

        if elapsed >= 3:
            return "Critical"

        elif elapsed >= 1.5:
            return "Warning"

    else:
        distraction_start = None

    return "Normal"