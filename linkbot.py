from irctk import Bot
from linkbot.services import LinkService
from linkbot.data import django
from linkbot.data import pinboard

@bot.command('last')
def get_tag(context):
	args = context.line['message'].split(' ')
	argsLen = len(args)
	count = 5
	if argsLen > 1:
		count = int(args[1])
		
	links = service.recent(count)
	for link in links:
		bot.reply(link.url,context.line)

	# links = Link.objects.all()[:count]
	# for link in links:
	# 	bot.reply(link.url,context.line)

@bot.command('tag')
def get_tag(context):
	args = context.line['message'].split(' ')
	tagStr = args[1]
	
	links = service.get_links_with_tag(tagStr)

	for link in links:
		bot.reply(link.url,context.line)

	# tags = Tag.objects.filter(value=tagStr)
	# for tag in tags:
	# 	bot.reply(tag.link.url,context.line)
	
	
@bot.command('link')
def add_link(context):
	args = context.line['message'].split(' ')
	null = args.pop(0)
	url = args.pop(0)
	tags = args
	
	# l = Link(url=url,pub_date=timezone.now())
	# l.save()
	# linkId = l.id
	# for tag in tags:
	# 	t = Tag(value=tag,link=l)
	# 	t.save()
	
	service.add_link(url, tags)
	message = 'url saved: ' + str(url);
	
	bot.reply(message,context.line)


def main():
	bot.config.from_pyfile('linkbot.cfg')
	bot.run()

if __name__ == '__main__':
	bot     = Bot()
	service = LinkService(pinboard.LinkData())
	main()