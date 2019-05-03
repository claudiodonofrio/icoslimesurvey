
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
        
    def call_rpc(self,method, params,setid=True):
        """
          Generic call to run a lime rpc call.
          At this moment we assume that a session key
          is stored for this instance.
          
          @param method (str): The name of the RPC's method
          @param params [list]: an array of parameters
              that is required by the method
          @param setid (bool): default False. If set to 
              True, rpc call will include the session id                
          @return raw response from "requests" module                
        """
        
        if setid:
            payload = {"method":method,"params":params, 'id':self.id}
        else:
            payload = {"method":method,"params":params}
        
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
    
    def set_session_key(self):
        """
            Create a session key.             
        """
        method = 'get_session_key'
        params = [self.usr, self.pwd]

        # get a session key
        try:
            r = self.call_rpc(method, params).json()
            self.session_key = r['result']
        except:
            ex = sys.exc_info()[0]
            print ( "Exception: %s" % ex)            
        return

    # -------------------------------------------------
    
    def release_session_key(self):
        """ 
            Close the RPC session

            Using this function you can close a previously opened session.
            @access public
            @param string $sSessionKey the session key
            @return string OK
        """
        
        if self.session_key:
            method = 'release_session_key'
            params = self.session_key
            r = self.call_rpc(method, params, False)
            if not r.ok:
                print('session key release failed: ' + r.text)
            
            self.session_key = None
        return
    
    # -------------------------------------------------    
    
    def list_surveys(self):
        """
            List the survey belonging to a user

            If user is admin he can get surveys of every user
                (parameter sUser) or all surveys (sUser=null)
            Else only the surveys belonging to the user requesting will be shown.
            Returns array with
             * `sid` the ids of survey
             * `surveyls_title` the title of the survey
             * `startdate` start date
             * `expires` expiration date
             * `active` if survey is active (Y) or not (!Y)
            
             @access public
             @param string $sSessionKey Auth credentials
             @param string|null $sUsername (optional) username
                 to get list of surveys
             @return array In case of success the list of surveys
        """
        
        method = 'list_surveys'
        params = [self.session_key]
        return self.call_rpc(method, params).json()

    # -------------------------------------------------
    
    def get_statistics(self, sid, output='html', lang='', graph='0'):
        """            
            Export statistics of a survey to a user.           
            Allow to export statistics available Returns string - 
            base64 encoding of the statistics.
            
            @access public
            @param string $sSessionKey Auth credentials
            @param int $iSurveyID ID of the Survey
            @param string $docType (optional) Type of documents the exported
                statistics should be (pdf|xls|html)
            @param string $sLanguage (optional) language of the survey to use
            @param string $graph (optional) Create graph option (default : no)
            @param int|array $groupIDs (optional)
                array or integer containing the groups we choose
                to generate statistics from
            @return string|array in case of success :
                Base64 encoded string with the statistics file
     """
        
        method = 'export_statistics'
        params = [self.session_key,sid, output, lang, graph]        
        return self.call_rpc(method, params).json()
        
    # -------------------------------------------------
    
    def get_timeline(self, sid, stype, start, end):
        
        """
            RPC Routine to export submission timeline.
            Returns an array of values (count and period)
     
            @access public
            @param string $sSessionKey Auth credentials
            @param int $iSurveyID ID of the Survey
            @param string $sType (day|hour)
            @param string $dStart
            @param string $dEnd
            @return array On success: The timeline. On failure array with
                error information
           
        """
        method = 'export_timeline'
        params = [self.session_key,sid, stype, start, end]        
        return self.call_rpc(method, params).json()
        
    # -------------------------------------------------        

    def export_responses(self, sid, stype='json'):
        """
        Export responses in base64 encoded string
     
        @access public
        @param string $sSessionKey Auth credentials
        @param int $iSurveyID ID of the Survey
        @param string $sDocumentType any format available by plugins (for example : pdf, csv, xls, doc, json)
        @param string $sLanguageCode (optional) The language to be used
        @param string $sCompletionStatus (optional) 'complete','incomplete' or 'all' - defaults to 'all'
        @param string $sHeadingType (optional) 'code','full' or 'abbreviated' Optional defaults to 'code'
        @param string $sResponseType (optional)'short' or 'long' Optional defaults to 'short'
        @param integer $iFromResponseID (optional)
        @param integer $iToResponseID (optional)
        @param array $aFields (optional) Selected fields
        @return array|string On success: Requested file as base 64-encoded string. On failure array with error information
        """
        
        method = 'export_responses'
        params = [self.session_key,sid, stype] 
        return self.call_rpc(method, params).json()
        
        
        
        
        
        
        
        
        
        
        
        
        
        