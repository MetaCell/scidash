# Docker Files for scidash

To build
--------

./rebuild.sh

To run once built
-----------------

./run.sh

(Note: if you are a member of the Docker Hub Repository, you can do a docker login and then this will give you the ability to pull from docker hub instead of having to rebuild locally.  Note the image can get big, so it may be faster to build locally if you have a slow connection).

To look at logs when running
----------------------------

./logs.sh

To login to the running container
---------------------------------

./login.sh

To stop and remove the running container
----------------------------------------

./stop.sh