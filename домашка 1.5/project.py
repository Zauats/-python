import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailWork():

    def __init__(self, login, password, recipients, message):
        self.DEFAULT_SMTP = "smtp.gmail.com"
        self.DEFAULT_IMAP = "imap.gmail.com"
        self.login = login
        self.password = password
        self.subject = 'Subject'
        self.recipients = recipients
        self.message = message

    def send_message(self):

        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))

        ms = smtplib.SMTP(self.DEFAULT_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()

    def recieve_message(self, header = None):
        mail = imaplib.IMAP4_SSL(self.DEFAULT_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")

        criterion = '(HEADER Subject "%s")' % self.header \
            if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)

        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()

        return email_message


if __name__ == '__main__':
    email_1 = EmailWork('cfif6734@gmail.com', 'neScaju',
                        ['cfif6735@gmail.com', 'cfif6736@gmail.com'],
                        'Привет, пойдем гулять?')
    email_1.send_message()
    email_1.recieve()
