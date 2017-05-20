import json
import re
import random
from lxml import html
import requests
from urlparse import urljoin



def get_random_url(current_url, list_of_links, exclude=None):

    #####
    # ADD (functionality): list of links to exclude, so we can exclude the most recently posted
    #####

    print "in get_random_url"
    print "list of links: %s" % list_of_links

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


def get_random_url_no_domain(list_of_links,exclude=None):
    #####
    # ADD (functionality): list of links to exclude, so we can exclude the most recently posted
    #####

    if len(list_of_links) > 0:
        rand = random.randint(0,len(list_of_links)-1)
        print"returning get_random_url: %s" % list_of_links[rand]
        return protocol_and_domain + list_of_links[rand]
    else:
        print "returning get_random_url: False"
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

    xp = get_xpath()
    # print tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs

    print "xp : %s" % xp

    return tree.xpath(xp)

    # #
    # # instead of xpath, maybe we try CSS
    # # construct a CSS Selector
    # # sel = CSSSelector('a[href]')
    #
    # css_expression = query_selector(url)
    # print "css expression: %s" % css_expression
    #
    # # expression = GenericTranslator().css_to_xpath('a[href]')
    # expression = GenericTranslator().css_to_xpath(css_expression)
    # print "expression: %s" % expression
    #
    # # Apply the selector to the DOM tree.
    # # results = sel(tree)
    # css_results = tree.xpath(expression+"/@href")
    # print "css selector results"
    # print css_results
    #
    # return css_results


def query_selector(site,blockStreams=True):
    # construct query selector

    print "in query_selector for page %s" % site

    domain = re.match(r'(((https?\:\/\/)?([-a-z0-9]+(\.[-a-z0-9]{2,}){1,2}))($|\s|\/.*))',site,re.I)

    print "domain: %s" % domain

    # [2] is domain with the protocol,
    # [4] is domian without the protocol var
    # basicQS, no_domain_QS, onsite_with_protocol_QS, onsite_with_domain_QS, blockStream_QS;
    blockStream_QS = ""
    if blockStreams == True:
        # / go2 = cnn live TV link
        blockStream_QS = ":not([href*='live']):not([href*='stream']):not([href*='/go2']):not([href*='video'])"

    # don't open new windows, email programs, or javascript links
    basicQS = ":not([target]):not([href^='mailto']):not([href^='javascript'])"

    # if there's no domain in the list, it's onsite
    no_domain_QS = "a[href]" + basicQS + ":not([href^='http'])" + blockStream_QS

    # if it points to its own domain with protocol, it's onsite
    # onsite_with_protocol_QS = "a[href^='" + domain[2] + "']" + basicQS + blockStream_QS
    onsite_with_protocol_QS = "a[href^='" + domain.group(2) + "']" + basicQS + blockStream_QS

    # if it points to its own domain by domain name only, it's onsite
    # onsite_with_domain_QS = "a[href^='" + domain[4] + "']" + basicQS + blockStream_QS
    onsite_with_domain_QS = "a[href^='" + domain.group(4) + "']" + basicQS + blockStream_QS

    # what about subdomains...?
    # base that on the stored current site

    # put it all together
    full_QS = no_domain_QS + ", " + onsite_with_protocol_QS + ", " + onsite_with_domain_QS

    print "full_QS %s" % full_QS
    return full_QS


def get_xpath(site=None,blockStreams=True):
    # construct query selector

    print "in get_xpath for page %s" % site

    # domain = re.match(r'(((https?\:\/\/)?([-a-z0-9]+(\.[-a-z0-9]{2,}){1,2}))($|\s|\/.*))',site,re.I)

    # print "domain: %s" % domain

    xp = "//"

    # print tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs
    legacyXP = "//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href"

    # [2] is domain with the protocol,
    # [4] is domian without the protocol var
    # basicQS, no_domain_QS, onsite_with_protocol_QS, onsite_with_domain_QS, blockStream_QS;
    blockStream_QS = ""
    if blockStreams == True:
        # / go2 = cnn live TV link
        # blockStream_QS = ":not([href*='live']):not([href*='stream']):not([href*='/go2']):not([href*='video'])"
        blockStreamXP = " and not(contains(@href,'live')) and not(contains(@href,'stream')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))"

    # don't open new windows, email programs, or javascript links
    # basicQS = ":not([target]):not([href^='mailto']):not([href^='javascript'])"
    # basicXP = "//a[@href] and not([@target]) and not(contains(@href,'mailto')) and not(contains(@href,'javascript'))"
    startXP = "//a["
    endXP = "]/@href"
    basicXP = "contains(@href,'/') and not(@target) and not(contains(@href,'mailto')) and not(contains(@href,'javascript'))"

    # if there's no domain in the list, it's onsite
    # no_domain_QS = "a[href]" + basicQS + ":not([href^='http'])" + blockStream_QS
    # no_domain_QS = "a[href]" + basicQS + ":not([href^='http'])" + blockStream_QS
    #
    # # if it points to its own domain with protocol, it's onsite
    # # onsite_with_protocol_QS = "a[href^='" + domain[2] + "']" + basicQS + blockStream_QS
    # onsite_with_protocol_QS = "a[href^='" + domain.group(2) + "']" + basicQS + blockStream_QS
    #
    # # if it points to its own domain by domain name only, it's onsite
    # # onsite_with_domain_QS = "a[href^='" + domain[4] + "']" + basicQS + blockStream_QS
    # onsite_with_domain_QS = "a[href^='" + domain.group(4) + "']" + basicQS + blockStream_QS
    #
    # # what about subdomains...?
    # # base that on the stored current site
    #
    # # put it all together
    # full_QS = no_domain_QS + ", " + onsite_with_protocol_QS + ", " + onsite_with_domain_QS

    fullXP = startXP + basicXP + blockStreamXP + endXP
    # fullXP = startXP + basicXP + endXP
    print "fullXP %s" % fullXP
    return fullXP
    # return legacyXP

    # return "//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href"

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
        print tree

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

        # Choose one at random, and set it as new_url
        # url = get_random_url(protocol_and_domain,ahrefs)
        url = get_random_url(url,ahrefs)
        print("returning get_random_url_from_page: ",url)
        return url  # chosen link (url) from the original url
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
        # sys.exit(1)
        return False



def get_random_url_from_page_no_domain(url,exclude=None):
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

        # Get links on the page
        # Need to refine this with CSS selector

        # test = tree.xpath('//title/text()')
        # test = tree.xpath("//a[@href]/text()")
        # test = tree.xpath("//a[@href]/@href")
        # test = tree.xpath("//a[not(contains(@href,'//'))]/@href")
        # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
        ahrefs = get_list_of_links(tree,url)
        print "got ahrefs"
        print ahrefs

        # Choose one at random, and set it as new_url
        # url = get_random_url(protocol_and_domain,ahrefs)
        url = get_random_url_no_domain(ahrefs)
        print("returning get_random_url_from_page: ",url)
        return url  # chosen link (url) from the original url
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
        # sys.exit(1)
        return False




def get_random_homepage(exclude=None):

    #####
    # TO ADD (functionality): exclude (so we can exclude current)
    #####

    # Get list of sites

    # OMG THIS IS THE PROBLEM

    # with open('static/site_list.json') as json_data:
    with open('static/site_list_backup.json') as json_data:
        print "opened"
        presets = json.load(json_data)
        # print "presets: %s" % presets

        site_list = presets['sites']['default'] # only the defaults from the json

        # print("site_list: ",site_list)

        rand_site_num = random.randint(0,len(site_list)-1)

        # return url
        # print("returning random homepage: ",site_list[rand_site_num]['url'])
        print "returning random homepage: %s" % site_list[rand_site_num]['url']
        return site_list[rand_site_num]['url']



# def click_link_or_start_over(from_url):
#
#     # roll the dice
#     dice = 1
#
#     if dice == 0:
#         # start again
#         # get a new homepage
#         new_url = noiszy_news.get_random_homepage()
#
#     else:
#         # use this page
#         # Get new_url from this page's list of links
#         # new_url = get_random_url_from_page_no_domain("http://www.google.com",from_url)
#
#         new_url = noiszy_news.get_random_url_from_page_no_domain(from_url)
#
#         # if there's an error in the above, then do this:
#         # new_url = get_random_homepage()
#
#     return new_url


def create_json(url=None, page_title=None, site=None, site_title=None, next_link=None,error=None):
    if error:
        url = error
        page_title = error
        site = error
        site_title = error

    item = {
        # 'url': new_url,
        'url': url,
        'page_title': page_title,
        'site': site,
        'site_title': site_title,
        'next_link': next_link
    }
    json_item = json.dumps(item)
    # print "json_item:"
    # print json_item
    #
    # print "item:"
    # print item

    return json_item

