import os
import re
import imdbpie

# fixme need to regex for Blade Runner 2049 (2017) as it is assuming year is 2049

'''
input folder to rename
resursive flag 'True|False'
metadata site imdb, rottent tomators
seperator period or spaces
option to append date 'True|False'
'''


# in logger_instance, root_path, append_date, folder_title*, folder_year*
# out
def get_folder_title(logger_instance, kwargs):

    if kwargs is None:

        logger_instance.warning(u'No kwargs sent to function, exiting function...')
        return 1, None

    else:

        if "root_path" in kwargs:

            root_path = kwargs['root_path']

        else:

            logger_instance.warning(u'No root_path sent to function, exiting function...')
            return 1, None

        if "completed_folder" in kwargs:

            completed_folder = kwargs['completed_folder']

        else:

            completed_folder = ""
            logger_instance.info(u'No completed_folder sent to function, assuming process all folders...')

        folder_title_remove_year_to_end_regex = re.compile('\.?\s?\(?[0-9]{4}.*$')
        folder_year_regex = re.compile('(?<!^)[\s._\-()][\d]{4}([\s._\-()]|$)')
        folder_year_regex_clean = re.compile('[^\d]+')

        for folder, subfolder, filename in os.walk(root_path):

            for i in subfolder:

                if completed_folder:

                    if completed_folder != i:

                        logger_instance.warning(u'Completed folder %s does not match folder %s, skipping' % (completed_folder, i))
                        continue

                folder_path = os.path.join(root_path, i)
                folder_title = re.sub(folder_title_remove_year_to_end_regex, '', i)

                if folder_title is None:

                    logger_instance.warning(u'Folder title does not match regex for release, skipping')
                    continue

                folder_year = re.search(folder_year_regex, i)

                if folder_year is not None:

                    folder_year = folder_year.group(0)
                    folder_year = re.sub(folder_year_regex_clean, '', folder_year)

                else:

                    logger_instance.warning(u'Cannot determine folder year for folder name %s, skipping' % i)
                    continue

                kwargs.update({'folder_title': folder_title, 'folder_year': folder_year, 'folder_path': folder_path})
                get_metadata_site_title(logger_instance, kwargs)


# in logger_instance, folder_title, folder_year, metadata_site
# out metadata_site_title
def get_metadata_site_title(logger_instance, kwargs):

    if kwargs is None:

        logger_instance.warning(u'No kwargs sent to function, exiting function...')
        return 1, None

    else:

        if "metadata_site" in kwargs:
            metadata_site = kwargs['metadata_site']

        else:

            logger_instance.warning(u'No metadata_site sent to function, exiting function...')
            return 1, None

        if "folder_title" in kwargs:

            folder_title = kwargs['folder_title']

        else:

            logger_instance.warning(u'No folder_title sent to function, exiting function...')
            return 1, None

        if "folder_year" in kwargs:

            folder_year = kwargs['folder_year']

        else:

            logger_instance.warning(u'No folder_year sent to function, exiting function...')
            return 1, None

    logger_instance.info(u'Searching metadata site %s for folder title %s %s...' % (metadata_site, folder_title, folder_year))

    if metadata_site == 'imdb':

        imdb_instance = imdbpie.Imdb()
        metadata_site_title_search_list_dict = imdb_instance.search_for_title('%s %s' % (folder_title, folder_year))

    else:

        logger_instance.warning(u'Metadata site %s is not valid' % metadata_site)
        return 1

    if not metadata_site_title_search_list_dict:

        logger_instance.warning(u'Metadata site %s did not return any matches' % metadata_site)
        return 1

    strip_title_compare_regex = re.compile('[()\\//:;*?"<>|.,`~!%_\-\'\s]+')
    title_clean_regex = re.compile('[\\//:*?"<>|]+')

    def roman_to_dec(title):

        title = re.sub('\sI\s?$', '1', title)
        title = re.sub('\sII\s?$', '2', title)
        title = re.sub('\sIII\s?$', '3', title)
        title = re.sub('\sIV\s?$', '4', title)
        title = re.sub('\sV\s?$', '5', title)
        title = re.sub('\sVI\s?$', '6', title)
        title = re.sub('\sVII\s?$', '7', title)
        title = re.sub('\sVIII\s?$', '8', title)
        title = re.sub('\sIX\s?$', '9', title)
        title = re.sub('\sX\s?$', '10', title)

        return title

    folder_title_compare = roman_to_dec(folder_title)
    folder_title_compare = re.sub(strip_title_compare_regex, '', folder_title_compare)
    folder_title_compare = re.sub('and|And', '&', folder_title_compare)

    # loop over list of dicts with possible match
    for i in metadata_site_title_search_list_dict:

        metadata_site_year = i.get("year")

        if metadata_site_year == folder_year:

            metadata_site_title = i.get("title")

            if metadata_site_title:

                metadata_site_title_compare = roman_to_dec(metadata_site_title)
                metadata_site_title_compare = re.sub(strip_title_compare_regex, '', metadata_site_title_compare)
                metadata_site_title_compare = re.sub('and|And', '&', metadata_site_title_compare)
                metadata_site_title_clean = re.sub(title_clean_regex, '', metadata_site_title)

                if metadata_site_title_compare.lower() == folder_title_compare.lower():

                    metadata_site_year = i.get("year")
                    metadata_site_id = i.get("imdb_id")
                    kwargs.update({'metadata_site_title': metadata_site_title_clean, 'metadata_site_id': metadata_site_id, 'metadata_site_year': metadata_site_year})
                    logger_instance.info(u'Metadata site year %s and folder year %s match for title %s' % (metadata_site_year, folder_year, metadata_site_title))

                    # run function to rename folder
                    rename_folder(logger_instance, kwargs)
                    break

                else:

                    # append metadata title to list as possible match
                    logger_instance.info(u'Metadata site title %s and folder title %s do not match, skipping rename' % (metadata_site_title_compare, folder_title_compare))
            else:

                # unable to get title - bad data from metadata site?
                logger_instance.warning(u'Cannot determine metadata site title, skipping rename')
                return 1


# in logger_instance, metadata_site_title
# out return code
def rename_folder(logger_instance, kwargs):

    if kwargs is None:

        logger_instance.warning(u'No kwargs sent to function, exiting function...')
        return 1, None

    else:

        if "append_date" in kwargs:
            append_date = kwargs['append_date']

        else:

            logger_instance.warning(u'No append_date sent to function, exiting function...')
            return 1, None

        if "separator" in kwargs:

            separator = kwargs['separator']

        else:

            logger_instance.info(u'No separator sent to function, assuming spaces')
            separator = " "

        if "root_path" in kwargs:

            root_path = kwargs['root_path']

        else:

            logger_instance.warning(u'No root_path sent to function, exiting function...')
            return 1, None

        if "folder_path" in kwargs:

            folder_path = kwargs['folder_path']

        else:

            logger_instance.warning(u'No folder_path sent to function, exiting function...')
            return 1, None

        if "metadata_site_year" in kwargs:

            metadata_site_year = kwargs['metadata_site_year']

        else:

            logger_instance.warning(u'No metadata_site_year sent to function, exiting function...')
            return 1, None

        if "metadata_site_title" in kwargs:

            metadata_site_title = kwargs['metadata_site_title']

        else:

            logger_instance.warning(u'No metadata_site_title sent to function, exiting function...')
            return 1, None

    if separator == "spaces":

        separator = " "

    elif separator == "hyphens":

        separator = "-"

    elif separator == "underscores":

        separator = "_"

    else:

        separator = " "

    metadata_site_title_separator = re.sub('\s+', separator, metadata_site_title)

    if os.path.isdir(folder_path):

        if append_date:

            metadata_site_title = "%s%s(%s)" % (metadata_site_title_separator, separator, metadata_site_year)

        metadata_path = os.path.join(root_path, metadata_site_title)

        if folder_path != metadata_path:

            try:

                os.rename(folder_path, metadata_path)
                logger_instance.info(u'Renamed folder %s to %s' % (folder_path, metadata_path))
                return 0

            except WindowsError:

                logger_instance.warning(u'Unable to rename folder %s to %s' % (folder_path, metadata_path))
                return 1

        else:

            logger_instance.info(u'Folder path %s and metadata path %s match, skipping rename' % (folder_path, metadata_path))

    else:

        logger_instance.warning(u'Folder path %s is not a directory, skipping rename' % folder_path)


# in logger_instance, kwargs for (root_path, recursive, metadata_site, separator, append_date)
# out return_code
def post_rename(logger_instance, **kwargs):

    get_folder_title(logger_instance, kwargs)
