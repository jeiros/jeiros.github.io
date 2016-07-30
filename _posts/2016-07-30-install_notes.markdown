---
layout: post
title:  "Installing AmberTools-Chimera-VMD on a Mac"
date:   2016-07-30 19:40:00 -0400
tags: how-to
---

I'm just writing this as how-to reference for installing useful software for MD research.
I already wrote most of this a long time ago but is somewhere hidden in my GitHub, so I'm putting it here for easier access.
Hopefully it's also useful for someone else although this is all pretty much really basic and I just write it down because 
I easily forget things.



## Installing AmberTools
Follow Jason Swail's [guide](http://jswails.wikidot.com/mac-os-x). Easy right?

In essence, these are the necessary things for AmberTools to work on a Mac:

1. Instal Xcode

2. Enable command-line tools

3. Download macports

4. Use macports to install the compilers for AmberTools to work


The gcc version 4.8 (known bug in [here](https://trac.macports.org/ticket/48471) failed for me so I installed the 4.9 version. 
The commands were:
```
sudo port install gcc49
sudo port install mpich-gcc49
sudo port select --set gcc mp-gcc49
sudo port select --set mpi mpich-gcc49-fortran
```
Once you complete all of the above steps without errors, you can actually start the installation of AmberTools:

1. Download them from [here](http://ambermd.org/AmberTools15-get.html)

2. Follow the instructions in page 23 of the [manual](http://ambermd.org/doc12/Amber15.pdf).

 * Everything worked for me using the most simple installation (`./configure gnu`)

If you do `make test` in your `$AMBERHOME` directory and everything is OK, you should see the following (after a lot of output):

```
All the tests PASSED
    1382 file comparisons passed
    0 file comparisons failed
    0 tests experienced errors
    Test log file saved as /usr/local/amber15/logs/test_at_serial/2015-10-28_15-26-42.log
No test diffs to save!
```

## Installing VMD
[Here](http://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD) are all of the downloadables.

I chose the latest version (1.9.2) and the MacOS X OpenGL (32-bit Intel x86) link.

A `.dmg` file is downloaded. Open it and then drag the VMD icon to the Applications folder. Done!

It won't let you just open it yet: Apple blocks applications from non-verified distributors (a.k.a non-Apple)
so you have to go to *System Preferences > Security & Privacy* and click on the *General* tab. There, click on the
lower-left lock icon, and then select the *Anywhere* option under the *Allow apps downloaded from:* section. 
Now you can use vmd.  

### How to use vmd from the command line
Using VMD from the command line is very convenient as you can directly load the topology and trajectories files, or several PDBs
very quickly. If you open VMD manually from the Dock it points every time to your home directory and you loose a lot of time manually
navigating to wherever the files you want to visualize are. 


1. Remove the space from the name of the Application (i.e. VMD1.9.2). This is best done from the Finder (spaces in the command line are a pain to work with).

2. Add this to your `~/.bash_profile`:
```
vmdappdir='/Applications/VMD1.9.2.app/Contents'
alias vmd='"$vmdappdir/Resources/VMD.app/Contents/MacOS/VMD" $*'
```
**NOTE:** VMD only has 32-bit version for Mac OS X. This is bad because you'll only be able to open
trajectories that are half the size of your RAM. More info on this issue [here](http://www.ks.uiuc.edu/Research/vmd/mailing_list/vmd-l/26606.html).

**I've come up with a solution to this** :heavy_exclamation_mark:
Copy or download the script below and save it somewhere in your 
`$PATH` (for example, `usr/local/bin`). Then make it an executable with `chmod +x load_big_trajs.sh`.


{% highlight bash %}
#!/bin/bash
# This script creates  a .tcl file in the /tmp/ directory
# with the necessary commands to call big trajectories
# from the command line. It uses a stride of 100 frames.
# If it still fails (memory error), change the stride to 
# a bigger number. The file in the /tmp/ directory is
# removed after vmd is closed. 

# Usage: load_big_trajs.sh topology.prmtop trajectories*.nc

if [[ $# -lt 2 ]]; then
    printf "Please provide at least two arguments (top and traj file)\n"
    printf "Usage: load_big_trajs.sh topology.prmtop trajectories*.nc\n"
    exit 1
fi
stride=100
prmtop=$1
tmpfile=$(mktemp /tmp/vmd_readin.tcl)
cat ~/Scripts/StateFile > $tmpfile # Comment this line out if you don't have a StateFile for VMD. Or change the path to were its sitting in your machine.
echo "mol new $prmtop" >> $tmpfile
for var in ${@:2} # We skip the first argument, the top file
do
    echo "mol addfile $var first 0 step $stride waitfor all" >> $tmpfile
done
# REPLACE THE PATH TO YOUR VMD EXECUTABLE!
/Applications/VMD1.9.2.app/Contents/Resources/VMD.app/Contents/MacOS/VMD -e $tmpfile -size 1920 1080
rm $tmpfile
{% endhighlight %}




**Take a look at line 40 in the script and change the path to your VMD executable if it's different!**
If you've followed the previous steps it should be the same as the one in the script, though. Now you'll be able to load multiple trajectory files 
from the command line like so: `load_big_trajs.sh topology.prmtop trajectories*.nc` (provided you have a sensible naming scheme of your trajectories
and they show up sequentially. Check this by doing `ls trajectories*.nc`).

![My helpful screenshot]({{ site.url }}/downloads/thumbsup.gif)


## Installing UCSF Chimera
[Here](https://www.cgl.ucsf.edu/chimera/download.html) are all the downloadables.

Same procedure as VMD. Click on .dmg file, drag Chimera icon to the Applications folder.

The binary is in `/Applications/Chimera.app/Contents/MacOS/chimera`.

### How to use chimera from the command line
Choose between:

  - Create an alias in your `.bash_profile` with `alias chimera = '/Applications/Chimera.app/Contents/MacOS/chimera'`
  - Do a symbolic link to somewhere in your `$PATH` with, for example:´sudo ln -s /Applications/Chimera.app/Contents/MacOS/chimera /usr/local/bin/chimera´

Either option should work.
I *think* `/usr/local/bin` is in the default $PATH, check it by typing `echo $PATH` and looking for it.
If not create it (with sudo) and append it to the $PATH in your `~/.bash_profile`.



