At the moment we are using a maya module to configure the maya start up.
Modules are basically just virtual re recreations the maya users start up. A module points to a new file structure that makes up the paths maya is looking for. IE maya looks at the scripts folder if you want to import a module into the maya session.
The .mod file location has to be referenced by your maya.env under the " MAYA_MODULE_PATH " for the path to be initialized.
The .mod file then references the name of the module and its location, can be relative to itsself. The module is a reference to the directory structure. You can have many modules that all mirror that structure which makes separating scripts nice and easy and all using only one varaiable in the maya env.
Using a env variable to set the path seemed to break the creation of other variables in the file.

=               -creates a new variable
PATH:=menus     -the absolute path of the folder "menus" in the MAYA_MOUDULE_PATH

there is more syntax like this....google maya module and you will find it

