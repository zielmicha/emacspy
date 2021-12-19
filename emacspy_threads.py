import emacspy, socket, tempfile, queue, threading
from emacspy import sym
from typing import Optional
import concurrent.futures, traceback

_call_soon_queue: queue.Queue = queue.Queue(0)
_wakeup_conn: Optional[socket.socket] = None

_emacs_thread = threading.current_thread()

def call_soon_in_main_thread(f):
    _call_soon_queue.put(f)
    if _wakeup_conn:
        _wakeup_conn.send(b'x')

def run_in_main_thread_future(f):
    fut: concurrent.futures.Future = concurrent.futures.Future()

    def wrapper():
        try:
            fut.set_result(f())
        except Exception as exc:
            traceback.print_exc()
            fut.set_exception(exc)

    call_soon_in_main_thread(wrapper)
    return fut

def run_in_main_thread(f):
    if _emacs_thread == threading.current_thread():
        raise Exception('already on emacs main thread')
    return run_in_main_thread_future(f).result()

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
