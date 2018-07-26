import lib.moviegrabber.mg_tools_downloader as mg_tools_downloader
import xmltodict

#
# example with keyword filter (1080p)
# http://192.168.1.10:1900/api/v2.0/indexers/all/results/torznab/api?apikey=o4xte43ftp56m64aknxch4pe7cp3lhaj&t=search&cat=&q=1080p&
#
# example with cat filtering
# http://192.168.1.10:1900/api/v2.0/indexers/all/results/torznab/api?apikey=o4xte43ftp56m64aknxch4pe7cp3lhaj&t=search&cat=5050&q=1080p&
#
# example with movie category and 1080p and bluray query filter
# http://192.168.1.10:1900/api/v2.0/indexers/all/results/torznab/api?apikey=o4xte43ftp56m64aknxch4pe7cp3lhaj&t=search&cat=2000&q=1080p%20bluray&extended=1
#
# example with limit of 10 results
# http://192.168.1.10:1900/api/v2.0/indexers/all/results/torznab/api?apikey=o4xte43ftp56m64aknxch4pe7cp3lhaj&t=search&cat=&extended=1&seeders=10000&q=&limit=10&maxage=10
#
# list of categories:-
# 2000	Movies
# 2010	Movies/Foreign
# 2020	Movies/Other
# 2030	Movies/SD
# 2040	Movies/HD
# 2045	Movies/UHD
# 2050	Movies/BluRay
# 2060	Movies/3D
#
# note looks like you cannot specify output as json thus use xml2dict
#
# input will be logger, host ip, post port, apikey, pos keyword filters, categories, limit
# output will be list containing dict, value of dict can be list also
#
# MG calls
#   torznab_download calls
#   torznab_result returns items will be:- title, *magnet, *torrent, *nzb, *details, *seeders, *peers, *imdb_tt, size, date, *nfo, *id
#
#   * = optional
#
#   e.g. return from torznab_result would look like:- [[{"title" : "ghostbusters"}, {"magnet" : "dfgsdfgdfdfgsdf"}], [{"title" : "ghostbusters2"}, {"magnet" : "eqweqweqweqwe"}]]
#
# MG processes list of dicts for each group against the filters


# in logger_instance,kwargs for construct url (host, port, api_key, category, search, limit, user_agent)
# out return_code, status_code, content
def torznab_download(logger_instance, kwargs, site_name):

    if kwargs is not None:

        if "host" in kwargs:
            host = kwargs['host']
        else:
            logger_instance.warning(u'No hostname sent to function, exiting function...')
            return 1, None

        if "port" in kwargs:
            port = kwargs['port']
        else:
            logger_instance.warning(u'No port sent to function, exiting function...')
            return 1, None

        if "api_key" in kwargs:
            api_key = kwargs['api_key']
        else:
            logger_instance.warning(u'No api_key sent to function, exiting function...')
            return 1, None

        if "category" in kwargs:
            category = kwargs['category']
        else:
            logger_instance.warning(u'No category sent to function, exiting function...')
            return 1, None

        if "search" in kwargs:
            search = kwargs['search']
            search = search.replace(",", " ")
        else:
            logger_instance.warning(u'No search sent to function, exiting function...')
            return 1, None

        if "limit" in kwargs:
            limit = kwargs['limit']
        else:
            logger_instance.warning(u'No limit sent to function, exiting function...')
            return 1, None

        if "user_agent" in kwargs:
            user_agent = kwargs['user_agent']
        else:
            logger_instance.warning(u'No user_agent sent to function, exiting function...')
            return 1, None

        if "read_timeout" in kwargs:
            read_timeout = kwargs['read_timeout']
        else:
            read_timeout = 30.0
            logger_instance.info(u'No read timeout sent to function, defaulting to %s seconds' % read_timeout)

    else:

        logger_instance.warning(u'No keyword args sent to function, exiting function...')
        return 1

    # construct url for api
    url = "http://%s:%s/api/v2.0/indexers/all/results/torznab/api?apikey=%s&t=search&cat=%s&q=%s&extended=1&maxage=%s" % (host, port, api_key, category, search, limit)
    logger_instance.debug(u"%s Index - Site feed URL %s" % (site_name, url))

    # download torznab results using requests
    return_code, status_code, content = mg_tools_downloader.http_client(logger_instance, url=url, user_agent=user_agent, request_type="get", read_timeout=read_timeout)
    return content


# in logger_instance, content
# out return_code, title, *magnet, *torrent, *nzb, *details, *seeders, *peers, *imdb_tt, size, date, *nfo, *id
def torznab_result(logger_instance, content, site_name):

    try:

        # parse xml formatted feed
        site_feed_parse = xmltodict.parse(content, process_namespaces=True)
        site_feed_parse = site_feed_parse["rss"]["channel"]["item"]

    except (ValueError, TypeError, KeyError):

        logger_instance.warning(u"%s Index - Site feed parse failed" % site_name)
        return 1

    movie_item_list = []

    # this breaks down the rss feed page into tag sections
    for node in site_feed_parse:

        seeders = None
        peers = None
        magneturl = None
        torrenturl = None

        list_named_attributes = node['http://torznab.com/schemas/2015/feed:attr']

        for i in list_named_attributes:

            attribute_name = i['@name']

            if attribute_name == "seeders":

                seeders = i['@value']

            if attribute_name == "peers":

                peers = i['@value']

            if attribute_name == "magneturl":

                magneturl = i['@value']

        try:

            title = node["title"]

        except (KeyError, TypeError, IndexError, AttributeError):

            title = None

        try:

            link = node["link"]

        except (KeyError, TypeError, IndexError, AttributeError):

            link = None

        if link != magneturl:

            torrenturl = link

        try:

            size = node["size"]

        except (KeyError, TypeError, IndexError, AttributeError):

            size = None

        try:

            comments = node["comments"]

        except (KeyError, TypeError, IndexError, AttributeError):

            comments = None

        try:

            details = node["guid"]

        except (KeyError, TypeError, IndexError, AttributeError):

            details = None

        try:

            pubdate = node["pubDate"]

        except (KeyError, TypeError, IndexError, AttributeError):

            pubdate = None

        movie_item_dict = {'title': title, 'torrenturl': torrenturl, 'size': size, 'details': details, 'comments': comments, 'pubdate': pubdate, 'seeders': seeders, 'peers': peers, 'magneturl': magneturl}
        movie_item_list.append(movie_item_dict)

    return movie_item_list
    # test = content[title, *magnet, *torrent, *nzb, *details, *seeders, *peers, *imdb_tt, size, date, *nfo, *id


# in logger_instance, kwargs for construct url (host, port, api_key, category, search, limit, user_agent)
# out return_code, seeders, leechers, size, date, tt number?,
def torznab(logger_instance, **kwargs):

    # download torznab result
    content = torznab_download(logger_instance, kwargs, "torznab")

    if content is not None:

        # send torznab result to function for processing
        result = torznab_result(logger_instance, content, "torznab")

        # send result back to calling module
        return result

