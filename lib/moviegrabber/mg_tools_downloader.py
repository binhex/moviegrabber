import requests
import backoff
import socket


@backoff.on_exception(backoff.expo, (socket.timeout, requests.exceptions.Timeout, requests.exceptions.HTTPError), max_tries=10)
def http_client(logger_instance, **kwargs):

    if kwargs is not None:

        if "url" in kwargs:

            url = kwargs['url']

        else:

            logger_instance.warning(u'No URL sent to function, exiting function...')
            return 1, None

        if "user_agent" in kwargs:

            user_agent = kwargs['user_agent']

        else:

            logger_instance.warning(u'No User Agent sent to function, exiting function...')
            return 1, None

        if "request_type" in kwargs:

            request_type = kwargs['request_type']

        else:

            logger_instance.warning(u'No request type (get/put/post) sent to function, exiting function...')
            return 1, None

        # optional stuff to include
        if "auth" in kwargs:

            auth = kwargs['auth']

        else:

            auth = None

        if "additional_header" in kwargs:

            additional_header = kwargs['additional_header']

        else:

            additional_header = None

        if "data_payload" in kwargs:

            data_payload = kwargs['data_payload']

        else:

            data_payload = None

        if "connect_timeout" in kwargs:

            connect_timeout = kwargs['connect_timeout']

        else:

            connect_timeout = 10.0

        if "read_timeout" in kwargs:

            read_timeout = kwargs['read_timeout']

        else:

            read_timeout = 30.0

    else:

        logger_instance.warning(u'No keyword args sent to function, exiting function...')
        return 1

    # use a session instance to customize how "requests" handles making http requests
    session = requests.Session()

    # set status_code and content to None in case nothing returned
    status_code = None
    content = None

    try:

        # define dict of common arguments for requests
        requests_data_dict = {'url': url, 'timeout': (connect_timeout, read_timeout), 'allow_redirects': True, 'verify': False}

        session.headers = {
            'Accept-encoding': 'gzip',
            'User-Agent': user_agent
        }

        if "additional_header" in kwargs:

            # append to headers dict with additional headers dict
            session.headers.update(additional_header)

        if "auth" in kwargs:

            session.auth = auth

        if request_type == "put":

            # add additional keyword arguments
            requests_data_dict.update({'data': data_payload})

        elif request_type == "post":

            # add additional keyword arguments
            requests_data_dict.update({'data': data_payload})

        # construct class.method from request_type
        request_method = getattr(session, request_type)

        # use keyword argument unpack to convert dict to keyword args
        response = request_method(**requests_data_dict)

        # get status code and content returned
        status_code = response.status_code
        content = response.content

        if status_code == 401:

            logger_instance.warning(u"The status code %s indicates unauthorised access for %s, error is %s" % (status_code, url, content))
            raise requests.exceptions.HTTPError

        elif status_code == 404:

            logger_instance.warning(u"The status code %s indicates the requested resource could not be found  for %s, error is %s" % (status_code, url, content))
            raise requests.exceptions.HTTPError

        elif status_code == 422:

            logger_instance.warning(u"The status code %s indicates a request was well-formed but was unable to be followed due to semantic errors for %s, error is %s" % (status_code, url, content))
            raise requests.exceptions.HTTPError

        elif not 200 <= status_code <= 299:

            logger_instance.warning(u"The status code %s indicates an unexpected error for %s, error is %s" % (status_code, url, content))
            raise requests.exceptions.HTTPError

    except requests.exceptions.ConnectTimeout as content:

        # connect timeout occurred
        logger_instance.warning(u"Connection timed for URL %s with error %s" % (url, content))
        return 1, status_code, content

    except requests.exceptions.ConnectionError as content:

        # connection error occurred
        logger_instance.warning(u"Connection error for URL %s with error %s" % (url, content))
        return 1, status_code, content

    except requests.exceptions.TooManyRedirects as content:

        # too many redirects, bad site or circular redirect
        logger_instance.warning(u"Too many retries for URL %s with error %s" % (url, content))
        return 1, status_code, content

    except requests.exceptions.HTTPError:

        # catch http exceptions thrown by requests
        return 1, status_code, content

    except requests.exceptions.RequestException as content:

        # catch any other exceptions thrown by requests
        logger_instance.warning(u"Caught other exceptions for URL %s with error %s" % (url, content))
        return 1, status_code, content

    else:

        if 200 <= status_code <= 299:
            logger_instance.info(u"The status code %s indicates a successful request for %s" % (status_code, url))
            return 0, status_code, content
