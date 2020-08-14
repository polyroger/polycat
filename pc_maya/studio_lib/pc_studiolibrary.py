def launchSL():

    import studiolibrary

    libraries = [
        {"name":"Gracie_and_pedro", "path":r"\\YARN\projects\mov\gra\1_assets\animation\studiolibrary", "default":True, "theme":{"accentColor":"rgb(0,200,100)"}},
        {"name":"Noodle_and_bun", "path":r"\\YARN\projects\ply\nod\1_assets\animation\studiolibrary"},
    ]

    studiolibrary.setLibraries(libraries)
    studiolibrary.main()