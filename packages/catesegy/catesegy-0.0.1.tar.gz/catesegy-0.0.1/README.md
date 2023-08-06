-----------
DESCRIPTION
-----------

Python client for extracting data from CATE archives and writing as segy data

------------
INSTALLATION
------------

    pip install catesegy


-----
USAGE
-----

See also `catenp.catesegy.Example`


    from catesegy import Authenticate,WriteFile

    # Authenticate to the server
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
   
    # Get the data and save as SEGY
    WriteFile(serverAddress,serverPort,cateUserName,
        tstart,tstop,
        cstart,cstop,
        "test.sgy"
        )



