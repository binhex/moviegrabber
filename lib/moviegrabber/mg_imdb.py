import imdbpie
from itertools import islice

# TODO set output to unicode,


# in, moviegrabber logger instance, imdb tt id
# out, list of dicts with imdb metadata
def imdb_json_api(mg_log, imdb_tt_id):

    # create imdb empty list, used to append dicts
    imdb_output_list = []

    # create imdbpie object
    imdb_instance = imdbpie.Imdb()

    # grab metadata from IMDb JSON for main title
    try:
        get_title = imdb_instance.get_title(imdb_tt_id)
    except imdbpie.exceptions.ImdbAPIError:
        mg_log.warning(u"failed to download json from imdb api")
        return 1

    try:
        imdb_poster_url = get_title['base']['image']['url']
        imdb_poster_url_dict = {'imdb_poster_url': imdb_poster_url}
        imdb_output_list.append(imdb_poster_url_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb poster url")

    try:
        imdb_title = get_title['base']['title']
        imdb_title_dict = {'imdb_title': imdb_title}
        imdb_output_list.append(imdb_title_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb title")

    try:
        imdb_year = get_title['base']['year']
        imdb_year_dict = {'imdb_year': imdb_year}
        imdb_output_list.append(imdb_year_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb year")

    try:
        imdb_runtime = get_title['base']['runningTimeInMinutes']
        imdb_runtime_dict = {'imdb_runtime': imdb_runtime}
        imdb_output_list.append(imdb_runtime_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb runtime")

    # Grab metadata from IMDb JSON for plot
    try:
        get_title_plot = imdb_instance.get_title_plot(imdb_tt_id)
    except imdbpie.exceptions.ImdbAPIError:
        mg_log.warning(u"failed to download json for title plot")
        return 1

    try:
        imdb_plot = get_title_plot['outline']['text']
        imdb_plot_dict = {'imdb_plot': imdb_plot}
        imdb_output_list.append(imdb_plot_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb plot")

    # Grab metadata from IMDb JSON for genres
    try:
        get_title_genres = imdb_instance.get_title_genres(imdb_tt_id)
    except imdbpie.exceptions.ImdbAPIError:
        mg_log.warning(u"failed to download json for imdb title genres")
        return 1

    try:
        imdb_genres = get_title_genres['genres']
        imdb_genres_list = []

        for i in imdb_genres:
            imdb_genres_list.append(i)

        imdb_genres_dict = {'imdb_genres': imdb_genres_list}
        imdb_output_list.append(imdb_genres_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb genres")

    # Grab metadata from IMDb JSON for ratings
    try:
        get_title_ratings = imdb_instance.get_title_ratings(imdb_tt_id)
    except imdbpie.exceptions.ImdbAPIError:
        mg_log.warning(u"failed to download json for imdb title ratings")
        return 1

    try:
        imdb_rating = get_title_ratings['rating']
        imdb_rating_dict = {'imdb_rating': imdb_rating}
        imdb_output_list.append(imdb_rating_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb ratings")

    try:
        imdb_rating_count = get_title_ratings['ratingCount']
        imdb_rating_count_dict = {'imdb_rating_count': imdb_rating_count}
        imdb_output_list.append(imdb_rating_count_dict)
    except KeyError:
        mg_log.warning(u"failed to download json for imdb ratings count")

    # Grab metadata from IMDb JSON for writers, directors, characters and actors
    try:
        get_title_credits = imdb_instance.get_title_credits(imdb_tt_id)
    except imdbpie.exceptions.ImdbAPIError:
        mg_log.warning(u"failed to download json for imdb title credits")
        return 1

    try:
        imdb_writers = get_title_credits['credits']['writer']
        imdb_writers_list = []

        for i in imdb_writers:
            imdb_writers_list.append(i['name'])

        imdb_writers_dict = {'imdb_writers': imdb_writers_list}
        imdb_output_list.append(imdb_writers_dict)

    except KeyError:
        mg_log.warning(u"failed to download json for imdb writers")

    try:

        imdb_directors = get_title_credits['credits']['director']
        imdb_directors_list = []

        for i in imdb_directors:
            imdb_directors_list.append(i['name'])

        imdb_directors_dict = {'imdb_directors': imdb_directors_list}
        imdb_output_list.append(imdb_directors_dict)

    except KeyError:
        mg_log.warning(u"failed to download json for imdb directors")

    try:
        imdb_cast = get_title_credits['credits']['cast']
        imdb_actors_list = []

        limit = 10

        for i in islice(imdb_cast, limit):
            imdb_actors_list.append(i['name'])

        imdb_actors_dict = {'imdb_actors': imdb_actors_list}
        imdb_output_list.append(imdb_actors_dict)

        imdb_character_list = []

        for i in islice(imdb_cast, limit):
            imdb_character_list.append(i['characters'][0])

        imdb_character_dict = {'imdb_characters': imdb_character_list}
        imdb_output_list.append(imdb_character_dict)

    except KeyError:
        mg_log.warning(u"failed to download json for imdb characters")

    return imdb_output_list
