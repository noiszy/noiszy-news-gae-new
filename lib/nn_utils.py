import json
import re
import random
# from lxml import html
# import requests
# from urlparse import urljoin

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

    # print "in get_xpath for site %s" % site

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
    # print "fullXP %s" % fullXP
    return fullXP
    # return legacyXP

    # return "//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href"





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


def create_json(
        url=None,
        page_title=None,
        site=None,
        site_title=None,
        from_page=None,
        next_link=None,
        error=None
    ):

    if error:
        url = error
        page_title = error
        site = error
        site_title = error
        from_page = error

    item = {
        # 'url': new_url,
        'url': url,
        'page_title': page_title,
        'site': site,
        'site_title': site_title,
        'next_link': next_link,
        'from_page': from_page
    }
    json_item = json.dumps(item)
    # print "json_item:"
    # print json_item
    #
    # print "item:"
    # print item

    return json_item

