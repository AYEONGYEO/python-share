# -*- coding:utf-8 -*-
# Create by A YEONG YEO
# python3
# Send email, Read email, Download All attachments

import smtplib
import imaplib
import email
import time
from email.mime.text import MIMEText
from email.header import decode_header
import chardet
import os

# Receiver email address
sendto = ''     # Fill here

# account       # Fill the account information
user = ""
password = ""

# SMTP server - Send email
def send_mail(user, password, sendto, msg_body):
    smtpsrv = "smtp.gmail.com"                      # dispatch mail server address
    smtpserver = smtplib.SMTP(smtpsrv, 587)         # dispath mail server port number
    try:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(user, password)
    except:
        print("SMTP server connection fail")

    msg = MIMEText(msg_body)
    msg['From'] = user
    msg['To'] = sendto
    msg['Subject'] = "Module Testing email Subject"

    smtpserver.sendmail(user, sendto, msg.as_string())
    print('done!')
    smtpserver.close()

class ReadEmail():
    def __init__(self):
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com", "993")
            self.imap.login(user, password)
        except:
            print("IMAP connection fail")

        self.imap.select('inbox')       # Select mail inbox
        type, data = self.imap.search(None, 'ALL')
        # type, data = self.imap.search(None, '(UNSEEN)')
        self.all_email = data[0].split()

    def get_message_object(self):
        email_message_list = []      # list include email.message.Message object, store all mail
        for mail in self.all_email:
            # get email to fetch order (RFC822 Protocal, email standard)
            result, data = self.imap.fetch(mail, '(RFC822)')
            raw_email = data[0][1]      # raw message (byte type)
            email_message_list.append(email.message_from_bytes(raw_email))     # message processing(email module) - convert byte type to message type

        return email_message_list

    def check_message_key(self, email_message_list):
        keys = email_message_list[0].keys()
        print(keys)

    def get_message_data(self, email_messagge_list):
        for email_message in email_messagge_list:
            from_name, from_addr = self.get_message_from(email_message['From'])
            subject = self.get_message_subject(email_message['Subject'])
            attachment = self.check_attachment(email_message)
            content = self.get_message_content(email_message)

            print("FROM : ", from_name)
            print("FROM ADDRESS : ", from_addr)
            print("SUBJECT : ", subject)
            print("ATTACHMENT : ", attachment)
            print("[CONTENT]")
            print("="*80)
            print(content)
            print("="*80)
            # print("SENDER :", email_message['Sender'])
            # print("TO :", email_message['To'])
            # print("DATE :", email_message['Date'])

    # Track specific senders - need to edit the code
    def find_email_from_bc(self, email_message_list):
        bc_addr = ""
        for email_message in email_message_list:
            from_name, from_addr = self.get_message_from(email_message['From'])
            attachment = self.check_attachment(email_message)
            if from_addr == bc_addr and not attachment:
                self.download_attachments(email_message)

    def get_message_from(self, data):
        mail_from = decode_header(data)
        # If the email have both the sender's name and the sender's email address
        if len(mail_from) == 2:
            from_name, encode = mail_from[0]  # Encoding information in sender's name value
            from_addr = mail_from[1][0]
            from_name = str(from_name, encode)
            from_addr = str(from_addr, encode).replace("<", "").replace(">", "")
        # If the email have only the sender's email address
        else:
            from_name = ""
            from_addr = mail_from[0][0]

        return from_name, from_addr

    def get_message_subject(self, data):
        return (self.find_encoding_info(data))

    def get_message_content(self, email_message):
        # The body of the mail is divided into several parts and stored
        # The contents of all original luck must be repeatedly output using the get_payload() function
        while email_message.is_multipart():
            email_message = email_message.get_payload(0)
        content_data = email_message.get_payload(decode=True)

        # email content encoding type-utf-8, EUC-KR
        content_encode = chardet.detect(content_data)['encoding']
        if content_encode == "utf-8":
            content = content_data.decode()
        elif content_encode == "EUC-KR":
            content = content_data.decode(content_encode)
        else:
            print("Error different types of encoding")

        return content

    def check_attachment_dir(self):
        if 'attachments' not in os.listdir('.'):
            os.mkdir('attachments')

    def check_attachment(self, email_message):
        check = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            check.append(self.find_encoding_info(part.get_filename()))

        return ", ".join(check)

    def download_all_mail_attachments(self, email_message_list):
        for email_message in email_message_list:
            self.download_attachments(email_message)

    def download_attachments(self, email_message):
        file_name = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            file_name.append(self.find_encoding_info(part.get_filename()))

            for one in file_name:
                if bool(one):
                    file_path = os.path.join(os.getcwd(), 'attachments', one)

                    if not os.path.isfile(file_path):
                        with open(file_path, 'wb') as f:
                            f.write(part.get_payload(decode=True))

    def find_encoding_info(self,txt):
        info = email.header.decode_header(txt)
        s, encoding = info[0]
        if not encoding:
            return s
        return str(s, encoding)

    def end(self):
        self.imap.close()
        self.imap.logout()

def main():
    start = time.time()
    # send email function
    # send_mail(user, password, sendto, "Hello This is test email")

    reademail = ReadEmail()
    reademail.check_attachment_dir()
    email_message_list = reademail.get_message_object()
    reademail.check_message_key(email_message_list)
    reademail.get_message_data(email_message_list)
    reademail.download_all_mail_attachments(email_message_list)
    reademail.end()
    
    print("total time : %s seconds" % str(time.time() - start))

if __name__ == '__main__':
    main()
