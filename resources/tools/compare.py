# To the Artfarts:

# To use this script, you need to create a new directory anywhere, for example your desktop.
# Name it whatever, you want, for example "comparison".
# Next within this folder, create 2 new folders: "hd" and "master".
# Then paste hd-textures phase files into hd (so it'd be /hd/phase_X/.....)
# Then "$ git checkout master" (switch to master) and copy the master resources into master (so
# it'd be /master/phase_X/.....)
# Next, open a command prompt window (cmd), navigate to this directory (you can use something
# like this: "cd C:\Users\Harvir\Desktop\comparison\").
# Finally, run this command: "python compare.py".
# Then you will have all your stats printed. If you want more information on each file, for
# example seeing all the new and changed files, you can toggle them below (change True to False
# or vice-versa).

# Harv~

log_new = True
log_updated = True
log_unchanged = True

import os
import filecmp

jpeg_files = []

# Walk the hd directory to get a list of files in hd-textures.
for root, _, files in os.walk('hd'):
    for f in files:
        if f.endswith('.jpg'):
            # Since this is a jpeg file, we want to consider it.
            jpeg_files.append(os.path.join(root, f))

# Initiate and set our counters to 0.
new = 0
updated = 0
unchanged = 0

# Open output.txt for logging.
with open('output.txt', 'w+') as file:
    for image_hd in jpeg_files:
        image_master = image_hd.replace('hd', 'master')
        if not os.path.isfile(image_master):
            # This image doesn't exist in master. It must be new for hd-textures.
            if log_new:
                file.write("New file %s detected!\n" % image_hd)
            new += 1
        elif not filecmp.cmp(image_hd, image_master):
            # This image exists, but has been modified. This indicates that this
            # might possibly be a HD-ified texture!
            if log_updated:
                file.write("Updated file %s detected!\n" % image_hd)
            updated += 1
        else:
            # The version in master is the exact same as in hd-textures. This means
            # that the HD texture is already in master, or this texture hasn't been
            # HD-ified yet.
            if log_unchanged:
                file.write("Unchanged file %s detected!\n" % image_hd)
            unchanged += 1

print("A total of %d new files, %d updated files, and %d unchanged files." % (new, updated, unchanged))
percent_changed = ((updated+new)*1.0/len(jpeg_files))*100
print("%0.2f%% of all textures have been updated." % percent_changed)
