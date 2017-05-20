import json
import re
import random
from lxml import html
import requests
from urlparse import urljoin

import nn_utils


# return the following from the URL:
# - Title (requires fetching page)
# - Chosen url on the page (for next page)
# - Page where we started
# - Error

def get_nn_item(url, from_page, exclude=None):
    print "in get_nn_item for %s" % url
    try:
        page = requests.get(url)
        # print "got page"
        tree = html.fromstring(page.content)
        # print "got tree"
        # print tree

        # Get title
        title = get_title_from(tree)

        # Get url to use
        next_link = get_chosen_href_from(tree,url)
        print "chose next link: %s" % next_link


        # Check for errors
        if (next_link['error']):
            print "ERROR GETTING HREF FROM %s" % url
            print result.error
            return {
                'url':url,
                'title': None,
                'next_page': None,
                'from_page': from_page,
                'error':"error getting href from %s" % url
            }

        else: #got one
            print "returning nni:"
            print {
                'url':url,
                'title': title,
                'from_page': from_page,
                'next_page': next_link['chosen'],
                'error':None
            }
            return {
                'url':url,
                'title': title,
                'from_page': from_page,
                'next_page': next_link['chosen'],
                'error':None
            }

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print "printing error in get_random_url_from_page"
        print e
        # sys.exit(1)
        # return False
        return {
            'url': url,
            'title': None,
            'next_page': None,
            'from_page': None,
            'error': e
        }

def get_title_from(tree):
    return tree.xpath("//title/text()")[0]



def get_chosen_href_from(tree,url):
    xp = nn_utils.get_xpath()
    list_of_links = tree.xpath(xp)
    if len(list_of_links) > 0:
        rand = random.randint(0,len(list_of_links)-1)
        chosen = list_of_links[rand]

        chosen = urljoin(url,chosen)
        return {
            'chosen':chosen,
            'chosenFrom':url,
            'error':None
        }

    else:
        print("returning get_hrefs_from: error")
        return {
            'chosen':None,
            'chosenFrom':None,
            'error':'couldn\'t get a link'
        }


def get_random_url(current_url, list_of_links, exclude=None):

    #####
    # ADD (functionality): list of links to exclude, so we can exclude the most recently posted
    #####

    print "in get_random_url"
    # print "list of links: %s" % list_of_links

    if len(list_of_links) > 0:
        rand = random.randint(0,len(list_of_links)-1)
        chosen = list_of_links[rand]

        chosen = urljoin(current_url,chosen)

        # if "http" in chosen:
        #     print("returning get_random_url: ",chosen)
        #     return chosen
        # else:
        #     # see https://docs.python.org/2/library/urlparse.html
        #     print("returning get_random_url: ",protocol_and_domain + chosen)
        #     return chosen

        return chosen

    else:
        print("returning get_random_url: False")
        return False


def get_list_of_links(tree,url):
    # not([href*='live']):not([href*='stream']):not([href*='/go2']):not([href*='video'])
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")  #  a hrefs
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))] and not(contains(@href,'stream'))] and not(contains(@href,'live'))] and not(contains(@href,'/go2'))] and not(contains(@href,'video'))]/@href")  #  a hrefs

    #####
    # FIX THIS.  We should allow any links to the current domain, even if domain is explicitly defined in link (currently being excepted by '//')

    print "in get_list_of_links"

    # print "xpath"
    # print tree.xpath("//a[@href]/@href")  #  a hrefs

    xp = nn_utils.get_xpath()
    # print tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs

    # print "xp : %s" % xp

    return tree.xpath(xp)


#####
# can get rid of protocol_and_domain
# def get_random_url_from_page(protocol_and_domain,url,exclude=None):
def get_random_url_from_page(url, exclude=None):

    #####
    # ADD (functionality): list of links to exclude, so we can exclude the most recently posted
    #####

    # Load page
    # print("about to use requests package")
    print "in get_random_url_from_page"
    try:
        page = requests.get(url)
        print "got page"
        # page = urlfetch.fetch(url)
        tree = html.fromstring(page.content)
        print "got tree"
        # print tree

        # Get links on the page
        # Need to refine this with CSS selector

        # test = tree.xpath('//title/text()')
        # test = tree.xpath("//a[@href]/text()")
        # test = tree.xpath("//a[@href]/@href")
        # test = tree.xpath("//a[not(contains(@href,'//'))]/@href")
        # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
        ahrefs = get_list_of_links(tree,url)
        print "got ahrefs"
        # print ahrefs


        #####
        # break here
        # one function gets hrefs
        # other chooses one at random (with checks)


        # Choose one at random, and set it as new_url
        # url = get_random_url(protocol_and_domain,ahrefs)
        new_url = get_random_url(url,ahrefs)
        if (new_url):
            print "returning get_random_url_from_page: %s" %url
            # return url  # chosen link (url) from the original url
            return {
                'new_url':new_url,
                'url': url,
                'error':None
            }  # chosen link (url) from the original url
        else:
            print "returning false from get_random_url_from_page: %s" %url
            # return url  # chosen link (url) from the original url
            return {
                'new_url':None,
                'url': None,
                'error':"couldn't get url from links"
            }  # ch
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print "printing error in get_random_url_from_page"
        print e
        # sys.exit(1)
        # return False
        return {
            'url':None,
            'from_page':None,
            'error':e
        }


