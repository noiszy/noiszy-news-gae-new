// writes a site to the site list on the page
function write_news_item(site, title, link, divId, fromPage, siteTitle, i) {
    // console.log("");
    // console.log("");
    // console.log("in write_news_item");
    // console.log("site: ", site);
    // console.log("title: ", title);
    // console.log("link: ", link);
    // console.log("div: ", divId);
    // console.log("fromPage: ", fromPage);
    // console.log("siteTitle: ", siteTitle);
    // console.log("i: ", i);

  var thiswrapper, thisid, thisurl, thisinput, thislabel, thisdelete;
  thisid = "item" + i;
  thisurl = site.url;

  thiswrapper = document.createElement("div");
  thiswrapper.setAttribute("class","news_item");
//  thiswrapper.setAttribute("data-val",thisurl);
//  thiswrapper.setAttribute("data-id",thisid);

  thisa = document.createElement("a");
  thisa.setAttribute("href", link);

  thistitle = document.createElement("span");
  thistitle.setAttribute("class", "href-title");
  thistitle.innerHTML = title;

  thishref = document.createElement("span");
  thishref.setAttribute("class", "href-destination");
  thishref.innerHTML = link;

  thissite = document.createElement("span");
  thissite.setAttribute("class", "href-site");
  // thissite.innerHTML = site;
  // thissite.innerHTML = title;
  thissite.innerHTML = "From site: " + siteTitle;

  thisFromPage = document.createElement("span");
  thisFromPage.setAttribute("class", "href-site");
  thisFromPage.innerHTML = "linked from " + fromPage;

  thisa.appendChild(thissite);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(thisFromPage);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(thistitle);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(thishref);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(document.createElement("br"));

  thiswrapper.appendChild(thisa);


  var inDiv = document.getElementById(divId);
  console.log('divId: ',divId)
  console.log('idDiv: ',inDiv)
  //
  // news_items_wrapper.appendChild(thiswrapper);

  inDiv.appendChild(thiswrapper);

  return;
}



function write_news_wrapper(total_num_results) {

    // anything we want to set up goes here...
    window.nn_counter = 0;

    // now call the function to write the news items, passing the max # of results
    write_news(total_num_results);

    // cleanup
    $("#loading").empty();
}



function write_news(total_num_results) {

    // get a whole site's worth of news
    // response will contain a collection of items

    //for now: leave this as a constant, but it should be the max remaining results
    var max_results_per_site = 6;
    console.log("total_num_results: ",total_num_results);
    console.log("window.nn_counter: ",window.nn_counter);


    results_to_get = Math.min(total_num_results - window.nn_counter, max_results_per_site)

    // call the py function via the URL
    // write the results, incrementing window.nn_counter
    // if window.nn_counter < total_num_results, call write_news again

    //call the python function via URL - /ajax/news5 -
    // $("<div>").load("/ajax/news5/"+total_num_results, function (collection) {
    $("<div>").load("/ajax/news5/"+results_to_get, function (collection) {

        json_collection = JSON.parse(collection);

        var response;

        var nni_items_length = json_collection['length'];
        nni_items = json_collection['items'];

        for (var j = 0; j < nni_items_length; j++){
            response = nni_items[j];

            json_response = response;

            write_news_item(
                site = json_response.site,
                title = json_response.page_title,
                link = json_response.url,
                divId = "news_items_wrapper",
                fromPage = json_response.from_page,
                siteTitle = json_response.site_title,
                i = total_num_results
            );

            window.nn_counter++;

            // should probably move this outside the loop
//            $("#loading").empty();
        }


        // let's see if this works.
        if (window.nn_counter < total_num_results) {
            console.log("")
            console.log("still not enough!");
            console.log("need "+total_num_results);
            console.log("only have " + window.nn_results);

            write_news(total_num_results);
        } else {
            // done!
            $("#loading").empty();
        }
    });

//    $("#loading").empty();

}