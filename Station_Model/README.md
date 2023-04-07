The main purpose of this code is to plot the weather data into Station Model

This code has two types of Data Collection.
    1. Fetch Data from **[Meteostat]([url](https://meteostat.net/en/about))** API (Meteostat processes data from various public sources. This allows both developers and end users to access weather and climate data through a single interface. Think of it as a gateway to meteorological data which puts user experience first.)
    2. Upload a Data File containing weather data, accepted formats for the file are (.csv, .txt, .nc, .xml)

Based on the method used for Data collection, the respective data is converted into a dataframe.


The Dataframe is then pushed into Parameters Validation Method and only accepts necessary parameters to plot into a dictionary of Parameter names as keys, and respective observation value as values.


Then the Final step is to plot the weather station model using Matplotlib,  and save the image in directory
