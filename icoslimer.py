
import requests
import sys
import time

class IcosLimer:
    
    def __init__(self, url=None):
                
        self.url = url                
        self.session_key = None
        self.headers = {'content-type': 'application/json',
                        'connection': 'Keep-Alive'}
        self.id = int(time.time()*10**6)
        self.usr = None
        self.pwd = None
        
    # -------------------------------------------------
    
    def set_auth(self, usr,pwd):    
        """ Set the authentication for the rpc calls """
        self.usr = usr
        self.pwd = pwd
    # -------------------------------------------------
    
    def set_url(self, url):    
        """ Set the server url for limesurvey remote control """
        self.url = url
        
    # -------------------------------------------------
    
    def set_headers(self, headers):
        """ URL header options, by default json rpc """
        self.headers = headers
        
    # -------------------------------------------------
    
    def set_session_key(self):
        """
            Create a session key. 
        """
        payload = {
                'method': 'get_session_key',
                'params': [self.usr, self.pwd],
                'id': 1,
                }
        # get a session key
        try:
            r = requests.post(self.url, json=payload, headers=self.headers).json()
            self.session_key = r['result']
        except:
            ex = sys.exc_info()[0]
            print ( "Exception: %s" % ex)
            
        return
            
    # -------------------------------------------------
        
    def call_rpc(self,method, params,setid=False):
        """
          Generic call to run a lime rpc call.
          At this moment we assume that a session key
          is stored for this instance.
          
          Args:
                method (str): The name of the RPC's method
                params (list): a list of parameters that is required by the method

            Returns:
                list: The result of the activation
        """
        if setid:
            payload = {"method":method,"params":params, 'id':self.id}
        else:
            payload = {"method":method,"params":params}
            
        #print(payload)
        
        try:
           r = requests.post(url=self.url,
                             headers=self.headers,
                             json=payload)
           return r
        except:
           ex = sys.exc_info()[0]
           print ( "Exception: %s" % ex)
           return


    # -------------------------------------------------
    
    def release_session_key(self):
        """ Closes the RPC session """
        
        if self.session_key:            

            payload = {"method":"release_session_key","params":self.session_key}
            
            r = requests.post(url=self.url, headers=self.headers, json=payload)
            if not r.ok:
                print('session key release failed: ' + r.text)
            
            self.session_key = None
        return
    
    # -------------------------------------------------    
    
    def list_surveys(self):
        """ get a list of all the surveys """
        
        method = 'list_surveys'
        params = [self.session_key, self.usr, self.pwd]
        
        return self.call_rpc(method, params, True).json()

    # -------------------------------------------------
    
    def get_statistics(self, sid, output='html'):
        """ get a list of all the surveys """
        
        method = 'export_statistics'
        params = [self.session_key, self.usr, self.pwd,
                  sid, output]
        params = [self.session_key,sid, output]
        
        return self.call_rpc(method, params, True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        