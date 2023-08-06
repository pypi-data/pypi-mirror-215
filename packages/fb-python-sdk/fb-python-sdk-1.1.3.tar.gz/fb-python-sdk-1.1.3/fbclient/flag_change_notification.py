
from abc import ABC, abstractmethod
from typing import Any, Callable
from fbclient.common_types import FBUser
from fbclient.interfaces import Notice, Notifier
from fbclient.notice_broadcaster import NoticeBroadcater

from fbclient.utils import log

FLAG_CHANGE_NOTICE_TYPE = 'flag_change_notice'


class FlagChangeNotice(Notice):
    def __init__(self, flag_key: str):
        self.__flag_key = flag_key

    @property
    def notice_type(self) -> str:
        return FLAG_CHANGE_NOTICE_TYPE

    @property
    def flag_key(self) -> str:
        return self.__flag_key


class FlagChangeNotifier(Notifier, ABC):

    def handle(self, notice: FlagChangeNotice):
        self.on_flag_change(notice)

    @abstractmethod
    def on_flag_change(self, notice: FlagChangeNotice):
        pass


class FlagValueChangedNotifier(FlagChangeNotifier):
    def __init__(self,
                 flag_key: str,
                 user: dict,
                 evaluate_fn: Callable[[str, dict, Any], Any],
                 flag_value_changed_fn: Callable[[str, Any], None]):
        self.__flag_key = flag_key
        self.__user = user
        self.__evaluate_fn = evaluate_fn
        self.__fn = flag_value_changed_fn

    def on_flag_change(self, notice: FlagChangeNotice):
        if notice.flag_key == self.__flag_key:
            new_flag_value = self.__evaluate_fn(self.__flag_key, self.__user, None)
            try:
                self.__fn(self.__flag_key, new_flag_value)
            except Exception as e:
                log.exception('FB Python SDK: unexpected error in handle flag change %s: %s' % (self.name, str(e)))

    @property
    def name(self) -> str:
        return 'FlagChange for: %s/%s' % (self.__user['name'], self.__flag_key)


class FlagTracker:
    def __init__(self,
                 flag_change_broadcaster: NoticeBroadcater,
                 evaluate_fn: Callable[[str, dict, Any], Any],):
        self.__broadcater = flag_change_broadcaster
        self.__evaluate_fn = evaluate_fn

    def add_flag_value_changed_notifier(self,
                                        flag_key: str,
                                        user: dict,
                                        flag_value_changed_fn: Callable[[str, Any], None]) -> FlagValueChangedNotifier:
        # check flag key
        if not isinstance(flag_key, str) or not flag_key:
            raise ValueError('flag_key must be a non-empty string')
        # check user
        FBUser.from_dict(user)
        # check flag_value_changed_fn
        if not isinstance(flag_value_changed_fn, Callable) or not flag_value_changed_fn:
            raise ValueError('flag_value_changed_fn must be a callable function')

        notifier = FlagValueChangedNotifier(flag_key, user, self.__evaluate_fn, flag_value_changed_fn)
        self.__broadcater.add_notifier(FLAG_CHANGE_NOTICE_TYPE, notifier)
        return notifier

    def add_flag_change_notifier(self, notifier: FlagChangeNotifier):
        self.__broadcater.add_notifier(FLAG_CHANGE_NOTICE_TYPE, notifier)

    def remove_flag_change_notifier(self, notifier: Notifier):
        self.__broadcater.remove_listener(FLAG_CHANGE_NOTICE_TYPE, notifier)
