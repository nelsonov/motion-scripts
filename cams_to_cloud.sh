#!/bin/bash

#-r recursive
#-c checksum compare.  Takes longer but does not depend on
#   timestamps
#-z Compress files in transit
#-v Verbose output
#-F lookes for .rsync-filter which will be used as a filter
#--ignore-times ignores timestamps
#--delete-after Deletes files on the receiving end that do not exist
#               on the sender.  Deletions are performed last.
#               Deleting last ensures that the receiving side gets
#               all the same exclude rules as the sending side
#               before it tries to delete anything
#lnelson@ Make sure I use the right user.  Windows capitalizes
#         the first letter of usernames (eg "Lnelson").

REMOTE=lnelson@manager01.nelnet.org
#REMOTE=manager01.us-west1-b.hosting-159308

rsync -rczvF --ignore-times --delete-after /media/cams/upload/ ${REMOTE}:/media/ui/cam/
