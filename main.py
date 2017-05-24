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



# # calls /ajax/news3/
# @app.route('/news/')
# @app.route('/news/<number_of_results>')
# def news(number_of_results=10): # default num results here
#     num = int(number_of_results)
#     print num
#     if num > 20: # max num results here
#         num = 20;
#     return render_template('news.html',number_of_results=num)
#     # print "in news, calling stream()"
#
#
#
# @app.route('/ajax/news3/')
#
# def ajax_news_3(news=None):
#
#     print
#     print
#     print "in ajax_news3"
#     try:
#
#         # For right now - always starting at the homepage
#         # Update this.
#
#         # Pick one (homepage) at random, store as current_site and current_page
#         # print "calling get_random_homepage()"
#
#         current_site_obj = nn_utils.get_random_homepage()
#
#         current_site = current_site_obj['url']
#         current_site_title = current_site_obj['title']
#
#         current_page = current_site
#
#         # Get a random URL from that page to work with, assign to new_url
#         # new_url = noiszy_news.get_random_url_from_page(current_page)
#
#         nn = noiszy_news.get_random_url_from_page(current_page)
#         print "got nn.get_random_url_from_page:"
#         print nn
#
#         # check for errors
#         if nn['error']:
#             # while debugging, go ahead and return this and print out the error
#             # if not debugging, should just do nothing with return values like this
#
#             print "##### got errormessage: %s #####" % nn['error']
#             errormsg = "couldn't get link on homepage %s " % current_page
#             return nn_utils.create_json(error=errormsg)
#
#         else:
#             new_url = nn['new_url']
#             current_page = nn['url'] # redundant
#             # print("new_url: ",new_url)
#
#             # if new_url:
#             print "was able to get a url from the page"
#             # Get the new_url, store as current_page
#             # current_page = new_url
#             print("current page: ",current_page)
#             print("new_url: ",new_url)
#
#             # now we have the url of a page linked to from the home page
#             # but we need the content of that page to create the news item.
#             # so, get the content of that page now.
#
#
#             #####
#             # need to split out function to get page contents, and one to get a random link
#             # can wrap both of those up togehter
#             # add to functions: success param, or "# of hrefs" - something to trigger error sfrom
#
#             # nni = noiszy_news.get_nn_item(current_page,nn['url'])
#             nni = noiszy_news.get_nn_item(new_url,current_page)
#
#             nni_json = nn_utils.create_json(
#                 url=nni['url'],
#                 page_title=nni['title'],
#                 site=current_site,
#                 site_title=current_site_title,
#                 next_link=nni['next_page'],
#                 from_page=nni['from_page']
#             )
#
#             print "nni_json: %s" % nni_json
#             return nni_json
#
#
#
#     except ValueError:
#         print "was NOT able to get a url from the page"
#         #  Create item & append to all_results
#         errormsg = "error"
#         return noiszy_news.create_json(error=errormsg)
#
#     #  Create item & append to all_results
#     errormsg = "end of ajax/news2"
#     return noiszy_news.create_json(error=errormsg)
#
#



# # calls /ajax/news4/
# @app.route('/deep_news/')
# @app.route('/deep_news/<number_of_results>')
# def deep_news(number_of_results=10): # default num results here
#     num = int(number_of_results)
#     print num
#     if num > 20: # max num results here
#         num = 20;
#     return render_template('deep_news.html',number_of_results=num)
#     # print "in news, calling stream()"
#
#
#
# @app.route('/ajax/news4/')
#
# def ajax_news_4(news=None):
#
#     print
#     print
#     print "in ajax_news4"
#     try:
#
#         # For right now - always starting at the homepage
#         # Update this.
#
#         # Pick one (homepage) at random, store as current_site and current_page
#         # print "calling get_random_homepage()"
#
#         current_site_obj = nn_utils.get_random_homepage()
#
#         current_site = current_site_obj['url']
#         current_site_title = current_site_obj['title']
#
#         current_page = current_site
#
#         # Get a random URL from that page to work with, assign to new_url
#         # new_url = noiszy_news.get_random_url_from_page(current_page)
#
#         nn = noiszy_news.get_random_url_from_page(current_page)
#         print "got nn.get_random_url_from_page:"
#         print nn
#
#         # check for errors
#         if nn['error']:
#             # while debugging, go ahead and return this and print out the error
#             # if not debugging, should just do nothing with return values like this
#
#             print "##### got errormessage: %s #####" % nn['error']
#             errormsg = "couldn't get link on homepage %s " % current_page
#             return [nn_utils.create_json(error=errormsg)]
#
#         else:
#             new_url = nn['new_url']
#             current_page = nn['url'] # redundant
#             # print("new_url: ",new_url)
#
#             # if new_url:
#             print "was able to get a url from the page"
#             # Get the new_url, store as current_page
#             # current_page = new_url
#             print("current page: ",current_page)
#             print("new_url: ",new_url)
#
#             # now we have the url of a page linked to from the home page
#             # but we need the content of that page to create the news item.
#             # so, get the content of that page now.
#
#
#             #####
#             # need to split out function to get page contents, and one to get a random link
#             # can wrap both of those up togehter
#             # add to functions: success param, or "# of hrefs" - something to trigger error sfrom
#
#             # nni = noiszy_news.get_nn_item(current_page,nn['url'])
#             nni = noiszy_news.get_nn_item(new_url,current_page)
#
#
#             # update this function (nn_utils.create_json) to work with an array of these obj
#             # nni_json = nn_utils.create_json(
#             #     url=nni['url'],
#             #     page_title=nni['title'],
#             #     site=current_site,
#             #     site_title=current_site_title,
#             #     next_link=nni['next_page'],
#             #     from_page=nni['from_page']
#             # )
#
#             nni_obj1 = {
#                 'url': nni['url'],
#                 'page_title': nni['title'],
#                 'site': current_site,
#                 'site_title': current_site_title,
#                 'next_link': nni['next_page'],
#                 'from_page': nni['from_page']
#             }
#
#
#             #######
#             # SEND BACK MULTIPLE ONES
#
#
#             # print "nni_json: %s" % nni_json
#             nni_list = [nni_obj1]
#             print "nni_list: %s" % nni_list
#             nni_list_json = json.dumps(nni_list)
#             print "nni_list_json: %s" % nni_list_json
#             return nni_list_json
#
#
#
#     except ValueError:
#         print "was NOT able to get a url from the page"
#         #  Create item & append to all_results
#         errormsg = "error"
#         return [noiszy_news.create_json(error=errormsg)]
#
#     #  Create item & append to all_results
#     errormsg = "end of ajax/news2"
#     return [noiszy_news.create_json(error=errormsg)]



# calls /ajax/news4/
@app.route('/news5/')
@app.route('/news5/<number_of_results>')
def deep_news(number_of_results=10): # default num results here
    num = int(number_of_results)
    print num
    if num > 20: # max num results here
        num = 20;
    return render_template('news5.html',number_of_results=num)
    # print "in news, calling stream()"



@app.route('/ajax/news5/')
@app.route('/ajax/news5/<max_results>')

def ajax_news_5(max_results=10,news=None):

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
