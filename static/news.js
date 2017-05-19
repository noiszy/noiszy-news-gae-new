// writes a site to the site list on the page
function write_news_item(site, title, link, div, i) {
    console.log("in write_news_item");
  var thiswrapper, thisid, thisurl, thisinput, thislabel, thisdelete;
  thisid = "item" + i;
  thisurl = site.url;

  thiswrapper = document.createElement("div");
  thiswrapper.setAttribute("class","news_item");
//  thiswrapper.setAttribute("data-val",thisurl);
//  thiswrapper.setAttribute("data-id",thisid);

  thisa = document.createElement("a");
  thisa.setAttribute("href", "link");

  thistitle = document.createElement("span");
  thistitle.setAttribute("class", "href-title");
  thistitle.innerHTML = title;

  thishref = document.createElement("span");
  thishref.setAttribute("class", "href-destination");
  thishref.innerHTML = link;

  thissite = document.createElement("span");
  thissite.setAttribute("class", "href-site");
  thissite.innerHTML = site;

  thisa.appendChild(thissite);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(thistitle);
  thisa.appendChild(document.createElement("br"));
  thisa.appendChild(thishref);
  thisa.appendChild(document.createElement("br"));

  thiswrapper.appendChild(thisa);


  var news_items_wrapper = document.getElementById("news_items_wrapper");

  news_items_wrapper.appendChild(thiswrapper);

  return;
}

