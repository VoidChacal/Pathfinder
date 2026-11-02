import time


LOG = "/caminho/device_events.log"


def watch_log():

    with open(LOG, "r") as file:

        file.seek(0,2)

        while True:

            line = file.readline()

            if line:

                process_event(line)

            time.sleep(1)


def process_event(line):

    print("[DEVICE EVENT]", line)


watch_log()
