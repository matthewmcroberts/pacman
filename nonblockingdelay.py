
from threading import Thread
from time import sleep

def call_later(delay,func):
    def delay_timer():
        sleep(delay)
        func()
    thread = Thread(target=delay_timer)
    thread.start()
    
def call_later_with_param(delay,func,param):
    def delay_timer():
        sleep(delay)
        func(param)
    thread = Thread(target=delay_timer)
    thread.start()

