#coding=utf-8

import socket
import threading
import re
import urllib2
import xml.dom.minidom

class UPnP(threading.Thread):
    def __init__(self):
        self.ctrl_url = ''
        self.service_type = ''
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind( ('',0) )
        ssdp_req = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN:"ssdp:discover"\r\nMX:3\r\nST:UPnP:rootdevice\r\n\r\n'
        self.udp_sock.sendto( ssdp_req,('239.255.255.250',1900) )
    
    def __get_information(self, location):
        req = urllib2.Request( location,unverifiable=True )
        info = urllib2.urlparse.urlparse( location )
        req.add_header( 'HOST', info[1] )
        
        fp = urllib2.urlopen( req )
        data = ''
        for buf in fp:
            data += buf
        fp.close()
        return data
    
    def __get_local_ip(self):
        soock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soock.connect(('baidu.com', 0))
        ip,port = soock.getsockname()
        sock.shutdown(socket.SHUT_RDWR)
        scok.close()
        return ip
    
    def get_port_map(self,PortMappingIndex):
        if self.ctrl_url == '':
            return ''
        actionName = 'GetGenericPortMappingEntry'
        actionParams = '<NewPortMappingIndex>%d</NewPortMappingIndex>\r\n\
        <NewRemoteHost></NewRemoteHost>\r\n\
        <NewExternalPort></NewExternalPort>\r\n\
        <NewProtocol></NewProtocol>\r\n\
        <NewInternalPort></NewInternalPort>\r\n\
        <NewInternalClient></NewInternalClient>\r\n\
        <NewEnabled>1</NewEnabled>\r\n\
        <NewPortMappingDescription></NewPortMappingDescription>\r\n\
        <NewLeaseDuration></NewLeaseDuration>\r\n' % (PortMappingIndex)
        control_doc = '<?xml version="1.0" encoding="utf-8"?>\r\n\
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\r\n\
        <s:Body>\r\n\
        <u:%s xmlns:u="%s">\r\n\
        %s</u:%s>\r\n\
        </s:Body>\r\n\
        </s:Envelope>\r\n' % (actionName,self.service_type,actionParams,actionName)
        up = urllib2.urlparse.urlparse(self.ctrl_url)
        header = 'POST %s HTTP/1.1\r\nHost: %s\r\n' %( up[2],up[1] )
        header += 'SOAPACTION: "' + serviceType + '#'+ actionName +'"\r\n'
        header += 'CONTENT-TYPE: text/xml\r\n'
        header += 'Content-Length: '+ str( len( control_doc ) ) + '\r\n\r\n'
        req = header + control_doc
        host,port = up[1].split(':')
        result, data = self.__communicate_with_upnp_server(host,port,req)
        return data
    
    def __communicate_with_upnp_server( self, host, port, req ):
        #send request
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( (host,int(port)) )
        sock.send( req )
        data = ''
        while 1:
            buf = fd.recv(1492)
            if len(buf)>0:
                data += buf
            else:
                break
        sock.close()
        #check the response
        is_ok = True
        try:
            s1,s2 = data.split('\r\n',1)
        except:
            s1 = ''
        if not s1.endswith('200 OK'):
            is_ok = False
        return (is_ok,data)

    def add_port(self,ExternalPort,Protocol,InternalPort):
        if ctrl_url == '':
            return ''
        InternalClient = self.__get_local_ip()
        actionName = 'AddPortMapping'
        actionParams = '<NewRemoteHost></NewRemoteHost>\r\n\
        <NewExternalPort>%d</NewExternalPort>\r\n\
        <NewProtocol>%s</NewProtocol>\r\n\
        <NewInternalPort>%d</NewInternalPort>\r\n\
        <NewInternalClient>%s</NewInternalClient>\r\n\
        <NewEnabled>1</NewEnabled>\r\n\
        <NewPortMappingDescription>upnp.py</NewPortMappingDescription>\r\n\
        <NewLeaseDuration>0</NewLeaseDuration>\r\n' % (ExternalPort,Protocol,InternalPort,InternalClient)
        control_doc = '<?xml version="1.0" encoding="utf-8"?>\r\n\
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\r\n\
        <s:Body>\r\n\
        <u:%s xmlns:u="%s">\r\n\
        %s</u:%s>\r\n\
        </s:Body>\r\n\
        </s:Envelope>\r\n' % (actionName,self.serviceType,actionParams,actionName)
        up = urllib2.urlparse.urlparse(self.ctrl_url)
        header = 'POST %s HTTP/1.1\r\nHost: %s\r\n' %( up[2],up[1] )
        header += 'SOAPACTION: "' + serviceType + '#'+ actionName +'"\r\n'
        header += 'CONTENT-TYPE: text/xml\r\n'
        header += 'Content-Length: '+ str( len( control_doc ) ) + '\r\n\r\n'
        req = header + control_doc
        host,port = up[1].split(':')
        result,data = self.__communicate_with_upnp_server(host,port,req)
        if result:
            print 'OK, ADD ',InternalClient,Protocol,str(ExternalPort)
        else:
            print 'ADD Fail'
        return data
    
    def del_port(self,ExternalPort,Protocol):
        if self.ctrl_url == '':
            return ''
        actionName = 'DeletePortMapping'
        actionParams = '<NewRemoteHost></NewRemoteHost>\r\n\
        <NewExternalPort>%d</NewExternalPort>\r\n\
        <NewProtocol>%s</NewProtocol>\r\n' % (ExternalPort,Protocol)
        control_doc = '<?xml version="1.0" encoding="utf-8"?>\r\n\
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\r\n\
        <s:Body>\r\n\
        <u:%s xmlns:u="%s">\r\n\
        %s</u:%s>\r\n\
        </s:Body>\r\n\
        </s:Envelope>\r\n' % (actionName,self.serviceType,actionParams,actionName)
        up = urllib2.urlparse.urlparse(self.ctrl_url)
        header = 'POST %s HTTP/1.1\r\nHost: %s\r\n' %( up[2],up[1] )
        header += 'SOAPACTION: "' + serviceType + '#'+ actionName +'"\r\n'
        header += 'CONTENT-TYPE: text/xml\r\n'
        header += 'Content-Length: '+ str( len( control_doc ) ) + '\r\n\r\n'
        req = header + control_doc
        host,port = up[1].split(':')
        result,data = self.__communicate_with_upnp_server(host,port,req)
        if result:
            print 'OK'
        else:
            print 'Fail'
        return data
        
    def run(self):
        while 1:
            try:
                data,addr = self.udp_sock.recvfrom(4096)
                
                #get location
                ret = re.findall( '[Ll][Oo][Cc][Aa][Tt][Ii][Oo][Nn]: ([^\r]*)',data )
                location = ret[0]
                print 'discription:',location
                
                #get control url from the xml
                igd = xml.dom.minidom.parseString(self.get_information(location))
                for service in igd.getElementsByTagName('service'):
                    val = {}
                    for child in service.childNodes:
                        try:
                            val[child.nodeName.lower()] = child.childNodes[0].nodeValue
                        except:
                            pass
                    if (val['servicetype'].lower()=='urn:schemas-upnp-org:service:wanpppconnection:1') or\
                       (val['servicetype'].lower()=='urn:schemas-upnp-org:service:wanipconnection:1'):
                        self.ctrl_url = urllib2.urlparse.urljoin( location,val['controlurl'] )
                        self.service_type = val['servicetype']
                        break
                        
                #ret = self.get_port_map( 1 )
            except:
                pass