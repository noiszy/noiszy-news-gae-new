from flask import Flask, Response, request, stream_with_context

from flask import render_template

import argparse
import sys
import re
import random
import json
import time
import noiszy_news
import nn_utils
import noiszy_news_object


#####
# implement this fix:
# incomplete read article: http://stackoverflow.com/questions/14442222/how-to-handle-incompleteread-in-python

#####
# Fix: xpath so that we can't create new news items from domains that don't match the site


from lxml import html
import requests


app = Flask(__name__)


#########
# TO DO:
# errors on requests - try different URLs (protocol, etc)
# update page via ajax each time a result is loaded
# if new url is the same as the last url, skip it
#########




# @app.route('/news5/')
# @app.route('/news5/<number_of_results>')
@app.route('/')
@app.route('/<number_of_results>')
def deep_news(number_of_results=10): # default num results here
    num = int(number_of_results)
    print num
    if num > 20: # max num results here
        num = 20;
    return render_template('news5.html',number_of_results=num)
    # print "in news, calling stream()"



@app.route('/ajax/news5/')
@app.route('/ajax/news5/<max_results>')

def ajax_news_5(max_results=10,news=None,show_errors=False):

    print
    print
    print "in ajax_news4"
    print "get max results: %s" % max_results

    try:

        # For right now - always starting at the homepage
        # Update this.

        # Pick one (homepage) at random, store as current_site and current_page
        # print "calling get_random_homepage()"

        current_site_obj = nn_utils.get_random_homepage()

        current_site = current_site_obj['url']
        current_site_title = current_site_obj['title']

        current_page = current_site

        # Get a random URL from that page to work with, assign to new_url
        # new_url = noiszy_news.get_random_url_from_page(current_page)

        # set up base values:
        from_page = "start new site"
        i = 0
        nni_list = []

        # start loop
        while i < int(max_results):

            print "starting loop, i = %s" % i

            # get an nni from the current page:
            nni = noiszy_news.get_nn_item(
                url=current_page,
                from_page=from_page,
                exclude=[]
            )

            print "got nni from current_page"
            print nni

            # check for errors
            if nni['error']:
                # while debugging, go ahead and return this and print out the error
                # if not debugging, should just do nothing with return values like this

                print "##### got errormessage: %s #####" % nni['error']
                errormsg = "couldn't get link on homepage %s " % current_page

                if show_errors:
                    nni_obj1 = nn_utils.create_nni_obj(error=errormsg)
                    nni_list.append(nni_obj1)

                # end the loop
                i = max_results


            else:

                # good result, so create & add it to the list of pages
                nni_obj1 = nn_utils.create_nni_obj(
                    url=nni['url'],
                    page_title=nni['title'],
                    site=current_site,
                    site_title=current_site_title,
                    next_link=nni['next_page'],
                    from_page=nni['from_page']
                )

                nni_list.append(nni_obj1)
                print "nni_list: %s" % nni_list

                # when done with item, swap out values
                current_page = nni['next_page']
                from_page = nni['url']

                # roll the dice to see if we're going to get a new item or return
                dice = random.randint(0, 3)
                if (dice == 0):
                    # get out
                    i = max_results
                else:
                    # just increment & move on
                    i = i+1

        # when done with the list, return
        return nn_utils.create_json_response(nni_list)


    except ValueError:
        print "was NOT able to get a url from the homepage"
        #  Create item & append to all_results
        errormsg = "error"
        # return [noiszy_news.create_json(error=errormsg)]
        nni_obj1 = nn_utils.create_nni_obj(error=errormsg)
        nni_list = [nni_obj1]
        nni_list_json = json.dumps(nni_list)
        return nni_list_json

        #  Create item & append to all_results
    errormsg = "was NOT able to get a url from the homepage - end of ajax/news5"
    return [noiszy_news.create_json(error=errormsg)]




@app.route('/hello/')
@app.route('/hello/<name>.html')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)




if __name__ == '__main__':
    app.run(debug=True)
