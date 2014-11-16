from email.mime.text import MIMEText
from email.parser import Parser


class Mail(Parser):
    """docstring for MailProcess"""
    def __init__(self, mailstrg, config):
        super(Mail, self).__init__()
        self.mailstrg = mailstrg
        self.config = config

        self.parse_mail(mailstrg=mailstrg)

    def parse_mail(self, **kwargs):
        if kwargs.mailstrg is not None:
            self.mailstrg = kwargs.mailstrg

        self.msg = MIMEText(self.mailstrg)
