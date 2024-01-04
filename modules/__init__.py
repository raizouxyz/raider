import importlib

_modules = [
    'autobumper',
    'avatar_change',
    'bannercolor_change',
    'bio_change',
    'bot_add',
    'button_push',
    'channel_spam',
    'dicoall_leveling',
    'displayname_change',
    'dissoku_review',
    'dm_spam',
    'dropdown_select',
    'friend_request',
    'guild_boost',
    'guild_join',
    'guild_leave',
    'guild_report',
    'hypesquad_change',
    'message_report',
    'nukebot',
    'pronouns_change',
    'reaction_add',
    'slashcommands_spam',
    'spotify_sync',
    'status_change',
    'token_generate',
    'userprofile_report',
    'vc_join',
    'webhook_spam',
]

modules = []
for module in _modules:
    importlib.import_module(f'modules.{module}')
    exec(f'modules.append({module})')