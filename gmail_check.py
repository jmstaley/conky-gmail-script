import urllib2
import feedparser

from optparse import OptionParser

class Gmail:
    """ Provides interface for checking Google Mail
        For use with Conky
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'https://mail.google.com/mail/feed/atom'
        self.passwd_mgr = self._password_manager()
        self.doc = None

    def _password_manager(self):
        """ Build and return a password manager
        """
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, self.username, self.password)
        return password_mgr

    def _open_url(self):
        """ Using password manager open and read feed url over https
        """
        handler = urllib2.HTTPBasicAuthHandler(self.passwd_mgr)

        opener = urllib2.build_opener(handler)
        file = opener.open(self.url)
        return file.read()

    def _parse_atom(self):
        """ Open feed and parse atom using feedparser
        """
        file = self._open_url()
        self.doc = feedparser.parse(file)

    def get_mail_count(self):
        """ Return unread mail count
        """
        self._parse_atom()
        return len(self.doc['entries'])

    def get_mail_summary(self, number=3):
        """ Return summary of emails, containing from and subject
        """
        pass
#        entries = doc.entries
#        summaries = {}
#        if entries:
#            for x in range(3):
#                summaries[x] = {'from_address': entries[x]['author_detail']['email'],
#                    'from_name': entries[x]['author_detail']['name'],
#                    'title': entries[x]['title_detail']['value']}
#        return summaries


if __name__ == "__main__":
    usage = "usage: %prog [options] username password"
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--messages", action="store_true", dest="messages",
                      help="display message information", default=False)

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("Please supply both username and password")

    mail = Gmail(username=args[0], password=args[1])

    print "Unread: %s" % mail.get_mail_count()
