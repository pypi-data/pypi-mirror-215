'''
Created on 22 Jun 2023

@author: kitchambers
'''

from catenp import Authenticate as CateNPAuth
from catenp import GetData

ArchiveInfo={}

def Authenticate(cateServer,cateServerPort,username,password):
    '''
    Authenticate to server (passes through to `catenp.Authenticate`)
    '''
    
    return CateNPAuth(cateServer,cateServerPort,username,password)


def WriteFile(cateServer,cateServerPort,username,
            tstart,tstop,
            cstart,cstop,
            segyFileName,
            headers=[],
            textHeader=None
            ):
    '''
    Query and download CATE data and write as a segy file
    
    @param cateServer: cate server address
    @type cateServer: str

    @param cateServer: cate server port
    @type cateServer: int
  
    @param username: cate server user name
    @type username: str

    @param tstart: isoformat time string for start of data (first sample)
    @type tstart: str

    @param tstop: isoformat time string for stop of data (last sample)
    @type tstop: str

    @param cstart: channel number for start of data
    @type cstart: int

    @param cstop: channel number for stop of data (inclusive)
    @type cstop: int
    
    @param segyFileName: output segy file name
    @type segyFileName: str
    
    @param headers: additional ObsPy headers to add to the data, should match the channel range
    @type headers: [{}]    
    '''


    # Get the archive info
    global ArchiveInfo
    if (cateServer,cateServerPort,username) not in ArchiveInfo:
        import requests
        import json
        from catenp.catenumpy import CATE_Session_Tokens
        if (cateServer,cateServerPort,username) not in CATE_Session_Tokens:
            raise Exception( "ERROR could not find authentication token for : "+str( (cateServer,cateServerPort,username) ) )
        sessionToken=CATE_Session_Tokens[(cateServer,cateServerPort,username)]
        resp=requests.get("http://"+cateServer+":"+str(cateServerPort)+"/archive_info", 
                       headers={"Authorization": "Bearer "+sessionToken},
                       )   
        if resp.status_code!=200: raise Exception( "ERROR getting archive information message: "+resp.content.decode() )
        ArchiveInfo[(cateServer,cateServerPort,username)]=json.loads(resp.content)
        
    arInfo=ArchiveInfo[(cateServer,cateServerPort,username)]

    # Get the data
    dta = GetData(cateServer,cateServerPort,username,
                  tstart,tstop,
                  cstart,cstop
                  ) 

    # Convert to ObsPy
    import numpy as np
    from obsln import Trace, Stream,UTCDateTime
    from obsln.io.segy.segy import SEGYTraceHeader, SEGYBinaryFileHeader
    from obsln.core import AttribDict
    
    stream = Stream()
    for ii in range(0,dta.shape[0]):
    
        # Data
        #data = np.require(data, dtype=np.float32)
        trace = Trace(data=dta[:,ii].astype(np.float32))
    
        # Example headers
        trace.stats.delta = 1./arInfo["time_axis"]["sample_rate_hz"]
        trace.stats.starttime = UTCDateTime(tstart)
        
        if not hasattr(trace.stats, 'segy.trace_header'): trace.stats.segy = {}
        trace.stats.segy.trace_header = SEGYTraceHeader()
        trace.stats.segy.trace_header.trace_sequence_number_within_line = ii + 1 + cstart
        trace.stats.segy.trace_header.trace_sequence_number_within_segy_file = ii+1
        trace.stats.segy.trace_header.original_field_record_number = ii+1+cstart
        trace.stats.segy.trace_header.trace_number_within_the_original_field_record = ii+1+cstart
        trace.stats.segy.trace_header.trace_identification_code=1
        trace.stats.segy.data_use=1
    
        # Header overrides
        if ii<len(headers): trace.stats.update(headers[ii])

        # Add trace to stream
        stream.append(trace)

    ##print("Stream:")
    ##print(stream)
    
    # Add the textual header
    stream.stats = AttribDict()
    if textHeader!=None:
        stream.stats.textual_file_header=textHeader
    else:
        textual_file_header =""
        for ii in range(0,40):
        
            line="C"+str(ii+1)
            if ii==1: line += "  FORMAT SEG Y REV1"
            if ii==2: line += "  Created by Cate-Segy "
            if ii==3: line += "    Server: "+cateServer
            if ii==4: line += "    Port: "+str(cateServerPort)
            if ii==5: line += "    User: "+username
            if ii==6: line += "    Start Time: "+str(tstart)
            if ii==7: line += "    Stop Time: "+str(tstop)            
            if ii==8: line += "    Start Channel: "+str(cstart)
            if ii==9: line += "    Stop Channel: "+str(cstop)  
            if ii==11: line += "   Data Value Byte ordering: '<'" 
            if ii==12: line += "   Data Value encoding: 4-byte IBM float"
            if ii==38: line += " SEG Y REV1"
            if ii==39: 
                for jj in range(len(line),58): line += " "
                line += "C40 END TEXTUAL HEADER"
       
            if ii!=39:
                for jj in range(len(line),79): line += " "
                line += '\n'
        
            textual_file_header += line
            
        stream.stats.textual_file_header=textual_file_header


    # Add the binary header
    stream.stats.binary_file_header = SEGYBinaryFileHeader()
    stream.stats.binary_file_header.trace_sorting_code = 5

    # Write out
    stream.write(segyFileName, format="SEGY", 
                 data_encoding=1,
                 byteorder='<',
                 textual_header_encoding="EBCDIC")
    
    


def Example():
    '''
    Simple test / example functionality
    '''

    print("\n*********************\nTest/ Example functionality\n******************\n")

    print("\n*********************\nRead in server data")

    with open("./test-data.txt") as fd:
        serverAddress = fd.readline().rstrip()           # CATE Server address (example 1.2,3,4)
        serverPort = int(fd.readline().rstrip())         # CATE Server port (example 8000)
        cateUserName = fd.readline().rstrip()            # User name on the server
        catePassword = fd.readline().rstrip()            # Password on the server
        
        tstart = fd.readline().rstrip()                  # Start of time interval to get
        tstop = fd.readline().rstrip()                   # Stop of time interval to get
        cstart = int( fd.readline().rstrip() )           # Start of channel interval to gets
        cstop = int( fd.readline().rstrip() )            # End of channel interval to get
        
        
    print("Got server details:")
    print("   Server=",serverAddress)  
    print("   port=",serverPort)  
    print("   User=",cateUserName)  
    
    
    print("\n*********************\nAuthenticate")
    tk = Authenticate(serverAddress,serverPort,cateUserName,catePassword)
    print("Got session token: ",tk)


    # Get some data
    print("\n*********************\nGetting data",flush=True)
    WriteFile(serverAddress,serverPort,cateUserName,
            tstart,tstop,
            cstart,cstop,
            "test.sgy"
            )
    



if __name__ == '__main__':
    Example()