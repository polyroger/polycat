launch houdini with variables set in hcmd command prompt. two batch files the one sets all the variables and launcehs houdini. The other tells that batch to execute. We could
also try this using a python sub process. a script could write the batch file and the subprocess execute that hcmd bat  

a python launcher gets information from a database and through the launchers user input writes out the new batchfile. When houdini closed the env batchfile should be deleted.
the 123.py file should be used to get declared variables and set certain attributes eg frame range in the playback options. ( these cannot be set with global variables )

the varribales in the bacth files shouldnt have spaces
y