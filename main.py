from flask import Flask, Response, request, stream_with_context

from flask import render_template

import argparse
import sys
import re
import random


# from google.appengine.api import urlfetch

from lxml import html
# from lxml.cssselect import CSSSelector

import requests
# import requests_toolbelt.adapters.appengine
#
# # Use the App Engine Requests adapter. This makes sure that Requests uses
# # URLFetch.
# requests_toolbelt.adapters.appengine.monkeypatch()


import json
import time

app = Flask(__name__)



#########
# TO DO:
# errors on requests - try different URLs (protocol, etc)
# update page via ajax each time a result is loaded
# if new url is the same as the last url, skip it
#########



# @app.route('/loop')
# def loop():
#     def generate():
#         # yield "Hello"
#         # yield "World"
#         yield "hiiiiii"
#     # return Response(generate())
#     return render_template("loop_test.html",name="hello world")



def generate_loop(times):
    # yield render_template("loop_test.html")
    for i in xrange(times):
        time.sleep(1)
        yield "<br>{i}: hi fancypants  ".format(i=i)
        # yield "something"
        with app.app_context():
            yield render_template('loop_test.html',message="a message")


@app.route('/longloop/<int:times>')
def longloop(times):
    # def generate(rows):
    #     for i in xrange(rows):
    #         time.sleep(1)
    #         yield "{i}: hi there  ".format(i=i)
    #
    #         # yield render_template("loop_test.html",name="heya")
    #
    #         # yield render_template("loop_test.html")
    # return Response(generate(rows))
    return Response(generate_loop(times))


# @app.route('/noiszy-news')
# def loop():
#     def generate():
#         yield "Hello"
#         yield "World"
#     return Response(generate())
#
# @app.route('/newsitems/<int:rows>')
# def newsitems(rows):
#     def generate(rows):
#         for i in xrange(rows):
#             time.sleep(1)
#             yield "{i}: Hello World".format(i=i)
#     return Response(generate(rows))


@app.route('/test')
def hello_world():

    return 'Hello again!'


def test_function():
    print("test function")

def get_random_url(protocol_and_domain,list_of_links,exclude=None):
    #####
    # ADD (functionality): list of links to exclude, so we can exclude the most recently posted
    #####

    if len(list_of_links) > 0:
        rand = random.randint(0,len(list_of_links)-1)
        print("returning get_random_url: ",protocol_and_domain + list_of_links[rand])
        return protocol_and_domain + list_of_links[rand]
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


def get_list_of_links(tree):
    # not([href*='live']):not([href*='stream']):not([href*='/go2']):not([href*='video'])
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")  #  a hrefs
    # return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))] and not(contains(@href,'stream'))] and not(contains(@href,'live'))] and not(contains(@href,'/go2'))] and not(contains(@href,'video'))]/@href")  #  a hrefs

    #####
    # FIX THIS.  We should allow any links to the current domain, even if domain is explicitly defined in link (currently being excepted by '//')
    return tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//')) and not(contains(@href,'stream')) and not(contains(@href,'live')) and not(contains(@href,'/go2')) and not(contains(@href,'video'))]/@href")  #  a hrefs


def get_random_url_from_page(protocol_and_domain,url,exclude=None):
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
        ahrefs = get_list_of_links(tree)
        print "got ahrefs"
        print ahrefs

        # Choose one at random, and set it as new_url
        url = get_random_url(protocol_and_domain,ahrefs)
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
        ahrefs = get_list_of_links(tree)
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



def stream():
    print "in stream()"

    # with app.app_context():
    def f():
        print "with app.app_context"
        yield render_template('news2_header.html')
        print "yielded"

        print "generate_ajax()"
        yield generate_ajax()

        yield render_template('news2_footer.html')

    return Response(stream_with_context(f()))



@app.route('/stream')
@app.route('/stream/<number_of_results>')

def streamed_response(number_of_results=12):
    print "in streamed_response"
    def generate():
        # yield 'Hello '
        # # yield request.args['name']
        # yield '!'
        print "in generate()"

        yield render_template('news2_header.html')
        print "yielded"

        print "generate_ajax()"
        # yield generate_ajax()







        # @app.stream_with_context
        # def generate():
        #     yield 'Hello '
        #     yield flask.request.args['name']
        #     yield '!'
        # return flask.Response(generate())

        print "starting ajax_news"

        # Setup...
        # num_results = 12  # number of results to display
        num_results = int(number_of_results)  # number of results to display
        all_results = []  # objects to hold results
        item = []  # objects to hold results
        count = 0  # counter

        print "number of results: %s" % number_of_results

        while count < num_results:

            print "-------"
            print "starting outer loop"
            print "count: %s" % count
            print "num_results: %s" % num_results
            print

            # Pick one (homepage) at random, store as current_site and current_page
            print "calling get_random_homepage()"

            current_site = get_random_homepage()
            current_page = current_site

            # Get a random URL from that page to work with, assign to new_url
            new_url = get_random_url_from_page(current_site, current_page)
            # print("new_url: ",new_url)

            # if
            if new_url:
                print "was able to get a url from the page"

                # Internal loop from here...
                site_page_count = 1
                # while site_page_count < 4 and count < num_results:
                while site_page_count != 0 and count < num_results:

                    print "----"
                    print "starting internal loop"

                    # Make sure new_url is defined before proceeding
                    if (new_url):
                        print "internal loop - was able to get a url from the page"

                        # Get the new_url, store as current_page
                        current_page = new_url

                        # print("current page: ",current_page)

                        try:
                            # Request current_page
                            page = requests.get(current_page)
                            tree = html.fromstring(page.content)

                            # get the list of a hrefs
                            # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                            ahrefs = get_list_of_links(tree)
                            # print("ahrefs: ",ahrefs)
                        except requests.exceptions.RequestException as e:  # This is the correct syntax
                            print e
                            # sys.exit(1)
                            ahrefs = []

                        # if the page includes >1 links (seems "real", and we can proceed from here)
                        if len(ahrefs) > 1:
                            print "list of ahrefs is > 1"

                            # Scrape its title, img etc
                            title = tree.xpath("//title/text()")
                            # print("new url: ",new_url)

                            # need to define this with a regex match
                            site_title = ""

                            #  Create item & append to all_results
                            item = {
                                # 'url': new_url,
                                'url': current_page,
                                'page_title': title[0],
                                'site': current_site,
                                'site_title': site_title
                            }
                            all_results.append(item)

                            print
                            print
                            print "WITH APP.APP_CONTEXT"
                            print
                            print

                            with app.app_context():
                                print
                                print
                                print "YIELD NOW"
                                print
                                print

                                yield render_template('news_item.html', item=item)

                                print
                                print
                                print "YIELDED"
                                print
                                print

                            print "added to all_results: %s" % item

                            # now on to the next
                            # get the next URL to work on and store it as new_url
                            new_url = get_random_url(current_site, ahrefs)
                            # print(get_random_url(current_site,test))
                            print "prepping next URL: %s" % new_url

                            # increment the number of results on the page
                            count = count + 1

                            # # since it all worked, roll the dice here
                            # # generate randomly between 0-x
                            # # internal loop will stop if it's 0
                            # # (so, can change the likelihood by changing 2nd argument)
                            # # lower argument = more likely to start a new site
                            # site_page_count = random.randint(0,2)
                            # print("dice rolled: ",site_page_count)


                        else:
                            print "list of ahrefs is: ", ahrefs
                            # ...get a new URL and loop back around with that one
                            new_url = get_random_url_from_page(current_site, current_site)
                            print "last URL didn't have ahrefs, so prepping next URL: %s" % new_url


                    # If new_url is not defined...
                    else:
                        # this url is bogus somehow
                        # so reset to the current site and go from there

                        print "new_url is false"
                        print "current_site: %s" % current_site
                        print "current_page: %s" % current_page
                        print

                        # ...get a new URL and loop back around with that one
                        new_url = get_random_url_from_page(current_site, current_site)

                    # generate randomly between 0-x
                    # internal loop will stop if it's 0
                    # (so, can change the likelihood by changing 2nd argument)
                    # lower argument = more likely to start a new site
                    site_page_count = random.randint(0, 2)
                    print "dice rolled: %s" % site_page_count

            else:
                print "was not able to get a url from homepage: %s" % current_site






        yield render_template('news2_footer.html')
        print "yielded"
    return Response(stream_with_context(generate()))




def click_link_or_start_over(from_url):

    # roll the dice
    dice = 1

    if dice == 0:
        # start again
        # get a new homepage
        new_url = get_random_homepage()

    else:
        # use this page
        # Get new_url from this page's list of links
        # new_url = get_random_url_from_page_no_domain("http://www.google.com",from_url)

        new_url = get_random_url_from_page_no_domain(from_url)

        # if there's an error in the above, then do this:
        # new_url = get_random_homepage()

    return new_url


def create_json(url, page_title, site, site_title, next_link=None):
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



@app.route('/ajax/news3/')

# write a new function here for ajax/news3
# use click_link_or_start_over(from_url)
# also need a function...don't want to get pages twice.  When we get a page, should grab its:
# - title
# - url (already have)
# - next_link link to click (random link on the page)
# ...all at once.
# so it should take an optional argument -
    # if arg exists, roll the dice to see if it should be used
    # if not, get new random homepage url
    # proceed with that url
    # get page
    # extract & return title, url, and next_link
    # on the page - use the next_link the next time around in the loop
    #
# draw this out.

def ajax_news_3(news=None):
    print
    print "in ajax_news2"
    try:
        # Pick one (homepage) at random, store as current_site and current_page
        print "calling get_random_homepage()"

        current_site = get_random_homepage()
        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        new_url = get_random_url_from_page(current_site, current_page)
        # print("new_url: ",new_url)

        # if
        if new_url:
            print "was able to get a url from the page"
            # Get the new_url, store as current_page
            current_page = new_url

            # print("current page: ",current_page)

            try:
                # Request current_page
                page = requests.get(current_page)
                tree = html.fromstring(page.content)

                # get the list of a hrefs
                # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                ahrefs = get_list_of_links(tree)
                # print("ahrefs: ",ahrefs)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print "request error:"
                print e
                # sys.exit(1)
                ahrefs = []
                # Create item & append to all_results
                errormsg = "couldn't get current page: " + current_page
                return create_json(
                    url=errormsg,
                    page_title=errormsg,
                    site=errormsg,
                    site_title=errormsg
                )

                # item = {
                #     # 'url': new_url,
                #     'url': errormsg,
                #     'page_title': errormsg,
                #     'site': errormsg,
                #     'site_title': errormsg
                # }
                #
                # # return
                # # return render_template('news_content.html', news=all_results)
                # return render_template('news_item.html', item=item)

            # if the page includes >1 links (seems "real", and we can proceed from here)
            if len(ahrefs) > 1:
                print "list of ahrefs is > 1"

                # Scrape its title, img etc
                title = tree.xpath("//title/text()")
                print "title: %s" % title
                print "page_title: %s" % title[0]
                print "site: %s" % current_site
                # print("new url: ",new_url)

                # need to define this with a regex match
                site_title = ""

                #  Create item & append to all_results
                return create_json(
                    url=current_page,
                    page_title=title[0],
                    site=current_site,
                    site_title=site_title
                )
                # item = {
                #     # 'url': new_url,
                #     'url': current_page,
                #     'page_title': title[0],
                #     'site': current_site,
                #     'site_title': site_title
                # }
                # json_item = json.dumps(item)
                # print "json_item:"
                # print json_item
                #
                # print "item:"
                # print item
                #
                #
                # # return
                # # return render_template('news_content.html', news=all_results)
                # # return render_template('news_item.html', item=item)
                # return json_item

            else:
                # Create item & append to all_results
                errormsg = "couldn't detect >1 hrefs: " + current_page
                return create_json(
                    url=errormsg,
                    page_title=errormsg,
                    site=errormsg,
                    site_title=errormsg
                )
                # item = {
                #     # 'url': new_url,
                #     'url': errormsg,
                #     'page_title': errormsg,
                #     'site': errormsg,
                #     'site_title': errormsg
                # }
                #
                # # return
                # # return render_template('news_content.html', news=all_results)
                # return render_template('news_item.html', item=item)
        else:

            # couldn't get a URL on the current_page

            # Create item & append to all_results
            errormsg = "couldn't get a URL from: " + current_page
            return create_json(
                url=errormsg,
                page_title=errormsg,
                site=errormsg,
                site_title=errormsg
            )
            # item = {
            #     # 'url': new_url,
            #     'url': errormsg,
            #     'page_title': errormsg,
            #     'site': errormsg,
            #     'site_title': errormsg
            # }
            #
            # # return
            # # return render_template('news_content.html', news=all_results)
            # return render_template('news_item.html', item=item)


    except ValueError:
        print "was NOT able to get a url from the page"
        #  Create item & append to all_results
        errormsg = "error"
        return create_json(
            url=errormsg,
            page_title=errormsg,
            site=errormsg,
            site_title=errormsg
        )
        # item = {
        #     # 'url': new_url,
        #     'url': "error",
        #     'page_title': "error",
        #     'site': "error",
        #     'site_title': "error"
        # }
        #
        # # return
        # # return render_template('news_content.html', news=all_results)
        # return render_template('news_item.html', item=item)
        # # return "error on this one"
        # # that's not working, try again.

    #  Create item & append to all_results
    errormsg = "end of ajax/news2"
    return create_json(
        url="",
        page_title=errormsg,
        site=errormsg,
        site_title=errormsg
    )
    # item = {
    #     # 'url': new_url,
    #     'url': "end of ajax/news2",
    #     'page_title': "end of ajax/news2",
    #     'site': "end of ajax/news2",
    #     'site_title': "end of ajax/news2",
    #     'next_url': ""
    # }
    #
    # json_item = json.dumps(item)
    # print "json_item:"
    # print json_item
    #
    # # return
    # # return render_template('news_content.html', news=all_results)
    # return render_template('news_item.html', item=item)


# @app.route('/news/')
@app.route('/ajax/news2/')
# @app.route('/news/<name>')

def ajax_news2(news=None):
    print
    print "in ajax_news2"
    try:
        # Pick one (homepage) at random, store as current_site and current_page
        print "calling get_random_homepage()"

        current_site = get_random_homepage()
        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        new_url = get_random_url_from_page(current_site, current_page)
        # print("new_url: ",new_url)

        # if
        if new_url:
            print "was able to get a url from the page"
            # Get the new_url, store as current_page
            current_page = new_url

            # print("current page: ",current_page)

            try:
                # Request current_page
                page = requests.get(current_page)
                tree = html.fromstring(page.content)

                # get the list of a hrefs
                # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                ahrefs = get_list_of_links(tree)
                # print("ahrefs: ",ahrefs)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print "request error:"
                print e
                # sys.exit(1)
                ahrefs = []
                # Create item & append to all_results
                errormsg = "couldn't get current page: " + current_page
                item = {
                    # 'url': new_url,
                    'url': errormsg,
                    'page_title': errormsg,
                    'site': errormsg,
                    'site_title': errormsg
                }

                # return
                # return render_template('news_content.html', news=all_results)
                return render_template('news_item.html', item=item)

            # if the page includes >1 links (seems "real", and we can proceed from here)
            if len(ahrefs) > 1:
                print "list of ahrefs is > 1"

                # Scrape its title, img etc
                title = tree.xpath("//title/text()")
                print "title: %s" % title
                print "page_title: %s" % title[0]
                print "site: %s" % current_site
                # print("new url: ",new_url)

                # need to define this with a regex match
                site_title = ""

                #  Create item & append to all_results
                item = {
                    # 'url': new_url,
                    'url': current_page,
                    'page_title': title[0],
                    'site': current_site,
                    'site_title': site_title
                }

                print "item:"
                print item

                # return
                # return render_template('news_content.html', news=all_results)
                return render_template('news_item.html', item=item)
            else:
                # Create item & append to all_results
                errormsg = "couldn't detect >1 hrefs: " + current_page
                item = {
                    # 'url': new_url,
                    'url': errormsg,
                    'page_title': errormsg,
                    'site': errormsg,
                    'site_title': errormsg
                }

                # return
                # return render_template('news_content.html', news=all_results)
                return render_template('news_item.html', item=item)
        else:

            # couldn't get a URL on the current_page

            # Create item & append to all_results
            errormsg = "couldn't get a URL from: " + current_page
            item = {
                # 'url': new_url,
                'url': errormsg,
                'page_title': errormsg,
                'site': errormsg,
                'site_title': errormsg
            }

            # return
            # return render_template('news_content.html', news=all_results)
            return render_template('news_item.html', item=item)


    except ValueError:
        print "was NOT able to get a url from the page"
        #  Create item & append to all_results
        item = {
            # 'url': new_url,
            'url': "error",
            'page_title': "error",
            'site': "error",
            'site_title': "error"
        }

        # return
        # return render_template('news_content.html', news=all_results)
        return render_template('news_item.html', item=item)
        # return "error on this one"
        # that's not working, try again.

    #  Create item & append to all_results
    item = {
        # 'url': new_url,
        'url': "end of ajax/news2",
        'page_title': "end of ajax/news2",
        'site': "end of ajax/news2",
        'site_title': "end of ajax/news2"
    }

    # return
    # return render_template('news_content.html', news=all_results)
    return render_template('news_item.html', item=item)


def ajax_news2_old(news=None):

    # @app.stream_with_context
    # def generate():
    #     yield 'Hello '
    #     yield flask.request.args['name']
    #     yield '!'
    # return flask.Response(generate())

    print "starting ajax_news"

    # Setup...
    num_results = 12    # number of results to display
    all_results = []    # objects to hold results
    item = []           # objects to hold results
    count = 0           # counter

    while count < num_results:

        print "-------"
        print "starting outer loop"
        print

        # Pick one (homepage) at random, store as current_site and current_page
        print "calling get_random_homepage()"

        current_site = get_random_homepage()
        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        new_url = get_random_url_from_page(current_site,current_page)
        # print("new_url: ",new_url)

        # if
        if new_url:
            print "was able to get a url from the page"


            # Internal loop from here...
            site_page_count = 1
            # while site_page_count < 4 and count < num_results:
            while site_page_count != 0 and count < num_results:

                print "----"
                print "starting internal loop"

                # Make sure new_url is defined before proceeding
                if (new_url):
                    print "internal loop - was able to get a url from the page"

                    # Get the new_url, store as current_page
                    current_page = new_url

                    # print("current page: ",current_page)

                    try:
                        # Request current_page
                        page = requests.get(current_page)
                        tree = html.fromstring(page.content)

                        # get the list of a hrefs
                        # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                        ahrefs = get_list_of_links(tree)
                        # print("ahrefs: ",ahrefs)
                    except requests.exceptions.RequestException as e:  # This is the correct syntax
                        print e
                        # sys.exit(1)
                        ahrefs = []


                    # if the page includes >1 links (seems "real", and we can proceed from here)
                    if len(ahrefs) > 1:
                        print "list of ahrefs is > 1"

                        # Scrape its title, img etc
                        title = tree.xpath("//title/text()")
                        # print("new url: ",new_url)

                        # need to define this with a regex match
                        site_title = ""

                        #  Create item & append to all_results
                        item = {
                            # 'url': new_url,
                            'url': current_page,
                            'page_title': title[0],
                            'site': current_site,
                            'site_title': site_title
                        }
                        all_results.append(item)

                        # with app.app_context():
                        #     yield render_template('news_item.html', item=item)

                        print "added to all_results: %s" %item

                        # now on to the next
                        # get the next URL to work on and store it as new_url
                        new_url = get_random_url(current_site,ahrefs)
                        # print(get_random_url(current_site,test))
                        print "prepping next URL: %s" % new_url

                        # increment the number of results on the page
                        count = count + 1

                        # # since it all worked, roll the dice here
                        # # generate randomly between 0-x
                        # # internal loop will stop if it's 0
                        # # (so, can change the likelihood by changing 2nd argument)
                        # # lower argument = more likely to start a new site
                        # site_page_count = random.randint(0,2)
                        # print("dice rolled: ",site_page_count)


                    else:
                        print "list of ahrefs is: ",ahrefs
                        # ...get a new URL and loop back around with that one
                        new_url = get_random_url_from_page(current_site,current_site)
                        print "last URL didn't have ahrefs, so prepping next URL: %s" % new_url


                # If new_url is not defined...
                else:
                    # this url is bogus somehow
                    # so reset to the current site and go from there

                    print "new_url is false"
                    print "current_site: %s" % current_site
                    print "current_page: %s" %current_page
                    print

                    # ...get a new URL and loop back around with that one
                    new_url = get_random_url_from_page(current_site,current_site)

                # generate randomly between 0-x
                # internal loop will stop if it's 0
                # (so, can change the likelihood by changing 2nd argument)
                # lower argument = more likely to start a new site
                site_page_count = random.randint(0,2)
                print "dice rolled: %s" % site_page_count

        else:
            print "was not able to get a url from homepage: %s" %current_site


    # return render_template('news.html', news=all_results)
    return render_template('news_content.html', news=all_results)
    # return Response(generate_ajax())





@app.route('/news/')
@app.route('/news/<number_of_results>')
def ajax_practice_news(number_of_results=5):
    return render_template('news.html',number_of_results=number_of_results)
    # print "in news, calling stream()"
    # return Response(stream())



@app.route('/')
def news():
    # return render_template('news.html')
    print "in /, calling stream()"
    return Response(stream())


def generate_ajax():
    # @app.stream_with_context
    # def generate():
    #     yield 'Hello '
    #     yield flask.request.args['name']
    #     yield '!'
    # return flask.Response(generate())

    print "starting ajax_news"

    # Setup...
    num_results = 12    # number of results to display
    all_results = []    # objects to hold results
    item = []           # objects to hold results
    count = 0           # counter

    while count < num_results:

        print "-------"
        print "starting outer loop"
        print

        # Pick one (homepage) at random, store as current_site and current_page
        print "calling get_random_homepage()"

        current_site = get_random_homepage()
        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        new_url = get_random_url_from_page(current_site,current_page)
        # print("new_url: ",new_url)

        # if
        if new_url:
            print "was able to get a url from the page"


            # Internal loop from here...
            site_page_count = 1
            # while site_page_count < 4 and count < num_results:
            while site_page_count != 0 and count < num_results:

                print "----"
                print "starting internal loop"

                # Make sure new_url is defined before proceeding
                if (new_url):
                    print "internal loop - was able to get a url from the page"

                    # Get the new_url, store as current_page
                    current_page = new_url

                    # print("current page: ",current_page)

                    try:
                        # Request current_page
                        page = requests.get(current_page)
                        tree = html.fromstring(page.content)

                        # get the list of a hrefs
                        # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                        ahrefs = get_list_of_links(tree)
                        # print("ahrefs: ",ahrefs)
                    except requests.exceptions.RequestException as e:  # This is the correct syntax
                        print e
                        # sys.exit(1)
                        ahrefs = []


                    # if the page includes >1 links (seems "real", and we can proceed from here)
                    if len(ahrefs) > 1:
                        print "list of ahrefs is > 1"

                        # Scrape its title, img etc
                        title = tree.xpath("//title/text()")
                        # print("new url: ",new_url)

                        # need to define this with a regex match
                        site_title = ""

                        #  Create item & append to all_results
                        item = {
                            # 'url': new_url,
                            'url': current_page,
                            'page_title': title[0],
                            'site': current_site,
                            'site_title': site_title
                        }
                        all_results.append(item)

                        print
                        print
                        print "WITH APP.APP_CONTEXT"
                        print
                        print

                        with app.app_context():
                            print
                            print
                            print "YIELD NOW"
                            print
                            print
                            yield render_template('news_item.html', item=item)
                            print
                            print
                            print "YIELDED"
                            print
                            print



                        print "added to all_results: %s" %item

                        # now on to the next
                        # get the next URL to work on and store it as new_url
                        new_url = get_random_url(current_site,ahrefs)
                        # print(get_random_url(current_site,test))
                        print "prepping next URL: %s" % new_url

                        # increment the number of results on the page
                        count = count + 1

                        # # since it all worked, roll the dice here
                        # # generate randomly between 0-x
                        # # internal loop will stop if it's 0
                        # # (so, can change the likelihood by changing 2nd argument)
                        # # lower argument = more likely to start a new site
                        # site_page_count = random.randint(0,2)
                        # print("dice rolled: ",site_page_count)


                    else:
                        print "list of ahrefs is: ",ahrefs
                        # ...get a new URL and loop back around with that one
                        new_url = get_random_url_from_page(current_site,current_site)
                        print "last URL didn't have ahrefs, so prepping next URL: %s" % new_url


                # If new_url is not defined...
                else:
                    # this url is bogus somehow
                    # so reset to the current site and go from there

                    print "new_url is false"
                    print "current_site: %s" % current_site
                    print "current_page: %s" %current_page
                    print

                    # ...get a new URL and loop back around with that one
                    new_url = get_random_url_from_page(current_site,current_site)

                # generate randomly between 0-x
                # internal loop will stop if it's 0
                # (so, can change the likelihood by changing 2nd argument)
                # lower argument = more likely to start a new site
                site_page_count = random.randint(0,2)
                print "dice rolled: %s" % site_page_count

        else:
            print "was not able to get a url from homepage: %s" %current_site



# @app.route('/news/')
@app.route('/ajax/news/')
# @app.route('/news/<name>')

def ajax_news(news=None):

    # # @app.stream_with_context
    # # def generate():
    # #     yield 'Hello '
    # #     yield flask.request.args['name']
    # #     yield '!'
    # # return flask.Response(generate())
    #
    # print "starting ajax_news"
    #
    # # Setup...
    # num_results = 12    # number of results to display
    # all_results = []    # objects to hold results
    # item = []           # objects to hold results
    # count = 0           # counter
    #
    # while count < num_results:
    #
    #     print "-------"
    #     print "starting outer loop"
    #     print
    #
    #     # Pick one (homepage) at random, store as current_site and current_page
    #     print "calling get_random_homepage()"
    #
    #     current_site = get_random_homepage()
    #     current_page = current_site
    #
    #     # Get a random URL from that page to work with, assign to new_url
    #     new_url = get_random_url_from_page(current_site,current_page)
    #     # print("new_url: ",new_url)
    #
    #     # if
    #     if new_url:
    #         print "was able to get a url from the page"
    #
    #
    #         # Internal loop from here...
    #         site_page_count = 1
    #         # while site_page_count < 4 and count < num_results:
    #         while site_page_count != 0 and count < num_results:
    #
    #             print "----"
    #             print "starting internal loop"
    #
    #             # Make sure new_url is defined before proceeding
    #             if (new_url):
    #                 print "internal loop - was able to get a url from the page"
    #
    #                 # Get the new_url, store as current_page
    #                 current_page = new_url
    #
    #                 # print("current page: ",current_page)
    #
    #                 try:
    #                     # Request current_page
    #                     page = requests.get(current_page)
    #                     tree = html.fromstring(page.content)
    #
    #                     # get the list of a hrefs
    #                     # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
    #                     ahrefs = get_list_of_links(tree)
    #                     # print("ahrefs: ",ahrefs)
    #                 except requests.exceptions.RequestException as e:  # This is the correct syntax
    #                     print e
    #                     # sys.exit(1)
    #                     ahrefs = []
    #
    #
    #                 # if the page includes >1 links (seems "real", and we can proceed from here)
    #                 if len(ahrefs) > 1:
    #                     print "list of ahrefs is > 1"
    #
    #                     # Scrape its title, img etc
    #                     title = tree.xpath("//title/text()")
    #                     # print("new url: ",new_url)
    #
    #                     # need to define this with a regex match
    #                     site_title = ""
    #
    #                     #  Create item & append to all_results
    #                     item = {
    #                         # 'url': new_url,
    #                         'url': current_page,
    #                         'page_title': title[0],
    #                         'site': current_site,
    #                         'site_title': site_title
    #                     }
    #                     all_results.append(item)
    #
    #                     with app.app_context():
    #                         yield render_template('news_item.html', item=item)
    #
    #                     print "added to all_results: %s" %item
    #
    #                     # now on to the next
    #                     # get the next URL to work on and store it as new_url
    #                     new_url = get_random_url(current_site,ahrefs)
    #                     # print(get_random_url(current_site,test))
    #                     print "prepping next URL: %s" % new_url
    #
    #                     # increment the number of results on the page
    #                     count = count + 1
    #
    #                     # # since it all worked, roll the dice here
    #                     # # generate randomly between 0-x
    #                     # # internal loop will stop if it's 0
    #                     # # (so, can change the likelihood by changing 2nd argument)
    #                     # # lower argument = more likely to start a new site
    #                     # site_page_count = random.randint(0,2)
    #                     # print("dice rolled: ",site_page_count)
    #
    #
    #                 else:
    #                     print "list of ahrefs is: ",ahrefs
    #                     # ...get a new URL and loop back around with that one
    #                     new_url = get_random_url_from_page(current_site,current_site)
    #                     print "last URL didn't have ahrefs, so prepping next URL: %s" % new_url
    #
    #
    #             # If new_url is not defined...
    #             else:
    #                 # this url is bogus somehow
    #                 # so reset to the current site and go from there
    #
    #                 print "new_url is false"
    #                 print "current_site: %s" % current_site
    #                 print "current_page: %s" %current_page
    #                 print
    #
    #                 # ...get a new URL and loop back around with that one
    #                 new_url = get_random_url_from_page(current_site,current_site)
    #
    #             # generate randomly between 0-x
    #             # internal loop will stop if it's 0
    #             # (so, can change the likelihood by changing 2nd argument)
    #             # lower argument = more likely to start a new site
    #             site_page_count = random.randint(0,2)
    #             print "dice rolled: %s" % site_page_count
    #
    #     else:
    #         print "was not able to get a url from homepage: %s" %current_site


    # return render_template('news.html', news=all_results)
    # return render_template('news_content.html', news=all_results)
    return Response(generate_ajax())




@app.route('/hello/')
@app.route('/hello/<name>.html')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)






# OK, going to need a "get next page" ajax function that takes the current page and returns either a link or a new homepage

# main function just renders news.html
# update news.html to make the ajax request
# probably count # of responses in news.html
# ajax function should take args: currentPage, excludePages(list)


@app.route('/ajax')
@app.route('/ajax/<number_of_results>')

def ajax_response(number_of_results=12):
    print "in streamed_response"
    def generate():
        # yield 'Hello '
        # # yield request.args['name']
        # yield '!'
        print "in generate()"

        yield render_template('news2_header.html')
        print "yielded"

        print "generate_ajax()"
        # yield generate_ajax()







        # @app.stream_with_context
        # def generate():
        #     yield 'Hello '
        #     yield flask.request.args['name']
        #     yield '!'
        # return flask.Response(generate())

        print "starting ajax_news"

        # Setup...
        # num_results = 12  # number of results to display
        num_results = int(number_of_results)  # number of results to display
        all_results = []  # objects to hold results
        item = []  # objects to hold results
        count = 0  # counter

        print "number of results: %s" % number_of_results

        while count < num_results:

            print "-------"
            print "starting outer loop"
            print "count: %s" % count
            print "num_results: %s" % num_results
            print

            # Pick one (homepage) at random, store as current_site and current_page
            print "calling get_random_homepage()"

            current_site = get_random_homepage()
            current_page = current_site

            # Get a random URL from that page to work with, assign to new_url
            new_url = get_random_url_from_page(current_site, current_page)
            # print("new_url: ",new_url)

            # if
            if new_url:
                print "was able to get a url from the page"

                # Internal loop from here...
                site_page_count = 1
                # while site_page_count < 4 and count < num_results:
                while site_page_count != 0 and count < num_results:

                    print "----"
                    print "starting internal loop"

                    # Make sure new_url is defined before proceeding
                    if (new_url):
                        print "internal loop - was able to get a url from the page"

                        # Get the new_url, store as current_page
                        current_page = new_url

                        # print("current page: ",current_page)

                        try:
                            # Request current_page
                            page = requests.get(current_page)
                            tree = html.fromstring(page.content)

                            # get the list of a hrefs
                            # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
                            ahrefs = get_list_of_links(tree)
                            # print("ahrefs: ",ahrefs)
                        except requests.exceptions.RequestException as e:  # This is the correct syntax
                            print e
                            # sys.exit(1)
                            ahrefs = []

                        # if the page includes >1 links (seems "real", and we can proceed from here)
                        if len(ahrefs) > 1:
                            print "list of ahrefs is > 1"

                            # Scrape its title, img etc
                            title = tree.xpath("//title/text()")
                            # print("new url: ",new_url)

                            # need to define this with a regex match
                            site_title = ""

                            #  Create item & append to all_results
                            item = {
                                # 'url': new_url,
                                'url': current_page,
                                'page_title': title[0],
                                'site': current_site,
                                'site_title': site_title
                            }
                            all_results.append(item)

                            print
                            print
                            print "WITH APP.APP_CONTEXT"
                            print
                            print

                            with app.app_context():
                                print
                                print
                                print "YIELD NOW"
                                print
                                print

                                yield render_template('news_item.html', item=item)

                                print
                                print
                                print "YIELDED"
                                print
                                print

                            print "added to all_results: %s" % item

                            # now on to the next
                            # get the next URL to work on and store it as new_url
                            new_url = get_random_url(current_site, ahrefs)
                            # print(get_random_url(current_site,test))
                            print "prepping next URL: %s" % new_url

                            # increment the number of results on the page
                            count = count + 1

                            # # since it all worked, roll the dice here
                            # # generate randomly between 0-x
                            # # internal loop will stop if it's 0
                            # # (so, can change the likelihood by changing 2nd argument)
                            # # lower argument = more likely to start a new site
                            # site_page_count = random.randint(0,2)
                            # print("dice rolled: ",site_page_count)


                        else:
                            print "list of ahrefs is: ", ahrefs
                            # ...get a new URL and loop back around with that one
                            new_url = get_random_url_from_page(current_site, current_site)
                            print "last URL didn't have ahrefs, so prepping next URL: %s" % new_url


                    # If new_url is not defined...
                    else:
                        # this url is bogus somehow
                        # so reset to the current site and go from there

                        print "new_url is false"
                        print "current_site: %s" % current_site
                        print "current_page: %s" % current_page
                        print

                        # ...get a new URL and loop back around with that one
                        new_url = get_random_url_from_page(current_site, current_site)

                    # generate randomly between 0-x
                    # internal loop will stop if it's 0
                    # (so, can change the likelihood by changing 2nd argument)
                    # lower argument = more likely to start a new site
                    site_page_count = random.randint(0, 2)
                    print "dice rolled: %s" % site_page_count

            else:
                print "was not able to get a url from homepage: %s" % current_site






        yield render_template('news2_footer.html')
        print "yielded"
    return Response(stream_with_context(generate()))





if __name__ == '__main__':
    app.run(debug=True)
