import os


class special_pipe(object):
    _path = None

    _file = None

    def _delete_if_exists(self):
        if os.path.exists(self._path):
            os.unlink(self._path)

    def __init__(self, path=None):
        self._path = path

    def __enter__(self):
        self._delete_if_exists()
        os.mkfifo(self._path)
        self._file = open(self._path, "w", 2)  # 2 byte buffer, 0 fails
        return self._file

    def __exit__(self, type, value, traceback):
        self._file.close()
        self._delete_if_exists()


def calculate_pi_digits():
    i = 0
    while True:
        yield i
        i += 1


while True:
    try:
        try:
            device_name = os.environ.get("DEVICE_NAME", "/dev/pi")
            with special_pipe(device_name) as pipe:
                for digit in calculate_pi_digits():
                    pipe.write(str(digit))
                    pipe.flush()
        except BrokenPipeError as exc:
            # print("restarting /dev/pi")
            pass
    except NameError as pypy_error:
        pass
