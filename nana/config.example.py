# Buat file config.py baru dalam dir dan impor yang sama, kemudian perpanjang kelas ini.
class Config(object):
	LOGGER = True
	
	# Must be filled!
	# Register here: https://my.telegram.org/apps
	api_id = 803843
	api_hash = "4705e5aba89a0e08b51c6dfb7125b290"
	DB_URL = "postgres://username:password@localhost:5432/database" # Your database URL

	# Version
	lang_code = "en" # Your language code
	device_model = "PC" # Device model
	system_version = "Linux" # OS system type

	# Use real bot for Assistant
	# Pass False if you dont want
	ASSISTANT_BOT = True
	ASSISTANT_BOT_TOKEN = "722320221:AAHW2iUIzHMwMYeGV_MYjmHbk8zZXpgrTv0"

	# Required for some features
	# Owner and AdminSettings is for your Assistant bot only
	Owner = 681335505 # Insert your Telegram ID (go @EmiliaHikariBot, type /id)
	AdminSettings = [681335505] # Do like above, can insert multiple other user id, example [12345, 23456]
	Command = ["!", "."] # Insert command prefix, if you insert "!" then you can do !ping
	# WORKER must be int (number)
	NANA_WORKER = 8
	ASSISTANT_WORKER = 2

	# APIs token
	thumbnail_API = "" # Register free here: https://thumbnail.ws/
	screenshotlayer_API = "" # Register free here: https://screenshotlayer.com/

	# Load or no load plugins
	# userbot
	USERBOT_LOAD = []
	USERBOT_NOLOAD = []
	# manager bot
	ASSISTANT_LOAD = []
	ASSISTANT_NOLOAD = []
	

class Production(Config):
	LOGGER = False


class Development(Config):
	LOGGER = True
