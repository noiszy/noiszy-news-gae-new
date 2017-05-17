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
    try:
        page = requests.get(url)
        # page = urlfetch.fetch(url)
        tree = html.fromstring(page.content)

        # Get links on the page
        # Need to refine this with CSS selector

        # test = tree.xpath('//title/text()')
        # test = tree.xpath("//a[@href]/text()")
        # test = tree.xpath("//a[@href]/@href")
        # test = tree.xpath("//a[not(contains(@href,'//'))]/@href")
        # ahrefs = tree.xpath("//a[contains(@href,'/') and not(contains(@href,'//'))]/@href")
        ahrefs = get_list_of_links(tree)

        # Choose one at random, and set it as new_url
        url = get_random_url(protocol_and_domain,ahrefs)
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

    with open('static/site_list.json') as json_data:
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



# @app.route('/news/')
@app.route('/')
def news():
    # return render_template('news.html')
    print "in news, calling stream()"
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




if __name__ == '__main__':
    app.run(debug=True)
