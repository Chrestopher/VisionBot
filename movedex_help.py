from bs4 import NavigableString

def find_type(url):
    #returns type from url
    f=url.split('/attackdex-swsh/')
    i=f[1].split('.')
    return i[0]
def find_category(url):
    #returns category from url
    f = url.split('/attackdex-swsh/')
    i = f[1].split('.')
    return i[0]
def find_thumbnail(src):
    image='serebii.net'+src
    return image
