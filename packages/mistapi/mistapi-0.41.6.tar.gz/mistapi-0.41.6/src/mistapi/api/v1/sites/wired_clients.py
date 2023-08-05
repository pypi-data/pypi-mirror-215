'''
--------------------------------------------------------------------------------
------------------------- Mist API Python CLI Session --------------------------

    Written by: Thomas Munzer (tmunzer@juniper.net)
    Github    : https://github.com/tmunzer/mistapi_python

    This package is licensed under the MIT License.

--------------------------------------------------------------------------------
'''

from mistapi import APISession as _APISession
from mistapi.__api_response import APIResponse as _APIResponse
import deprecation

def countSiteClientsWired(mist_session:_APISession, site_id:str, distinct:str="mac", mac:str=None, device_mac:str=None, port_id:str=None, vlan:str=None, page:int=1, limit:int=100, start:int=None, end:int=None, duration:str="1d") -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/countSiteClientsWired
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    site_id : str        
    
    QUERY PARAMS
    ------------
    distinct : str{'port_id', 'vlan', 'mac'}, default: mac
    mac : str
      client mac
    device_mac : str
      device mac
    port_id : str
      port id
    vlan : str
      vlan
    page : int, default: 1
    limit : int, default: 100
    start : int
    end : int
    duration : str, default: 1d        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/wired_clients/count"
    query_params={}
    if distinct: query_params["distinct"]=distinct
    if mac: query_params["mac"]=mac
    if device_mac: query_params["device_mac"]=device_mac
    if port_id: query_params["port_id"]=port_id
    if vlan: query_params["vlan"]=vlan
    if page: query_params["page"]=page
    if limit: query_params["limit"]=limit
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    
def searchSiteClientsWired(mist_session:_APISession, site_id:str, device_mac:str=None, mac:str=None, port_id:str=None, vlan:str=None, ip_address:str=None, manufacture:str=None, text:str=None, limit:int=100, start:int=None, end:int=None, duration:str="1d") -> _APIResponse:
    """
    API doc: https://doc.mist-lab.fr/#operation/searchSiteClientsWired
    
    PARAMS
    -----------
    mistapi.APISession : mist_session
        mistapi session including authentication and Mist host information
    
    PATH PARAMS
    -----------
    site_id : str        
    
    QUERY PARAMS
    ------------
    device_mac : str
      device mac
    mac : str
      client mac
    port_id : str
      port id
    vlan : str
      vlan
    ip_address : str
    manufacture : str
      manufacture
    text : str
      single entry of hostname/mac
    limit : int, default: 100
    start : int
    end : int
    duration : str, default: 1d        
    
    RETURN
    -----------
    mistapi.APIResponse
        response from the API call
    """
    uri = f"/api/v1/sites/{site_id}/wired_clients/search"
    query_params={}
    if device_mac: query_params["device_mac"]=device_mac
    if mac: query_params["mac"]=mac
    if port_id: query_params["port_id"]=port_id
    if vlan: query_params["vlan"]=vlan
    if ip_address: query_params["ip_address"]=ip_address
    if manufacture: query_params["manufacture"]=manufacture
    if text: query_params["text"]=text
    if limit: query_params["limit"]=limit
    if start: query_params["start"]=start
    if end: query_params["end"]=end
    if duration: query_params["duration"]=duration
    resp = mist_session.mist_get(uri=uri, query=query_params)
    return resp
    