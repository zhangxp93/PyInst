# 控制N1914A子程序，未完成
import pyvisa
import time


# 定义2401类，连接2401信号源分析仪
class N9020b1:
    def __init__(self, instrument_address):
        """
        设置N1914A仪器地址，连接N1914A信号源
        :param instrument_address:
        """
        self.instrument_address = instrument_address
        self.rm = pyvisa.ResourceManager()
        self.N9020b = self.rm.open_resource(self.instrument_address)
        time.sleep(0.01)
        response = self.N9020b.query("*IDN?")
        print("Instrument identification:", response, '成功连接N9020b')
        time.sleep(0.001)

    def set_freq(self, freq):
        """
        设置频率,单位GHz
        :param freq:
        :return:
        """
        self.N9020b.write(f'SENS:FREQ {freq}GHz')
        time.sleep(0.001)

    def set_freq_cent(self, freq):
        """
        设置中心频率，单位GHz
        :param freq:
        :return:
        """
        self.N9020b.write(f'FREQ:CENT {freq}GHz')
        time.sleep(0.001)

    def set_peak_search(self):
        """
        peak search
        :return:
        """
        self.N9020b.write(f"CALC:MARK1:MAX:PEAK")

    def set_mark_del_on(self, x):
        self.N9020b.write(f"CALC:MARK{x}:MODE DELT")

    def set_mark_aoff(self):
        """
        关闭所有mark
        :return:
        """
        self.N9020b.write(f"CALC:MARK:AOFF")

    def set_mark_del_freq(self, x, freq):
        """
        delt频率，GHz
        :param freq:
        :return:
        """
        self.N9020b.write(f"CALC:MARK{x}:X {freq}MHz")

    def query_mark_delt_x(self, x):
        """
        读取偏移频率
        :return:
        """
        value = self.N9020b.query(f'CALC:MARK{x}:X?')
        return value

    def query_power(self):
        """
        读取功率
        :return:
        """
        power = float(self.N9020b.query(f'FETC?'))
        time.sleep(0.01)
        return power

    def save_png(self, file_addr):

        self.N9020b.write(f'MMEM:STOR:SCR "F:\\{file_addr}.PNG"')

    def close(self):
        """
        关闭仪器n9020b端口
        :return:
        """
        self.N9020b.close()
        print('关闭仪器n9020b端口')

if __name__ == '__main__':
    addr = 'USB0::0x2A8D::0x1C0B::MY60110334::0::INSTR'
    n9020b = N9020b1(addr)
    n9020b.close()


