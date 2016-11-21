from cred import *
import os, logging


defaults = {
    "WHATSAPP_LOGIN": phone,
    "WHATSAPP_PW": pw,
    "WHATSAPP_ADMIN": "",
    "BING_API_KEY": ""
}

auth = (os.environ.get('WHATSAPP_LOGIN', defaults['WHATSAPP_LOGIN']),
        os.environ.get('WHATSAPP_PW', defaults['WHATSAPP_PW']))

# If filter_groups is True, the bot only stays
# at groups that there is at least one admin on it.
# Otherwise will leave instantly if added.
filter_groups = True
admins = [os.environ.get('WHATSAPP_ADMIN', defaults['WHATSAPP_ADMIN']), ]

#Overall Admin for Autobot,will be used for security and admin features
botAdmin = '918122753538'

# Bing API for image search
bing_api_key = os.environ.get('BING_API_KEY', defaults['WHATSAPP_ADMIN'])

# Path to download the media requests
# (audio recordings, printscreens, media and youtube videos)
if not os.path.exists('bot-tmp'):
    os.makedirs('bot-tmp')
media_storage_path = "bot-tmp"

# Session shelve db path
session_db_path = r"C:\Users\radhakrishnanr\Desktop\tmp\sessions.db"

# Logging configuration.
# By default only logs the command messages.
# If logging_level set to logging.DEBUG, yowsup will log every protocoll message exchange with server.
log_format = '_%(filename)s_\t[%(levelname)s][%(asctime)-15s] %(message)s'
logging_level = logging.INFO


