import os
import shutil
import sys

from nana import app, Command, OFFICIAL_BRANCH, REPOSITORY
from __main__ import restart_all, except_hook
from pyrogram import Filters
from nana.assistant.updater import update_changelog

from git import Repo, exc


__MODULE__ = "Updater"
__HELP__ = """
You want to update latest version?
Easy, just type like bellow

──「 **Check update** 」──
-> `update`
Only check update if avaiable

──「 **Update bot** 」──
-> `update now`
Update your bot to latest version
"""

async def gen_chlog(repo, diff):
	changelog = ""
	d_form = "%H:%M - %d/%m/%y"
	for cl in repo.iter_commits(diff):
		changelog += f'• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n'
	return changelog

async def initial_git(repo):
	isexist = os.path.exists('nana-old')
	if isexist:
		shutil.rmtree('nana-old')
	os.mkdir('nana-old')
	os.rename('nana', 'nana-old/nana')
	os.rename('.gitignore', 'nana-old/.gitignore')
	os.rename('LICENSE', 'nana-old/LICENSE')
	os.rename('README.md', 'nana-old/README.md')
	os.rename('requirements.txt', 'nana-old/requirements.txt')
	update = repo.create_remote('master', REPOSITORY)
	update.pull('master')
	os.rename('nana-old/nana/config.py', 'nana/config.py')
	shutil.rmtree('nana/session/')
	os.rename('nana-old/nana/session/', 'nana/session/')

@app.on_message(Filters.user("self") & Filters.command(["update"], Command))
async def Updater(client, message):
	await message.edit("__Checking update...__")
	initial = False
	try:
		repo = Repo()
	except exc.NoSuchPathError as error:
		await message.edit(f"**Update failed!**\n\nError:\n`directory {error} is not found`")
		return
	except exc.InvalidGitRepositoryError as error:
		repo = Repo.init()
		initial = True
	except exc.GitCommandError as error:
		await message.edit(f'**Update failed!**\n\nError:\n`{error}`')
		return

	if initial:
		if len(message.text.split()) != 2:
			await message.edit('Your git workdir is missing!\nBut i can repair and take new latest update for you.\nJust do `update now` to repair and take update!')
			return
		elif len(message.text.split()) == 2 and message.text.split()[1] == "now":
			try:
				await initial_git(repo)
			except Exception as err:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				await message.edit('An error has accured!\nPlease see your Assistant for more information!')
				await except_hook(exc_type, exc_obj, exc_tb)
				return
			await message.edit('Successfully Updated!\nBot is restarting...')
			await update_changelog("-> **WARNING**: Bot has been created a new git and sync to latest version, your old files is in nana-old")
			await restart_all()
			return


	brname = repo.active_branch.name
	if brname not in OFFICIAL_BRANCH:
		await message.edit(f'**[UPDATER]:** Looks like you are using your own custom branch ({brname}). \
				in that case, Updater is unable to identify which branch is to be merged. \
				please checkout to any official branch')
		return

	try:
		repo.create_remote('upstream', REPOSITORY)
	except BaseException:
		pass

	upstream = repo.remote('upstream')
	upstream.fetch(brname)
	try:
		changelog = await gen_chlog(repo, f'HEAD..upstream/{brname}')
	except Exception as err:
		if "fatal: bad revision" in str(err):
			try:
				await initial_git(repo)
			except Exception as err:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				await message.edit('An error has accured!\nPlease see your Assistant for more information!')
				await except_hook(exc_type, exc_obj, exc_tb)
				return
			await message.edit('Successfully Updated!\nBot is restarting...')
			await update_changelog("-> **WARNING**: Bot has been created a new git and sync to latest version, your old files is in nana-old")
			await restart_all()
			return
		exc_type, exc_obj, exc_tb = sys.exc_info()
		await message.edit('An error has accured!\nPlease see your Assistant for more information!')
		await except_hook(exc_type, exc_obj, exc_tb)
		return

	if not changelog:
		await message.edit(f'Nana is up-to-date with branch **{brname}**\n')
		return

	if len(message.text.split()) != 2:
		changelog_str = f'To update latest changelog, do\n-> `update now`\n\n**New UPDATE available for [{brname}]:\n\nCHANGELOG:**\n`{changelog}`'
		if len(changelog_str) > 4096:
			await message.edit("`Changelog is too big, view the file to see it.`")
			file = open("nana/cache/output.txt", "w+")
			file.write(changelog_str)
			file.close()
			await client.send_document(message.chat.id, "nana/cache/output.txt", reply_to_message_id=message.message_id, caption="`Changelog file`")
			os.remove("nana/cache/output.txt")
		else:
			await message.edit(changelog_str)
		return
	elif len(message.text.split()) == 2 and message.text.split()[1] == "now":
		await message.edit('`New update found, updating...`')
		try:
			upstream.pull(brname)
			await message.edit('Successfully Updated!\nBot is restarting...')
		except exc.GitCommandError:
			repo.git.reset('--hard')
			await message.edit('Successfully Updated!\nBot is restarting...')
		await update_changelog(changelog)
		await restart_all()
	else:
		await message.edit("Usage:\n-> `update` to check update\n-> `update now` to update latest commits\nFor more information check at your Assistant")
