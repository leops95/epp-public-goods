from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.1, participation_fee=0)
SESSION_CONFIGS = [dict(name='public_goods_4_players', num_demo_participants=None, app_sequence=['public_goods_4']), dict(name='public_goods_all_players', num_demo_participants=None, app_sequence=['public_goods_all'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'CHF'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


