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
    q, r, t, j = 1, 180, 60, 2
    while True:
        u = 3 * (3 * j + 1) * (3 * j + 2)
        y = (q * (27 * j - 12) + 5 * r) // (5 * t)
        yield y
        new_q = 10 * q * j * (2 * j - 1)
        r = 10 * u * (q * (5 * j - 2) + r - y * t)
        t = t * u
        j = j + 1
        q = new_q


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
