import threading
import time
import socket
import struct
import time
import sys
import datetime
class ModbusData:
    def __init__(self,IP,port):
        self.IP = IP
        self.port = port
        self.header = ''
        self.X = []
        self.Y = []
        self.Z = []
        self.Pd = []
        self.Dis = []
        self.Stime = []
        self.Etime = ''
        self.SPS = 0
        self.connect_success=False
        self.wait=False

        self.lock = threading.Lock()
        self.background_thread = threading.Thread(target=self.connect, args=(IP,port), daemon=True)
        self.background_thread.start()

    def connect(self,IP,port):
        arr = [0x01, 0x02, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0xc0, 0x00, 0x01]
        link=struct.pack("%dB"%(len(arr)),*arr)

        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e: 
            print ("Error creating socket: %s" % e) 
            sys.exit(1) 
        
        # Second try-except block -- connect to given host/port 
        try: 
            client.connect((IP,port))
            print("connect success")
            #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' + str(datetime.datetime.now()))
            self.connect_success = True
        except : 
            print ("FAIL") 
            sys.exit(1) 
        

        client.send(link)

        while True:
            link1 = client.recv(2500)
            
            data = link1.hex()
            #print(data)
            if(data == "010200000006010600c00001"):
                continue
            #print(len(data))
            header = data[:400]
            self.header = header
            #print(header)
            packet_type = data[2:4] + data[0:2]
            #print(packet_type)
            event_flag = data[6:8] + data[4:6]
            #print(event_flag)
            Syear =  int(data[10:12] + data[8:10] ,16)
            Smonth =  int(data[14:16] + data[12:14] ,16)
            Sday =  int(data[18:20] + data[16:18] ,16)
            Shour =  int(data[22:24] + data[20:22] ,16) 
            Sminute = int(data[26:28] + data[24:26],16)
            Ssecond = int(data[30:32],16)
            Smsecond = int(data[28:30],16)
            Stime = str(Syear) + "-" + str(Smonth) + "-" + str(Sday) + "-" + str(Shour) + "-" + str(Sminute) + "-" + str(Ssecond) + "-" + str(Smsecond)
            #print(Stime)
            self.Stime.append(Stime)
            Eyear =  int(data[34:36] + data[32:34] ,16)
            Emonth =  int(data[38:40] + data[36:38] ,16)
            Eday =  int(data[42:44] + data[40:42] ,16)
            Ehour =  int(data[46:48] + data[44:46] ,16) 
            Eminute = int(data[50:52] + data[48:50],16)
            Esecond = int(data[54:56],16)
            Emsecond = int(data[52:54],16)
            Etime = str(Eyear) + "-" + str(Emonth) + "-" + str(Eday) + "-" + str(Ehour) + "-" + str(Eminute) + "-" + str(Esecond) + "-" + str(Emsecond)
            #print(Etime)
            self.Etime = Etime
            
            self.SPS = int(data[396:398] ,16)

            XYZdata = data[400:]
            xconnect, yconnect, zconnect, Pdconnect, Disconnect = data_cut(XYZdata)
            #print(len(xconnect)) --- 100
            self.X.extend(xconnect)
            self.Y.extend(yconnect)
            self.Z.extend(zconnect)
            self.Pd.extend(Pdconnect)
            self.Dis.extend(Disconnect)
            #print(len(self.X))
            if(len(self.X)>1000):
                del self.X[:100]
                del self.Y[:100]
                del self.Z[:100]
                del self.Pd[:100]
                del self.Dis[:100]
                del self.Stime[:1]
    

    def get_IP(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.IP
        except :
            print("Connect Fail, so Nothing in list")

    def get_Port(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.port
        except :
            print("Connect Fail, so Nothing in list")

    def get_Header(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.header
        except :
            print("Connect Fail, so Nothing in list")

    def get_Now_Channel1(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.X[-100:]
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel2(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Y[-100:]                  
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_Channel3(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Z[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Pd(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Pd[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Displacement(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Dis[-100:]          
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_SystmeTime(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Stime[-1]
        except :
            print("Connect Fail, so Nothing in list")
    def get_Now_EventTime(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.Etime
        except :
            print("Connect Fail, so Nothing in list")
    def get_SPS(self):
        if(self.wait == False):
            time.sleep(2)
            self.wait = True
        try:
            return self.SPS
        except :
            print("Connect Fail, so Nothing in list")
    def get_NsecondChannel1Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Xreturn = []
        UTreturn = []
        try:
            Xreturn.extend(self.X[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Xreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
    def get_NsecondChannel2Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Yreturn = []
        UTreturn = []
        try:
            Yreturn.extend(self.Y[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Yreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
        
    def get_NsecondChannel3Data(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Zreturn = []
        UTreturn = []
        try:
            Zreturn.extend(self.Z[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Zreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")

    def get_NsecondPd(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Pdreturn = []
        UTreturn = []
        try:
            Pdreturn.extend(self.Pd[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Pdreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")

    def get_NsecondDisplacement(self,N):
        #print("len(Data)" + str(len(Data)))
        if(N == 0):
            print("Don't input 0, return now Data")
            N = 1
        elif(len(self.Stime)<N):
            print("Only have "+ str(len(self.Stime)) + " Second Data")
            N = len(self.Stime)
        elif(N >60):
            print("We only store 60s Data")    
        N1000 = N*100
        Disreturn = []
        UTreturn = []
        try:
            Disreturn.extend(self.Dis[-N1000:])
            UTreturn.extend(self.Stime[-N:])
            return Disreturn, UTreturn
            
        except :
            if(self.connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")


def data_cut(XYZstr):
    
    xdata_cut = []
    ydata_cut = []
    zdata_cut = []
    PD_cut = []
    Dis_cut = []
    flag = 0
    #Little Endian 轉回正常
    XYZhex = ''
    #print(len(XYZstr))
    
    #每4個byte為一組處理
    for i in range(0, len(XYZstr), 4):
        XYZdecimal=0
        a = XYZstr[i:i+2]
        b = XYZstr[i+2:i+4]
        XYZhex = b+a
        #hex to decimal 
        #print(XYZhex)

        #儲存進XYZ的陣列
        if(flag == 0):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536  # 转换为有符号整数
            XYZdecimal = round(XYZdecimal/16.718,4)
            #print(XYZdecimal)
            xdata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 1):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = round(XYZdecimal/16.718,4)
            #print(XYZdecimal)
            ydata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 2):
            hex_string = XYZhex  # 十六进制字符串
            unsigned_integer = int(hex_string, 16)  # 将十六进制字符串转换为无符号整数
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            XYZdecimal = round(XYZdecimal/16.718,4)
            #print(XYZdecimal)
            zdata_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 3):
            hex_string = int(XYZhex,16) 
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            PD_cut.append(XYZdecimal)
            flag = flag +1
        elif(flag == 4):
            hex_string = int(XYZhex,16) 
            XYZdecimal = unsigned_integer if unsigned_integer < 32768 else unsigned_integer - 65536
            Dis_cut.append(XYZdecimal)
            flag = 0

    return xdata_cut, ydata_cut, zdata_cut, PD_cut, Dis_cut

if __name__ == '__main__':

    XXXX = ModbusData('10.0.0.227',502)
    
    while True:
        #bbbb = aaaa.get_Now_Channel1()
        data = XXXX.get_Displacement()
        print(data)
        data = XXXX.get_Pd()
        print(data)
        time.sleep(1)
       
    
