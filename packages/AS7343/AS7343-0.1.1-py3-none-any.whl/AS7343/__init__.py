from .addr import *
from machine import SoftI2C,Pin,I2C
import time,math
class AS7343:
    def __init__(self,i2cid,sda,scl,addr=addr.AS7343_ADDR_A):
        "define AS7343"
        self.addr=addr
        self.i2c = I2C(i2cid,scl=Pin(scl),sda=Pin(sda))
    def AS7343_read(self,regAddress):
        rx_buffer=ord(self.i2c.readfrom_mem(self.addr, regAddress, 1));
        return rx_buffer;
    def AS7343_write(self,regAddress,data):
        data=bytearray([data])
        return self.i2c.writeto_mem(self.addr,regAddress,data);
    def get_channel_data(self,channel):
          channelData = 0x0000;
          b1=self.i2c.readfrom_mem(self.addr,addr.AS7343_DATA_0_L + channel*2,1)
          b2=self.i2c.readfrom_mem(self.addr,addr.AS7343_DATA_0_H + channel*2,1)
          channelData = ord(b2);
          channelData = (channelData<<8) | ord(b1);
          return channelData
    def power(self ,power=True):
        '''Start AS7343'''
        self.AS7343_write(addr.AS7343_ENABLE, power);
    def enable_spectral_measurement(self,enable=True):
	'''Enable or disable test'''
        self.AS7343_write(addr.AS7343_ENABLE, 0x01 | (enable)<<1);
    def set_SMUX_F1_F4(self):
	'''Switch senser to F1-F4 mode'''
        self.AS7343_write(addr.AS7343_CFG9, 0x10);
        self.AS7343_write(addr.AS7343_INTENAB, 0x01);
        self.AS7343_write(addr.AS7343_CFG6, 0x10);
        self.AS7343_write(0x00, 0x05);
        self.AS7343_write(0x01, 0x02);
        self.AS7343_write(0x02, 0x10);
        self.AS7343_write(0x03, 0x04);
        self.AS7343_write(0x04, 0x55);
        self.AS7343_write(0x05, 0x00);
        self.AS7343_write(0x06, 0x30);
        self.AS7343_write(0x07, 0x05);
        self.AS7343_write(0x08, 0x06);
        self.AS7343_write(0x09, 0x00);
        self.AS7343_write(0x80, 0x11);

    def set_SMUX_F5_F8(self):
        '''Switch senser to F5-F8 mode'''
        self.AS7343_write(AS7343_CFG9, 0x10);
        self.AS7343_write(AS7343_INTENAB, 0x01);
        self.AS7343_write(AS7343_CFG6, 0x10);
        self.AS7343_write(0x00, 0x05);
        self.AS7343_write(0x01, 0x20);
        self.AS7343_write(0x02, 0x00);
        self.AS7343_write(0x03, 0x40);
        self.AS7343_write(0x04, 0x55);
        self.AS7343_write(0x05, 0x31);
        self.AS7343_write(0x06, 0x00);
        self.AS7343_write(0x07, 0x05);
        self.AS7343_write(0x08, 0x06);
        self.AS7343_write(0x09, 0x00);
        self.AS7343_write(0x80, 0x11);
    def direct_config(self):
        '''Init AS7343'''
        self.AS7343_write(addr.AS7343_CFG6, 0x0);
        self.AS7343_write(addr.AS7343_FD_CFG0, 0xa1);
        self.AS7343_write(addr.AS7343_CFG10, 0xf2);
        self.AS7343_write(addr.AS7343_CFG0, 0x10);
        self.AS7343_write(addr.AS7343_CFG1, 0x0c);
        self.AS7343_write(addr.AS7343_CFG8, 0xc8);
        self.AS7343_write(addr.AS7343_CFG20, 0x62);
        self.AS7343_write(addr.AS7343_AGC_GAIN_MAX, 0x99);
        self.AS7343_write(addr.AS7343_FD_TIME_1, 0x64);
        self.AS7343_write(addr.AS7343_FD_TIME_2, 0x21);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x04);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x65);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x02);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x05);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x01);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x30);
        self.AS7343_write(0xe4, 0x46);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x60);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x20);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x04);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x50);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x03);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x01);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x05);
        self.AS7343_write(0xe4, 0x56);
        self.AS7343_write(0xe7, 0x05);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x60);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x30);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x40);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x10);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x20);
        self.AS7343_write(0xe4, 0x66);
        self.AS7343_write(0xe7, 0x00);
        self.AS7343_write(0xe4, 0x66);

    def set_cycle(self,cycle):
        '''Set sensor cycle ex:0-1-2-3'''
        self.AS7343_write(addr.AS7343_CFG20, cycle<<5);
    def get_AVALID_bit(self):
        status2 = self.AS7343_read(addr.AS7343_STATUS2);
        return (status2 & 0x40) > 0;
    def check_saturation(self):
        status2 = self.AS7343_read(addr.AS7343_STATUS2);
        return (status2 & 0x10) > 0;
    def delay_for_reading(self):
        while not self.get_AVALID_bit():
            time.sleep(0.01)

    def get(self,output=list):
        '''get all data to a LIST or a DICT'''
        self.enable_spectral_measurement(True);
        self.delay_for_reading();
        self.enable_spectral_measurement(False);
        _all_data=['FZ', 'FY', 'FXL', 'NIR', '2xVIS1', 'FD1','F2', 'F3', 'F4', 'F6', '2xVIS2', 'FD2','F1', 'F7', 'F8', 'F5', '2xVIS3', 'FD3']
        if output not in [list,dict]:raise TypeError("No available type (dict,list)")
        data=output()
        for i in range(0,18):
            if output==list:
                data.append(self.get_channel_data(i))
            elif output==dict:
                data[_all_data[i]]=(self.get_channel_data(i))
        return data
        
    def set_gain(self,gain_raw):
        self.AS7343_write(addr.AS7343_CFG1, gain_raw);
    def get_gain(self):
        return self.AS7343_read(addr.AS7343_CFG1);
    def set_TINT(self,TINT):
        ATIME=0
        while 1:
            ASTEP = ((TINT/(ATIME+1))*720.0/2.0);
            if (abs(((ATIME+1)*(ASTEP+1)*2/720) - TINT) <=1):
                break
            else:
                ATIME += 1;
        self.AS7343_write(addr.AS7343_ATIME, ATIME);
        self.AS7343_write(addr.AS7343_ASTEP_LSB, (int(ASTEP) & 0xFF));
        self.AS7343_write(addr.AS7343_ASTEP_MSB, (int(ASTEP)>>8));
    def set_LED(self,on,current_ma=16):
        '''Set led on off and led current'''
        self.AS7343_write(addr.AS7343_LED,(on<<7)+int((current_ma-4)/2));
    def get_flicker(self):
        data=self.AS7343_read(addr.AS7343_FD_STATUS);
        return data;
    def optimizer(self,max_TINT=1000):
        '''Auto set sensor mode'''
        currentGain = 12;
        FSR = 65535;
        TINT = 182.0;
        self.set_TINT(TINT);

        while (True):
            max_count = 0;
            min_count = 0xffff;
            self.set_gain(currentGain);
            self.enable_spectral_measurement(True);
            data=self.get()
            self.enable_spectral_measurement(False);

            for i in range(0,18):
                if (i == 5 or i == 11 or i == 17):
                    continue;
                if (data[i]>max_count):
                    max_count = data[i]
                if (data[i]<min_count):
                    min_count = data[i]
            if (max_count > 0xE665):
                if(currentGain == 0):
                    break;
                currentGain -= 1;
                continue;
            elif (min_count == 0):
                if(currentGain == 12):
                    break;
                currentGain += 1;
                continue
            else:
                break

        counts_expected = float(max_count)
        multiplier = 0.90

        while (True):
            max_count = 0;
            exp = (multiplier*float(FSR-counts_expected));
            if (exp<0):
                break;
            temp_TINT = TINT + pow(2, math.log((multiplier*float(FSR-counts_expected)))/math.log(2))*(2.0/720.0);

            if (temp_TINT>max_TINT):
                break;

            self.set_TINT(temp_TINT);

            self.enable_spectral_measurement(True);
            data=self.get();
            self.enable_spectral_measurement(False);

            for i in range(0,18):
                if (i == 5 or i == 11 or i == 17):
                    continue;
                if (data[i]>max_count):
                    max_count = data[i];
                    

            if (max_count >= multiplier*0xFFEE):
                multiplier = multiplier - 0.05;
                continue;
            else:
                TINT = temp_TINT;
            break;
        self.set_gain(currentGain);
        self.set_TINT(TINT);
    def get_CIE1931(self):
        '''Try to get CIE1931 xy value'''
        all_data=self.get(dict)
        cie_x=all_data["FXL"]/(all_data["FXL"]+all_data["FY"]+all_data["FZ"])
        cie_y=all_data["FY"]/(all_data["FXL"]+all_data["FY"]+all_data["FZ"])
        return (cie_x,cie_y)