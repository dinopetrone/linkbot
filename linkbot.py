import string
from irctk import Bot
from linkbot.services import LinkService
# from linkbot.data import django
from linkbot.data import pinboard

bot  = Bot()
service = LinkService(pinboard.LinkData())

@bot.command('help')
def get_help(context):
	message = """My available commands [MUST be prefixed with a . (dot)]:
- tags: show a list of all unique tags
- tag [tag]: show links with a specific tag
- recent [count]: displays the N most recent links. If <int> is omitted, 5 will be used.
- link [url]|[desc]|[tags]: add a new link. must be | delimited. tags are <space> delimited
"""
	for line in message.split('\n'):
		bot.reply(line, context.line)

@bot.command('recent')
def get_tag(context):
	count = 5 
	message = prepare_message(context)
	
	try:
		count = int(message)
	except (ValueError,TypeError):
		pass
		
	bot.reply("fetching recent links...", context.line)
	links = service.recent(count)
	
	for link in links:
		
		if link.description:
			bot.reply("{}: {}".format(link.description, link.url),context.line)
		else:
			bot.reply("{}".format(link.url), context.line)

@bot.command('tag')
def get_tag(context):
	args = prepare_message(context).split(' ')
	tagStr = args[0]
	
	bot.reply("finding links with tags: {}".format(tagStr), context.line)
	links = service.get_links_with_tag(tagStr)

	for link in links:
		if link.description:
			bot.reply("{}: {}".format(link.description, link.url),context.line)
		else:
			bot.reply("{}".format(link.url), context.line)

@bot.command('tags')
def get_tags(context):
	bot.reply("fetching all tags...", context.line)
	tags = sorted(service.get_tags(), key=lambda tag: tag.count, reverse=True)
	bot.reply("{} tags available".format(len(tags)), context.line)
	
	n = 1
	for tag in tags:
		bot.reply("{}) {} ({})".format(str(n).zfill(2), tag.name, tag.count), context.line)
		n += 1
			
	
@bot.command('link')
def add_link(context):
	# input format:
	# link|description|tags
	# first item in the split will be .link so [len(.link):]
	message = prepare_message(context)
	args = message.split('|')
	args = map(string.strip, args)
	url, description, tags = args
	
	tags = " ".join(filter(string.strip, tags.split(" ")))
	
	service.add_link(url, description, tags)
	
	message_reply = 'url saved: ' + str(url);
	bot.reply(message_reply, context.line)


def prepare_message(context):
	message = context.line['message']
	try:
		first_space = message.index(" ")
	except ValueError:
		# no spaces were found which means, a command like .recent
		# with has no futher arguments was used
		# so just return None
		return None

	message = message[first_space:]
	return message.strip()


def main():
	bot.config.from_pyfile('linkbot.cfg')
	bot.run()



if __name__ == '__main__':
	
	main()