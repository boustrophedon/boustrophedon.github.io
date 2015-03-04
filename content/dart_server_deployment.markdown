Title: How I'm deploying Dart server code on DigitalOcean
Category: System Administration
Tags: dart, deployment, systemd, fedora, websockets

So I finally started to work on my multiplayer breakout clone in dart that I've been meaning to do forever. It's moderately functional now. This post is how I am deploying the server code on digitalocean. It's written mostly for someone who has maybe used a desktop linux environment and isn't completely lost on the command line, but who maybe hasn't set up a server before. Here is the short version:

- create a new fedora droplet
	- ssh keys
- yum update (optional)
- create new user
- copy ssh keys to new user's directory
	- make sure permissions are correct
- add user to wheel
- remove root login from sshd\_config
- add dartapps user
	- useradd -r -s /sbin/nologin dartapps
- download and unzip dart-sdk to /opt/
- symlink /opt/dart-sdk/bin/{dart,dart2js,pub} to /usr/bin/{dart,dart2js,pub}
- cd to /usr/local/bin and git clone the repo
- This is what I did originally to get deps working:
	- if not running as root, switch to root
	- run `PUB_CACHE=/usr/local/bin/dart-breakout/pub-cache pub get`
- You can also choose to do the previous step and the following on the server, or locally and scp the file:
	- after getting the dependencies with pub get, create a build/ directory and run:
		`dart2js --categories=Server --output-type=dart bin/server.dart -o build/server.dart`
- create systemd unit file
	- if building with dart2js, set the exec file accordingly
- enable unit file
- start unit file
- yay

First, create a digitalocean droplet running Fedora (21 is the latest they have as of 3/15). You should probably choose to have your ssh key included.

The next step is optional: Do a `yum update`. This, of course, updates all of your packages and may take a little while. It will also most likely give you some security fixes that you probably want.

Next we're going to create a new user so that you're not running as root all the time, because that is a bad idea. run `useradd NEWUSERNAME` with whatever you want, and follow the directions. Add this user to wheel with `usermod -a -G wheel NEWUSERNAME`, which will give it access to sudo. You can modify your /etc/sudoers (with `visudo` !) so that you don't have to type your password for sudo, or not, depending on your preference. Finally, if you added ssh keys on droplet creation, copy them from .ssh/authorized\_keys to /home/NEWUSERNAME/.ssh/authorized\_keys and make sure to chown and chgrp your new /home/NEWUSERNAME/.ssh/ directory so it's owned by your new user.

Since digitalocean provides console access via its web dashboard, there's really no reason to allow root logins from ssh, so now that we have a new user that we can log in to (check to make sure you can log in first; you may have to reboot the server) let's fix that. Edit /etc/ssh/sshd\_config as root and uncomment the line `PermitRootLogin yes`, and change yes to no. Try sshing to the droplet as root. If it still works, you need to restart the ssh server or at least reload the configs.

Now we're going to create a user to run our dart server. We want it to have very few privileges on the system in case someone takes advantage of a vulnerability in the server and is able to execute arbitrary code, and it is also convenient for other purposes, like bandwidth-limiting, disk space quotas, other monitoring stuff that I'm not going to cover. I'm going to call this user 'dartapps' but you can call it whatever. To create it, run `useradd -r -s /sbin/nologin dartapps`. The -r option makes the user a system user, without a home directory, and -s /sbin/nologin means that it doesn't have a login shell; you cannot login as this user even if you gave it a password.

It is now time to install the dart sdk. Open https://www.dartlang.org/tools/download.html#other and copy the 64-bit linux download url. Download it into /opt and unzip it (you will probably need to `yum install unzip`). In order to make things convenient, you can symlink any or all of the files in /opt/dart-sdk/bin/ to /usr/bin/ by doing `ln -s /opt/dart-sdk/bin/dart /usr/bin/dart`, and similarly for the others. At the very least you will want to do this for the dart and pub commands. You may also need to `chmod o+rx /opt/dart-sdk/bin/dart` if you cannot run e.g. `dart --help` from your NEWUSERNAME user.

At this point we finally get to download our own code. Either scp your server code, git clone it, or whatever, into some directory. I chose /usr/local/bin/dart-breakout/ for my breakout code, but it could just have easily gone into /srv/ or something. /srv may in fact be a better choice.

There is an optional, somewhat unsupported step here: Instead of copying all your code over, you may, on your local development machine, create a build/bin directory in your pub package file structure. Then, run the following command, assuming your server dart code is in bin/server.dart: `dart2js --categories=Server --output-type=dart bin/server.dart -o build/bin/server.dart`. This runs "dart2dart" on your code and puts it all in a single file, but instead of outputting js it outputs dart code. You may also do this on the server after getting the dependencies as explained in the next paragraph.

If you did not follow the above optional step, this is what I originally did: Normally, pub downloads your packages into ~/.pub-cache. However, our dartapps user does not have a home directory. If we try to run `pub get` as root, pub will install our dependencies into /root/.pub-cache, which is of course unreadable by the dartapps user. We can fix this by either creating a global pub-cache inside, say, /usr/local/include/ or /usr/local/lib/, but I chose the option of creating it inside my server's code directory, so /usr/local/bin/dart-breakout/pub-cache. This is already a bit messy and a mild abuse of /usr/local/bin, and the better option is to compile all your dart code to a single file as in the above step.

In order to create this extra pub cache directory, we need to (as root), run `PUB_CACHE=/usr/local/bin/dart-breakout/pub-cache pub get`. Setting the PUB\_CACHE variable tells pub where to put the cache, and sets up the symlinks to point at that local cache for our application. Of course, be sure to substitute dart-breakout for your own name. You should test that the dependencies are installed and permissions are correct by running the server as a non-root user.

Lastly, we get monitoring, logging, and restart-on-crash for free by creating a simple systemd unit file that runs our server as the dartapps user. Drop this file into /etc/systemd/system/dart-breakout.service, replacing dart-breakout in both the filename and inside the file as needed:

	[Service]
	ExecStart=/usr/bin/dart /usr/local/bin/dart-breakout/bin/server.dart
	Restart=always
	StandardOutput=syslog
	StandardError=syslog
	SyslogIdentifier=dart-breakout
	User=dartapps
	Group=dartapps
	
	[Install]
	WantedBy=multi-user.target

If you followed the optional "dart2dart" step, replace the project/bin/server.dart file with the compiled file, which you would probably install to /usr/local/bin/ directly.

And now we're done! Run (as root) `systemctl enable dart-breakout` to enable the service to run on startup, and `systemctl start dart-breakout` to start the server now. You can use `journalctl -u dart-breakout` to view the output of your program.
