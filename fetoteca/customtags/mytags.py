from django import template

register = template.Library()

@register.filter(name='infield')
def infield(entrada,set1,field):
	found=False
	for item in set1:
		if item[field]==entrada[field]:
			found=True

	return found

@register.filter(name='usefield')	
def filterfield(entrada,field):
	lista=[]
	for item in entrada:
		lista.append(item[field])
	return lista

@register.filter(name="joinfield")
def joinfield(list, args):
	ret = ""
	sep = ""
	args = args.split(':')

	for item in list:
		ret += sep + item[args[0]]
		sep = args[1]
	return ret

@register.filter(name='range')
def tag_range(input):
	return xrange(1, int(input) + 1)

@register.filter(name='iif')
def iif(input, args):
	args = args.split(':')
	if len(args) > 1:
		if str(input) == args[0]:
			return args[1]

	if len(args) == 3:
		return args[2]
	return ""

@register.filter(name='truncate')
def truncate(input, size):
	size = int(size) - 3
	if len(input) > size and size > 0:
		return input[0:size] + "..."
	else:
		return input

@register.filter(name='get')
def get(input, field):
	if field in input:
		return input[field]
	else:
		return ''