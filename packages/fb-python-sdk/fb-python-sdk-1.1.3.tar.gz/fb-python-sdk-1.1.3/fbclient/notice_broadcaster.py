
from queue import Empty, Queue
from threading import Thread
from fbclient.interfaces import Notice, Notifier

from fbclient.utils import log


class NoticeBroadcater:
    def __init__(self):
        self.__event_queue = Queue()
        self.__closed = False
        self.__notifiers = {}
        self.__thread = Thread(daemon=True, target=self.__run)
        self.__thread.start()

    def add_notifier(self, notice_type: str, notifier: Notifier):
        log.debug('add notifier %s for notice type %s' % (notifier.name, notice_type))
        if notice_type not in self.__notifiers:
            self.__notifiers[notice_type] = []
        self.__notifiers[notice_type].append(notifier)

    def remove_listener(self, notice_type: str, notifier: Notifier):
        if notice_type in self.__notifiers:
            notifiers = self.__notifiers[notice_type]
            if not notifiers:
                del self.__notifiers[notice_type]
            else:
                notifiers.remove(notifier)

    def broadcast(self, notice: Notice):
        self.__event_queue.put(notice)

    def stop(self):
        self.__closed = True
        self.__thread.join()

    def __run(self):
        while not self.__closed:
            try:
                notice = self.__event_queue.get(block=True, timeout=1)
                self.__event_process(notice)
            except Empty:
                pass

    def __event_process(self, notice: Notice):
        if notice.notice_type in self.__notifiers:
            for notifier in self.__notifiers[notice.notice_type]:
                notifier.handle(notice)
