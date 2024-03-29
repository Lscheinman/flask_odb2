import time, string, random, socket, pyorient
import click
from datetime import datetime
from dateutil.parser import parse

SERVER_NAME = 'localhost:8000'
SECRET_KEY = '<YOUR SECRET KEY>'
SIGNATURE_EXPIRED = 'Signature expired'
BLACK_LISTED = 'Blacklisted token'
DB_ERROR = "Database error"
PROTECTED = ["password"]

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
#MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
#MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
MAIL_USERNAME = '<YOUR MAIL_USERNAME>'
MAIL_PASSWORD = '<YOUR MAIL_PASSWORD>'
COPILOT_URL = '<YOUR COPILOT_URL>'
COPILOT_AUTH = '<YOUR COPILOT_AUTH>'
COPILOT_POST = 'https://api.cai.tools.sap/build/v1/dialog'
COPILOT_DEV_TOKEN = '<YOUR COPILOT_DEV_TOKEN>'


# mail accounts
MAIL_DEFAULT_SENDER = 'from@example.com'

def get_datetime():
    """
    Utility function for returning a common standard datetime
    :return:
    """
    return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def clean_concat(content):
    """
    Utility function for returning cleaned strings into a normalized format for keys
    :param content:
    :return:
    """
    try:
        content = content.lower().translate(str.maketrans('', '', string.punctuation)).replace(" ", "")
    except Exception as e:
        click.echo('%s %s' % (get_datetime(), str(e)))
        content = None

    return content


def clean(content):
    """
    Utility function for returning cleaned strings into a normalized format for keys
    :param content:
    :return:
    """
    try:
        content = str(content.replace("'", "").replace('"', ''))
    except Exception as e:
        click.echo('%s %s' % (get_datetime(), str(e)))
        content = None

    return content

def change_if_date(date_string, fuzzy=False):
    """
    Return a date if the string is possibly in a date format within the list of date_formats.

    :param date_string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    date_formats = [
        '%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%A, %D %B %Y %H:%M:%S %z', '%A, %D %B %Y %H:%M:%S %Z',
        '%A, %D %B %y %h:%m:%s %z', '%a, %d %b %y %h:%m:%s %z', '%a, %d %b %y %h:%m:%s %Z','%a, %D %b %Y %H:%M:%S %Z',
        '%m/%d/%y, %I:%M %p', '%M/%d/%y, %I:%M %p', '%M/%D/%y, %I:%M %p', '%M/%D/%Y, %I:%M %p',
        '%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y', '%Y-%M-%D', '%Y/%M/%D', '%D-%M-%Y', '%D/%M/%Y',
        '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%d-%m-%Y %H:%M', '%d/%m/%Y %H:%M',
                    ]
    try:
        parse(date_string, fuzzy=fuzzy)
        try:
            for df in date_formats:
                try:
                    dt = datetime.strptime(date_string, df)
                    return dt
                except:
                    pass
        except Exception as e:
            click.echo('%s %s' % (get_datetime(), str(e)))
        return False

    except ValueError:
        return False

def randomString(stringLength=15):

    letters = string.ascii_lowercase + string.hexdigits + string.ascii_uppercase + '!@#$%^&*()_,.>,<'
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_host(user, pswd):
    click.echo('[OrientModel_init__%s] Pausing to allow ODB setup' % (get_datetime()))
    time.sleep(20)
    click.echo('[OrientModel_init__%s] Complete to allow ODB setup' % (get_datetime()))
    possible_hosts = socket.gethostbyname_ex(socket.gethostname())[-1]
    if len(possible_hosts) > 0:
        hostname = possible_hosts[0][:possible_hosts[0].rfind('.')]
        i = 2
        possible_hosts = ["localhost"]
        while i < 6:
            possible_hosts.append("%s.%d" % (hostname, i))
            i += 1
    for h in possible_hosts:

        client = pyorient.OrientDB("%s" % h, 2424)
        try:
            session_id = client.connect(user, pswd)
            click.echo('[OrientModel_init__%s] successfully connected to %s' % (get_datetime(), h))
            return {"client": client, "session_id": session_id}
        except Exception as e:
            click.echo('[OrientModel_init__%s] %s failed\n%s' % (get_datetime(), h, str(e)))

    return {"client": None, "session_id": None}
