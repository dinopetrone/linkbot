from irctk import Bot
from linkbot.services import LinkService
# from linkbot.data import django
from linkbot.data import pinboard

bot  = Bot()
service = LinkService(pinboard.LinkData())

@bot.command('recent')
def get_tag(context):
	
	args = context.line['message'].split(' ')
	argsLen = len(args)
	count = 5
	if argsLen > 1:
		count = int(args[1])
		
	bot.reply("fetching recent links...", context.line)
	links = service.recent(count)
	for link in links:
		
		if link.description:
			bot.reply("{}: {}".format(link.description, link.url),context.line)
		else:
			bot.reply("{}".format(link.url), context.line)

@bot.command('tag')
def get_tag(context):
	args = context.line['message'].split(' ')
	tagStr = args[1]
	
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
	args = context.line['message'].split(' ')
	null = args.pop(0)
	url = args.pop(0)
	tags = args
	
	service.add_link(url, tags)
	message = 'url saved: ' + str(url);
	
	bot.reply(message,context.line)


def main():
	bot.config.from_pyfile('linkbot.cfg')
	bot.run()

if __name__ == '__main__':
	
	main()