MovieGrabber
============

Description
-----------
MovieGrabber is a fully automated way of downloading movie from usenet, it supports any nzb client that has a "watched" or "monitor" folder facility such as Sabnzbd+, Grabit and Newsbin. MovieGrabber works by checking imdb for matching criteria and if a match is found the nzb will be downloaded and stored in either a specified queued folder for user review or sent to the watched folder for processing and automatic downloading via your usenet binary client.

Features
--------
- imdb rating filter
- imdb votes filter
- imdb genres filter
- imdb year filter
- imdb actors filter
- imdb directors filter
- imdb characters filter
- imdb titles filter
- min/max post size
- format/resolution filter
- movie already downloaded
- replace existing movie
- nzb already in watched/nzb/completed folders
- email notification for queued/downloading
- post processing rules - create flexible rules to delete/move files based on genre, certificate, size etc
- torrent support for index site kickass torrents
- xbmc notification for queued/downloading
- xbmc library update on download complete

Windows Installation
--------------------
1. Download the latest win32 release from SourceForge
2. Unzip to install location
3. Change directory to install location
4. Start MovieGrabber by clicking on "MovieGrabber.exe"
5. open browser and go to http://<yourip>:9191

Linux Installation
------------------
1. Install Python 2.6x or later (3.x is NOT supported)
2. Download the latest src release from SourceForge
3. Unzip to install location
4. Change directory to install location
5. Start MovieGrabber by running "python ./MovieGrabber.py --daemon"
6. open browser and go to http://<yourip>:9191

Upgrading
---------
1. Shutdown MovieGrabber
2. Download the latest release from SourceForge
3. Unzip to the installation folder, overwritting all files
4. Start MovieGrabber

Changelog
---------
ver 2.2.0.b9
- added in pre-checks for valid host ip and valid config.ini entry
- added in sort order by imdbyear to queue/history
- bug in download cherrypy plugin - wrong queue specified for poison pill
- bug downloader not forcing shutting down correctly when downloads queued
- bug failed nzb/torrent downloads were not marked as failed in history/queue
- enhancement beter detection of match for post title regardless of seperator
- bug kat switched to gzipped torrents causing failed downloads, now correctly identify gzipped content
- bug new db being incorrectly marked for upgrade need to check pragma versions
- change logging to correct string formatting
- enhancement updated python modules
- removed imdb webscrape - out of date, using api only
- updated dognzb to new url for api
- change min and max api search terms from minsize and maxsize to min and max
- fixed up error code and description logging

ver 2.2.0.b8
- enhancement - check torrent AND usenet archive folders before marking movie for queue/download
- enhancement - store download url for movie from all index sites and use as fallback incase of download issue
- enhancement - now caching movies download and movies replaced for os.walk generator
- enhancement - can now specify number of posts to process (backlog searching)
- enhancement - improved number of posts returned by using server side filtering for "must exist" items, client side filtering done for may or must not exist
- bug - fixed issue with sessions being left open in methods, now closed using remove, this caused locking issues for other methods in the same thread

ver 2.2.0.b7
- added in webui icon to purge selected item
- bug decode issue for movies downloaded filter
- bug better detection of remote/local version checking

ver 2.2.0.b6
- bug defining a good rating of 0.1 causes error option values must be strings
- bug catch exception if kat rss feed not gzipped
- bug if watched folder didnt exist then queue release would error
- bug cannot enable xbmc notification with blank password
- bug movies with no rating or votes are NOT being flagged as bad
- bug refresh causes repost of form data, now fixed using PRG
- bug imdb website changes caused fallback webscrape to fail for actor and runtime
- bug kat path in add torrent site, not required
- bug force favorite title/bad title to match for movie title with year appended
- bug imdb favorites section had incorrect variable names
- bug destination folder was not case sensitive for post processing rules
- bug case insensitve sort order screwing up columns with integer values
- added search history/queue for movie titles
- added sort by dltype sort order gui post type asc, post type desc
- added sqlite logging to seperate log file
- added dognzb added to list of known working newznab hosts
- added bad release groups option
- change allow multiple xbmc hosts in config/notification
- change improved filename matching for movies exist/replace, now does partial filename match against imdb name
- change added in nzbid.org usenet site to list of known compatible newznab sites
- change speed improvements, multiple threads now running concurrently, also has de-dupe checking for postname via unique flag on db column
- change removed multiple sqlalchemy sessions, now using global session with thread safe option "scoped_session"
- change changed from good group (posted group name MUST exist in one of the defined lists) to a more intelligent preferred group list, which will force a download if a post group name does not exist in downloaded filename
- change server side to client side filtering for post name search criteria - newznab search api is crap
- change client side to server side filtering for post size using newznab api - increase posts returned
- change attr=imdb to extended=1 for newznab api, not all sites support specific extended attributes i.e. dognzb.cr
- change relaxed movies exists logic, now if movie is in movies to replace it will force a download even if the movie already exists

ver 2.2.0.b5
- upgade argparse and tidy up commandline arguments and help
- xbmc notification/library update changed to support frodo (xbmc 12)
- changed filters from for loops to set intersection and list comprehensions
- fixed kat url change
- switched from exact string match to ALL words for kat AND search string
- switched to sql alchemy for sqlite connection management
- add in ability to define multiple index sites for usenet and torrents
- add individual purge options for movies in queue with tickboxes and "purge selected" button in webui
- add size info to email notification
- add in actors, directors, writers, characters, and runtime to queue/history
- various webgui changes for queue/history
- moved post processing rules to config.ini

ver 2.2.0.b4
- added in initial spotweb support
- switched to SafeConfigParser to allow upgrade checks
- bug empty votes or size fields in config caused crash - now checking value is integer
- reworked imdb actors, directors, writers section
- bug post title ascii encode issue - remove string and coerced to unicode - look at forcing??
- removed metadata - old format for media browser
- added in addtional info logging for filters
- bug typo for sd collection scanner - using wrong dir cache
- bug issue casued by switching queuing on without restart caused missing function
- capture ssl errors when downloading rss/api feed
- rename filter functions to e.g. filter_os_watched, filter_imdb_good_ratings
- bug queue release button/checkbox not working due to nested forms
- bug poster image not showing in history/queue due to missing html encoding for filename - e.g. "movie - 1.jpg"
- bug ket.ph rss feed change, now updated to use new xml tag names
- html w3c validation cleanup on all templates
- switched from tables to divs
- html5 doc type now specified

Known Issues
------------
- ie cannot force download/release using either checkbox or button - ie does not support input "form="
- release group filter is doing partial matching, need to use match
- retry for urllib2 does not work correctly for download watched - urlerror works httperror does not, wrong number of arguments? 2/6
___
If you appreciate my work, then please consider buying me a beer  :D

[![PayPal donation](https://www.paypal.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=H8PWP3RLBDCBQ)
