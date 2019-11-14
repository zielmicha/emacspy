import emacspy_threads, threading, time

emacspy_threads.call_soon_in_main_thread(lambda: print('a'))
emacspy_threads.init()
emacspy_threads.call_soon_in_main_thread(lambda: print('b'))

def test():
    time.sleep(1)
    emacspy_threads.call_soon_in_main_thread(lambda: print('c'))
    emacspy_threads.run_in_main_thread(lambda: print('d'))

threading.Thread(target=test).start()
