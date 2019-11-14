import emacspy, socket, tempfile, queue, threading
from emacspy import sym
from typing import Optional

_call_soon_queue: queue.Queue = queue.Queue(0)
_wakeup_conn: Optional[socket.socket] = None

def call_soon_in_main_thread(f):
    _call_soon_queue.put(f)
    if _wakeup_conn:
        _wakeup_conn.send(b'x')

def run_in_main_thread(f):
    ev = threading.Event()

    def wrapper():
        f()
        ev.set()

    call_soon_in_main_thread(wrapper)
    ev.wait()

@emacspy.defun('emacspy-threads/wakeup')
def wakeup(p, data):
    while True:
        try:
            f = _call_soon_queue.get_nowait()
        except queue.Empty:
            break

        f()

def init():
    with tempfile.TemporaryDirectory() as dir:
        path = dir + '/socket'

        s = socket.socket(socket.AF_UNIX)
        s.bind(path)
        s.listen(1)

        # this is "self-pipe trick"
        emacspy.f.make_network_process(
            sym(":name"), "emacspy-wakeup",
            sym(":remote"), path,
            sym(":filter"), sym('emacspy-threads/wakeup'))

        global _wakeup_conn
        _wakeup_conn, _ = s.accept()

    wakeup(None, None)
