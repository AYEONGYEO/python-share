# python-share
- python3 ver
## Contents
1. [SFTP connection](#sftp-connection) - Check the file list and find new file, Send email with new file list
2. [Email function](#email-function) - Send email, Read email inbox, Download email attachments 
* * *
### [Email function](https://github.com/YEONGYEO/python-share/blob/master/email/python_get_email_function.py)
   
1. Send the email   
```
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
```

2. Read email inbox   
- IMAP server connection   
```
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com", "993")
            self.imap.login(user, password)
        except:
            print("IMAP connection fail")

        self.imap.select('inbox')       # Select mail inbox
        type, data = self.imap.search(None, 'ALL')
        # type, data = self.imap.search(None, '(UNSEEN)')
        self.all_email = data[0].split()
```
- Order description
```
    reademail = ReadEmail()
    reademail.check_attachment_dir()
    email_message_list = reademail.get_message_object()
    # reademail.check_message_key(email_message_list)
    reademail.get_message_data(email_message_list)
    reademail.download_all_mail_attachments(email_message_list)
    reademail.end()
```
+ check_attachment_dir - If there is no directory named attachment, It will make it
+ get_message_object - Get all email convert to message object
+ check_message_key - Check keys of message object like sender, to, and date
+ download_all_attachments - download attachment from the email

* * *

### [SFTP connection](https://github.com/YEONGYEO/python-share/blob/master/sftp-connection/sftp-connection.py)
   
1. Check the file list
2. Find new file
3. Store file list as text file
4. Send email with new file list

- Basic setting   
Create the text file for compare between before and after upload new files (text file name : stored-file-list.txt )

- email send function   
Fill the empty spots - sender, pw(password), receiver  

```
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

            msg = MIMEText("Notification of new file upload - %s" % str(email_body))   # email body section
            msg['Subject'] = 'SFTP server check'        # email subject
            google.sendmail(self.sender, self.receiver, msg.as_string())
        except:
            print("error send email")
        finally:
            google.quit()
```

- SFTP connect
```
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=username, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except:
            print("error connecting sftp server")
```

- Check the file list in the path and count number
```
    def search_current_file(self):
        file_list = self.sftp.listdir(self.path)
        file_list = sorted(file_list)
        print("file number is total %d" % len(file_list))
        print("file list in sftp server {}".format(file_list))
        return file_list
```

- Open the file for compare
```
    def open_stored_file_list(self):
        try:
            with open('stored-file-list.txt', 'r') as f:
                origin = f.read()
                f.close()
                origin = origin.split(',')
            return origin
        except:
            print("doesn't exist 'stored-file-list.txt'")
```


