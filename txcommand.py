
import xml.etree.ElementTree as ET
import httplib, urllib
import argparse
import sys


def send_tx_command(ip, command, timeout = 1.0):
    try:
        res = ""
        params = urllib.urlencode({'param': command})
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn = httplib.HTTPConnection(ip, 80, timeout=timeout)
        conn.request("POST", "/sys__rs232req.xml", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("HTTP response status is not 200. Status = " + str(response.status) )
        data = response.read()
        root = ET.fromstring(data)
        res = root[0].text.lstrip()
        res = res[0:res.find('\r')]
        if  res.find('FE') != -1:
            raise Exception("TX command error. Response: " + res)


    finally:
        conn.close()
    return res



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Sends TX command to Teamcast's module using IP communication protocol and \
                                     prints the response. For example command 'python txcommand.py 192.168.250.3 \
                                     TX2120000100'  sets ASI1 interface of module as a source for the input 1.\
                                     Returned value is 0 in case tx command transaction has been successful, otherwise the returned value is 255. ")
    parser.add_argument('ip', help = 'IP address of the module')
    parser.add_argument('tx_command',  help = 'TX command without whitespaces and \\r\\n (example: TX21A000)')
    parser.add_argument('--timeout', type = float, help = 'Timeout of TX command transaction in seconds', default = 1.0)
    args = parser.parse_args()
    try:
        res = send_tx_command(args.ip, args.tx_command, timeout = args.timeout)
        print res
    except Exception as e:
        print >> sys.stderr , ''.join(("tx_command: Error (",args.ip, ", ", args.tx_command, "): ", str(e)))
        exit(-1)


