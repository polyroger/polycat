def launchSL():

    import studiolibrary

    libraries = [
    {"name":"Noodle and Bun", "path":r"\\YARN\projects\ply\nod\1_assets\animation", "default":True, "theme":{"accentColor":"rgb(0,200,100)"}},
    {"name":"Project2", "path":r"\\YARN\projects\mov\gra\1_assets\animation"},
    ]


    studiolibrary.setLibraries(libraries)
    studiolibrary.main()