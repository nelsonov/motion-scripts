#!/usr/bin/python3

import datetime
import time
import glob
import os
from subprocess import call

sourcepath = "/var/lib/motion/cams/cam01/"
uploadpath = "/var/www/html/cams/cam01"
subdirs=('movies', 'snapshots', 'timelapse')
filetypes=('jpg', 'mp4', 'avi')
filenow = time.strftime("image-%Y-%m-%d_%H%M.jpg")
comment = time.strftime("%c")
sigal = "/opt/sigal/venv/bin/sigal"
sigalcfg = "/etc/sigal/sigal.conf.py"
rightnow=int(time.time())
client_id="rpi06"
startmins=28     # ie 12:28
endmins=32       # ie 12:32
keephours=60*60*24 # A full day
keeptime=60*60*5   # 5 Hours

def call_sigal(sigal, config, source, upload):
    #From CLI: sigal build -v source upload
    call([sigal, "build", "-c", config, source, upload])
    #call(rsync_cmd)

def cull_files (path, start, end, cutoff, rightnow):
    #Keep is range of minutes for which to keep files.
    #The idea is to leave only one file per hour.
    #This is done by creating a set of minutes for the
    #whole hour and then subtrating the minutes we want
    #to keep.
    #cutoff is a period of time (in seconds) in the
    #immediate past for which we keep all files
    counter=0
    cutofftime=rightnow - cutoff
    end+=1 #ranges are not inclusive of the higher end
    hour=set(range(0, 60))  # example, 12:00 - 12:59
    keep=set(range(start, end))
    excludemins=hour.difference(keep)
    for file in os.listdir(path):
        if file.endswith(filetypes):
            fullpath=os.path.join(path, file)
            mtime = os.path.getmtime(fullpath)
            timestamp=datetime.datetime.fromtimestamp(mtime)
            minute=timestamp.minute
            if mtime < cutofftime and minute in excludemins:
                os.remove(fullpath)
                print("Cull: %0i %s deleted" % (minute, fullpath))
                counter+=1
            else:
                print("Cull: %0i %s keeping" % (minute, fullpath))
    return counter

def rotate_files (sourcedir, dstdir, cutoff, rightnow):
    #If dstdir is empty, then delete files
    #cutoff specifies a cutoff afterwhich files should rotated or deleted

    #Test for and/or create directories

    #If file is older than cutoff
    ##If dstdir is empty, delete
    ##Else move to dstdir
    counter=0
    cutofftime=rightnow - cutoff
#    print ("rightnow %s, cutofftime %s"
#           %(time.ctime(rightnow), time.ctime(cutofftime)))
    for file in os.listdir(sourcedir):
#        print ("Rotate? %s" % file)
        if file.endswith(filetypes):
            fullpath=os.path.join(sourcedir, file)
            newpath=os.path.join(dstdir, file)
            mtime = os.path.getmtime(fullpath)
#            print ("mtime %s" % time.ctime(mtime))
            if mtime < cutofftime:
                if dstdir == "":
                    os.remove(fullpath)
                    print ("Rotate: %s deleted" % fullpath)
                    counter+=1
                else:
                    os.rename(fullpath, newpath)
                    print ("Rotate: %s rotated to\n %s" % (fullpath, newpath))
                    counter+=1
            else:
                print ("Rotate: %s keeping" % fullpath)
    return counter

def daysets(toppath, outerdirs, innerdirs, keephours):
    for outerdir in outerdirs:
        outer=toppath + outerdir + "/" + outerdir
        for i in range(0, len(innerdirs) -1):
            cutoff=(i+1) * keephours
#            print ("Yielding %s %s %d"
 #                  % (outer + innerdirs[i],
  #                    outer + innerdirs[i+1], cutoff))
            yield([outer + innerdirs[i], outer + innerdirs[i+1], cutoff])
        cutoff=len(innerdirs) * keephours
#        print ("Yielding %s %d" % (outer + innerdirs[-1], cutoff))
        yield([outer + innerdirs[-1], "", cutoff])

typedirs=["movies", "timelapse", "snapshots"]
culldirs=["snapshots"]
daydirs=["/", "_1day/", "_2day/"]


for typedir in culldirs:
    deleted=cull_files(sourcepath + typedir + "/" + typedir + daydirs[0],
                       startmins, endmins, keeptime, rightnow)

for dayset in daysets(sourcepath, typedirs, daydirs, keephours):
    rotated=rotate_files(dayset[0], dayset[1], dayset[2], rightnow)

call_sigal(sigal, sigalcfg, sourcepath, uploadpath)
