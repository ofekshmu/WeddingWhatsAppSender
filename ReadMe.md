# Wedding Whatsapp sender

## Intro

This small app helped me distribute weddings invitations, approvals and more to our 400 wedding guest over the course of our wedding.

## Inputs

The script is based on a contact excel created by us, with a set number and type of columns. The app handels this excel file along with other files derived from it in order to send proper messages to our guests depending on various cases

## Features

0. The first Feature was a broad cast message to all guest in the excel,
message is prederemined and sent to the guests which are marked with a binary "1" in the excel file. The message is changed according to number of guests to match the correct grammer and sent to the specified number in the excel.

- Mind that that Py What kit that is used for sending the messages uses web interface and does not feedback, meaning that unless you stare at the screen, and wait for each message, you cannot know if a problem accured in the sending process.
a possible problem could be - an invalid number.

1. we were provided with 10comm app that helps us get approvals from our guests, this app also receives an excel file that needs to be prepared in according - the options creates an excel file with name and phone number only

2. Approval excel is an excel file derived from the 10comm app output excel.
The provided 10comm excel is read and processed for a better (in terms of data)
excel file.

3. A script for sending an identical broadcast message to approved guests.

4. Same as option 3, for the iPlan app.