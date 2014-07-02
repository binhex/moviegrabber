unRAID Installation
-------------------
1. Download the MovieGrabber plugin from SourceForge to \\<ip address of server>\flash\config\plugins
2. Reboot unRAID or telnet into unRAID host and run installplg /boot/config/plugins/<moviegrabber plugin filename>
3. Go to Settings menu and look for MovieGrabber icon under Network Services
4. Click on the icon and configure the plugin, and exmple configuration is as follows:-

Sample Configuration
--------------------
Enable MovieGrabber = yes
Can be set to no to disable the plugin

Install Directory = /mnt/cache/.Apps/MovieGrabber 
Should be on a persistent drive such as cache drive, do NOT install to flash drive

IP = 192.168.1.10 
Should be the same as your unRAID server

Port = 9191
Can be any number from 1024 upwards, but must not already be in use by another plugin

Run as user = nobody
This can be set to a specific user if required but most standard installations will be most suited to setting this to nobody

Show storage memory usage = yes
Can be set to no to disable memory usage if required

Changelog
---------
ver 1.0.3
created 64bit version of moviegrabber plugin for unRAID 6.x series
fixed moviegrabber install to pull download url from sourceforge page
fixed moviegrabber plugin to pull download url from sourceforge page
fixed moviegrabber app version update to pull version from sourceforge page
fixed moviegrabber plugin version update to pull version from sourceforge page
fixed downgrade plugin button not centre aligned
forced utf-8 encoding in plugin to prevent issue with os.walk

ver 1.0.2
updated openssl package to openssl-0.9.8r-i486-3 (same version as sabnzbd_unplugged)
updated infozip package to infozip-6.0-i486-1 (same version as sabnzbd_unplugged)
updated sqlite package to sqlite-3.7.5-i486-1 (same version as sabnzbd_unplugged)

ver 1.0.1
fix missing infozip package

ver 1.0.0
initial release

Known Issues
------------
current moviegrabber version does not work, gets info from moviegrabber using --version flag
check $2 $3 $4 etc and remove if referencing datadir
missing warning about persistent data on reboot