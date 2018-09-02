# Mirrorcast - Open Source Alternative to Chromecast

The idea is to replicate what chromecast can do in regards to screen mirroring and streaming media to a remote display. 
Google chromes screen mirroring feature works well when used with a receiver such as chromecast but this is a proprietary solution and audio does not work for desktop mirroring on some operating systems.

This application is ideal for wireless projection, no more cables, just send your desktop or media over the network to a receiver

At the moment, there is only a client for Debian/Ubuntu Operating systems. There is a server/receiver application for raspberry pi

Mirrorcast aims to be a low latency screen mirroring solution with high quality video and audio at 25-30fps, the later is why we will not use something like VNC.

Mirrorcast uses up about the same amount of system resources as google chromes cast feature. The delay is less than 1 second on most networks.

To acheive this we will use existing FOSS software such as ffmpeg, ffplay, VLC player and omxplayer

<p>Video Demo <a href="https://www.youtube.com/embed/23fGNmvI6zE">https://www.youtube.com/embed/23fGNmvI6zE</a> </p>

<h2>TO DO:</h2>

<b>DEBIAN/UBUNTU APPLET</b>

<p>The debian/ubuntu app is working but could do with improvements</p>

<ul><li>Automate audio settings(This is partially done, you might need to modify some code to automate audio settings for some computers)</li>
<li>Add option mirror selected application (Using Xlib and composite(redirect and pixmap) so that applications will still mirror if covered by another window, resized or minimised), this might require a full C+ conversion, unfortunately I lack practice in C and C+</li>
<li>Tidy up code (Find simplier and more pythonic solutions where possible)</li></ul>

<b>Other (If you want to help out with creating a client for the following then that would be great)</b>
<ul><li>Create Windows client application</li>
<li>Create MacOs client application</li>
<li>Create Android client application</li>
<li>Other bug fixes; additionial features and improvements</li></ul>


<h2>How to use</h2>

Currently this is a rough prototype that I have only tested on computers running Ubuntu 16.04 and Lubuntu and a raspberry pi as the receiver. The applet will add a option to start mirroring the selected display to the selected receiver. It has been deployed at a High School where it is used so the teachers can use the projectors without cables.

To install the mirrorcast client on debian/ubuntu
First download and install the latest mirrorcast deb file from releases
```sh
sudo dpkg -i mirrorcast_version_number.deb
```
If you are missing dependencies install them with:
```sh 
sudo apt-get update && sudo apt-get -f install
```
Then add/edit the hostnames or ip addresses of your receivers in /opt/mirrorcast/receivers (if the receiver is widescreen then put '16:9' as the aspect)
If you want to be able to play DVD's then you need to edit /etc/nbd-server/config and add your dvd drive to it.
Here is my config file
```
[generic]
        #user = root
        #group = cdrom
        includedir = /etc/nbd-server/conf.d
        allowlist = true
[dvd]
        exportname = /dev/sr0
        readonly = true
```
Then you will need to enable and restart the nbd server
```sh
sudo service nbd-server restart
sudo systemctl enable nbd-server
```

<h2>Setting up the raspberry pi server/receiver.</h2>
First install omxplayer, youtube-dl(from github) and python-omxplayer-wrapper for python3.
Then download mirrorcast_server_pi.py and omx.py from the server folder or just clone the whole repo.
Install python-mpv 
```sh 
npm3 python-mpv
```
Add the following to /etc/rc.local
```
python3 /path/to/mirrorcast_server_pi.py
modprobe nbd
```
If you want to be able to play DVD's then you will need the mpeg2 license from the pi store and mpv compiled with mmal and libmpv support(I will share pre-compiled ones at a later stage)
Restart the pi



By default the mirrorcast server uses udp port 8090 and tcp port 8092. If the client wants to stream files, then TCP port 8090 needs to be open on the client side. For DVD's nbd port needs to be open on client side too.

To start mirroring your desktop, start the mirrorcast application, it will add an applet to your toolbar, first select the display you want to mirror(if you have more than one), then select your receiver, then click "start mirroring"

<p>NOTE: This is a work in progress, the code is rushed, messy and not at all elegant at this stage. </p>
