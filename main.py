from flask import Flask, Response, request, stream_with_context

from flask import render_template

import argparse
import sys
import re
import random
import json
import time
import noiszy_news

#####
# implement this fix:
# incomplete read article: http://stackoverflow.com/questions/14442222/how-to-handle-incompleteread-in-python


# from google.appengine.api import urlfetch

from lxml import html
import requests
# import requests_toolbelt.adapters.appengine
#
# # Use the App Engine Requests adapter. This makes sure that Requests uses
# # URLFetch.
# requests_toolbelt.adapters.appengine.monkeypatch()


app = Flask(__name__)


#########
# TO DO:
# errors on requests - try different URLs (protocol, etc)
# update page via ajax each time a result is loaded
# if new url is the same as the last url, skip it
#########



# calls /ajax/news3/
@app.route('/news/')
@app.route('/news/<number_of_results>')
def ajax_practice_news(number_of_results=5):
    return render_template('news.html',number_of_results=number_of_results)
    # print "in news, calling stream()"



@app.route('/ajax/news3/')

def ajax_news_3(news=None):
    print
    print "in ajax_news3"
    try:
        # Pick one (homepage) at random, store as current_site and current_page
        # print "calling get_random_homepage()"
        current_site = noiszy_news.get_random_homepage()

        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        new_url = noiszy_news.get_random_url_from_page(current_page)
        # print("new_url: ",new_url)

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
                ahrefs = noiszy_news.get_list_of_links(tree,current_page)
                # print("ahrefs: ",ahrefs)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print "request error:"
                print e
                ahrefs = []
                # Create item & append to all_results
                errormsg = "couldn't get current page: " + current_page
                return noiszy_news.create_json(error=errormsg)

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
                return noiszy_news.create_json(
                    url=current_page,
                    page_title=title[0],
                    site=current_site,
                    site_title=site_title
                )

            else:
                # Create item & append to all_results
                errormsg = "couldn't detect >1 hrefs: " + current_page
                return noiszy_news.create_json(error=errormsg)

        else:

            # couldn't get a URL on the current_page

            # Create item & append to all_results
            errormsg = "couldn't get a URL from: " + current_page
            return noiszy_news.create_json(error=errormsg)

    except ValueError:
        print "was NOT able to get a url from the page"
        #  Create item & append to all_results
        errormsg = "error"
        return noiszy_news.create_json(error=errormsg)

    #  Create item & append to all_results
    errormsg = "end of ajax/news2"
    return noiszy_news.create_json(error=errormsg)






@app.route('/hello/')
@app.route('/hello/<name>.html')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)




if __name__ == '__main__':
    app.run(debug=True)
