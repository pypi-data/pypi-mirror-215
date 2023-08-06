import logging
from time import time

from fbclient import get, set_config
from fbclient.common_types import FBUser
from fbclient.config import Config
from fbclient.utils import log

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%m-%d %H:%M')

env_secret = '9T0GABTXokagxhUZ81hUnws9_E2uOpIEyTjScBRr6JKA'

config = Config(env_secret, event_url='http://localhost:5100', streaming_url='ws://localhost:5100')

set_config(config)

client = get()

previous_flag_changed_keys = []

if client.initialize:
    # client.identify({'key': 'test-python-sdk-user', 'name': 'test-python-sdk-user'})
    def fn(flag_key, new_flag_value):
        return log.info("%s value is %s" % (flag_key, new_flag_value))
    while True:
        line = input('input user key and flag key seperated by / \n')
        if 'exit' == line.strip():
            break
        try:
            user_key, flag_key, *_ = tuple(line.split('/'))
            user = {'key': user_key, 'name': user_key, 'country': 'cn'}
            flag_changed_key = f'{user_key}_{flag_key}'
            if flag_changed_key not in previous_flag_changed_keys:
                client \
                    .flag_tracker \
                    .add_flag_value_changed_listener(flag_key, user, fn)
                previous_flag_changed_keys.append(flag_key)
            fb_user = FBUser.from_dict(user)
            log.info('FB Python SDK Test: user= %s' % fb_user.to_json_str())
            t1 = time()
            log.info('FB Python SDK Test: variation= %s' % client.variation_detail(flag_key, user).to_json_str())
            t2 = time()
            log.info('FB Python SDK Test: execution time= %f' % (t2 - t1))
        except:
            log.exception('FB Python SDK Test: unexpected error')
            break

client.stop()
