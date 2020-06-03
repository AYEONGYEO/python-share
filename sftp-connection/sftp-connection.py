# -*- coding:utf-8 -*-
# 2020.06.03, AYEONG YEO
# SFTP connect and check the new file in SFTP server
# Send email after checking new file

from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import paramiko
import smtplib
import time
import sys

class EmailSend():
    def __init__(self):
        self.sender = ""    # Fill here! - google account email address
        self.pw = ""        # Fill here! - sender password
        self.receiver = ""      # Fill here! - receiver email address

    def send(self, email_body):
        try:
            google = smtplib.SMTP('smtp.gmail.com', 587)    # If you want to use not google account, Change here
            google.starttls()
            google.login(self.sender, self.pw)

            msg = MIMEText("새로운 파일이 업로드되어 알림 - %s" % str(email_body))   # email body section
            msg['Subject'] = 'SFTP server check'        # email subject
            google.sendmail(self.sender, self.receiver, msg.as_string())
        except:
            print("error send email")
        finally:
            google.quit()

class SftpConnector:
    def __init__(self):
        host = ""   # Fill here! - SFTP host
        port = 2222     # Change port number
        username = ""      # Fill here! - SFTP user name
        password = ""       # Fill here! - SFTP user password
        self.path = ""   # Fill here! - Write the path where you want to check, and directory seperation = "/"

        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=username, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except:
            print("error connecting sftp server")

    def search_current_file(self):
        file_list = self.sftp.listdir(self.path)
        file_list = sorted(file_list)
        print("file number is total %d" % len(file_list))
        print("file list in sftp server {}".format(file_list))
        return file_list

    def open_stored_file_list(self):
        try:
            with open('stored-file-list.txt', 'r') as f:
                origin = f.read()
                f.close()
                origin = origin.split(',')
            return origin
        except:
            print("doesn't exist 'stored-file-list.txt'")

    def find_new(self, stored_file_list, current_file_list):
        try:
            new_file_list = sorted(list(set(current_file_list) - set(stored_file_list)))

            print("current file list {}".format(current_file_list))
            print("stored file list {}".format(stored_file_list))
            print("new file list {}".format(new_file_list))

            if not new_file_list:
                raise
            return new_file_list
        except:
            print("There aren't new uploaded files")
            sys.exit()

    def write_stored_file_list(self, new_file_list):
        with open('stored-file-list.txt', mode='at') as f:
            for file in new_file_list:
                f.write("%s,"%file)

    def end(self):
        self.sftp.close()
        self.transport.close()

if __name__=="__main__":
    start = time.time()
    sftp = SftpConnector()
    email = EmailSend()

    current_file_list = sftp.search_current_file()
    stored_file_list = sftp.open_stored_file_list()

    new_file_list = sftp.find_new(stored_file_list, current_file_list)

    sftp.write_stored_file_list(new_file_list)
    email.send(new_file_list)

    sftp.end()
    print("total time : %s seconds" % str(time.time() - start))
