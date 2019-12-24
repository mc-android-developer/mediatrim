# mediatrim
Clean up your image and media files: unify file naming, remove exif data 

## how to use
Install git
<pre>
sudo apt install git
</pre>
you also need python2.7 to be installed and operational

Clone repo
<pre>
git clone git@github.com:mcmindcoder/mediatrim.git
</pre>

When mediatrim executed it process media files in the current folder and all subfolders of current folder.
Lets say you have your image files located in **~/images** and you cloned mediatrim to **~/mediatrim**

Then run 
<pre>
cd ~/images
~/mediatrim/mediatrim.py
</pre>

You also can run specific modules to do individual tasks. 
E.g. to remove only exif data on your mediafiles run
<pre>
cd ~/images
~/mediatrim/mediatrim/exif.py
</pre>

Or if you want only remove media file duplicates run
<pre>
cd ~/images
~/mediatrim/mediatrim/remove_duplicates.py
</pre>