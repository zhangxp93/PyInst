"""
@date: 2024-11-24
@author: zhangxp93
@contact: 937097345@qq.com

"""
# 您可以免费地使用、修改和分发PyInst ，但必须包含原始作者的版权声明和下列许可声明。
"""
MIT License

Copyright (c) [2024] [zhangxp93]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
import pyvisa
import time

import common


# 定义Fswp类，连接Fswp信号源分析仪
class Fswp:
    def __init__(self, instrument_address):
        """
        设置Fswp仪器地址，连接Fswp信号源分析仪
        :param instrument_address:写入仪器地址，例如："USB0::0x0957::0x0E09::MY47402409::0::INSTR"
        """
        common.setup_logging()
        self.instrument_address = instrument_address
        self.rm = pyvisa.ResourceManager()
        self.Fswp = self.rm.open_resource(self.instrument_address)
        time.sleep(0.01)
        response = self.Fswp.query("*IDN?")
        response = response.replace("\n", "").replace("\r", "")  # 删除字符串中的换行符和回车符
        logging.info(f'Instrument identification:{response}')
        logging.info('FSWP连接成功')

    def run_cont(self):
        """
        cont运行
        :return:
        """
        self.Fswp.write('INIT:CONT OFF')
        self.Fswp.write('INIT:CONT ON')

    def run_single(self):
        """
        RUN SINGLE
        :return:
        """
        self.Fswp.write('INIT:CONT OFF')
        self.Fswp.write('INIT:IMM')

    def set_run_single1(self):
        """
        不使用了
        RUN SINGLE
        :return:
        """
        self.Fswp.write('INIT:CONT OFF')
        self.Fswp.write('INIT:IMM')
        #
        star_time = time.time()
        while True:
            opc = self.Fswp.query("*OPC?")
            if opc.strip() == '1':
                logging.info('run single运行完成')
                break
            if time.time() - star_time > 60:
                logging.error(f'运行超时')
            time.sleep(1)

    def set_run_single(self):
        """
        设置仪器为单次运行模式，并等待运行完成，同时记录运行时间。
        """
        try:
            # 设置 PyVISA 的超时时间为 10 秒
            self.Fswp.timeout = 10000  # 单位为毫秒，10 秒

            # 记录开始时间
            start_time = time.time()

            # 发送 SCPI 指令：关闭连续运行，启动单次运行
            self.Fswp.write('INIT:CONT OFF')
            self.Fswp.write('INIT:IMM')

            # 轮询 OPC 状态
            while True:
                opc = self.Fswp.query("*OPC?")
                if opc.strip() == '1':  # 操作完成
                    logging.info('run single 运行完成')
                    break

                # 检查是否超时（超时时间为 60 秒）
                if time.time() - start_time > 60:
                    logging.error('运行超时')
                    break

                # 每 1 秒检查一次
                time.sleep(0.5)

            # 记录结束时间并计算运行时间
            end_time = time.time()
            elapsed_time = end_time - start_time  # 运行时间，单位为秒
            logging.info(f'运行时间: {elapsed_time:.2f} 秒')

        except pyvisa.errors.VisaIOError as e:
            logging.error(f"VisaIOError: {e}")
        except Exception as e:
            logging.error(f"运行出错: {e}")

    def set_cent_freq(self, freq):
        """
        设置中心频率,单位GHz,PN和SP模式都可用
        :param freq:
        :return:
        """
        self.Fswp.write(f'FREQ:CENT {freq}GHz')
        time.sleep(0.001)

    def set_window(self, window):
        """
        选择窗口
        :param window:
        :return:
        """
        self.Fswp.write(f'INST "{window}"')

    def set_marker_x(self, x, offset):
        """
        设置marker
        :param x:
        1,2,3,4,5,6,7
        :param offset:1K,10K,100K,1M,10M,20M,100M
        :return:
        """
        marker_on = self.Fswp.write(f'CALC:MARK{x} ON')  # 打开marker
        self.Fswp.write(f'DISP:MTAB ON')  # 显示marker表
        self.Fswp.write(f'CALC:MARK{x}:X {offset}Hz')
        time.sleep(0.01)

    def query_marker_x(self, x):
        """
        读取mark值
        :param x: 1,2,3,4,5,6,7
        :return:
        """
        marker_value = self.Fswp.query(f'CALC:MARK{x}:Y?')
        return marker_value

    def query_rms(self):
        """
        读取积分抖动rms,fs
        :return:
        """
        jitter_value = float(self.Fswp.query('FETC:RANG2:PNO2:RMS?')) * 1e15
        print('jitter时间：', jitter_value)
        return jitter_value

    def save_csv_png(self, filename):
        """
        存csv与png
        :param filename: 文件名需包含路径，'Z:\\DATA\\186_5514\\186_5514_SIOA201P8_GND_REF300_12000_+35'
        :return:
        """
        self.Fswp.write(f'MMEM:STOR1:TRAC 1,"{filename}.csv"')
        self.Fswp.write(f'MMEM:NAME "{filename}.png"')
        self.Fswp.write('HCOP:IMM')
        logging.info('save_csv_png 运行完成')

    def save_png(self, filename):
        """
        存csv与png
        :param filename: 文件名需包含路径，'Z:\\DATA\\186_5514\\186_5514_SIOA201P8_GND_REF300_12000_+35'
        :return:
        """
        self.Fswp.write(f'MMEM:NAME "{filename}.png"')
        self.Fswp.write('HCOP:IMM')
        logging.info('save_png 运行完成')

    def set_dc_power(self, on_off):
        """
        设置DC POWER
        :param on_off:ON,OFF
        :return:
        """

        self.Fswp.write(f'SOUR:VOLT {on_off}')

    def set_dc_supply_volt(self, volt):
        """
        设置DC voltage supply
        :param volt:电压值
        :return:
        """

        self.Fswp.write(f'SOUR:VOLT:POW:LEV:AMPL {volt}')

    def set_dc_power_on(self):
        """
        设置DC POWER ON
        :return:
        """
        self.Fswp.write(f'SOUR:VOLT ON')

    def set_dc_power_off(self):
        """
        设置DC POWER off
        :return:
        """
        self.Fswp.write(f'SOUR:VOLT OFF')

    def set_vtune(self, vt):
        """
        设置vt电压
        :param vt:
        :return:
        """
        self.Fswp.write(f'SOUR:VOLT:CONT:LEV:AMPL {vt}')

    def set_auto_search_off(self):
        """
        auto_search关闭
        :return:
        """

        self.Fswp.write(f'SENS:ADJ:CONF:FREQ:AUT:STAT OFF')

    def query_freq_cent(self):
        """
        查询频率
        :return:
        """
        freq = float(self.Fswp.query(f'FREQ:CENT?')) / 1e9
        return freq

    def query_singal_power(self):
        power = float(self.Fswp.query(f'POW:RLEV?'))
        return power

    def close(self):
        self.Fswp.close()
        # self.rm.close()
        # print('关闭Fswp连接')
        logging.info('关闭Fswp连接')

    def set_select_pn(self):
        """
        选择相噪模式窗口
        :return:
        """
        self.Fswp.write('INST PNO')

    def set_select_sp(self):
        """
        选择频谱模式窗口
        :return:
        """
        self.Fswp.write('INST SAN')

    def set_peak_search(self):
        self.Fswp.write('CALC:MARK:MAX')

    def set_mark_delt(self):
        self.Fswp.write('CALC:DELT ON')

    def set_mark_delt_freq(self, x, freq):
        self.Fswp.write(f'CALC:DELT{x}:X {freq}MHz')

    def query_mark_delt_x(self, x):
        """
        读取偏移频率
        :return:
        """
        value = self.Fswp.query(f'CALC:DELT{x}:X:REL?')
        return value

    def query_mark_delt_y(self, y):
        value = float(self.Fswp.query(f'CALC:DELT{y}:Y?'))
        return value

    def set_continuous_peak(self):
        self.Fswp.write('CALC:MARK:MAX:AUTO ON')

    def set_mark_all_off(self):
        """
        关闭所有mark
        :return:
        """
        self.Fswp.write('CALC:MARK:AOFF')

    def set_freq_span(self, span):
        """
        sp模式设置span,MHz
        :return:
        """
        self.Fswp.write(f'SENS:FREQ:SPAN {span}MHz')

    def set_bw(self, bw):
        self.Fswp.write(f'SENS:BAND:RES {bw}Hz')

    def set_mark_on(self, x):
        self.Fswp.write(f'CALC:MARK{x}:STAT ON')
        time.sleep(0.01)

    def set_mark_del_on(self, x):
        self.Fswp.write(f'CALC:DELT{x}:STAT ON')
        time.sleep(0.01)

    def set_disp_rlev(self, value):
        self.Fswp.write(f'DISP:WIND:TRAC:Y:SCAL:RLEV {value}')

    def set_signal_source_freq(self, freq):
        """
        设置源频率，GHz
        :param freq:
        :return:
        """
        self.Fswp.write(f'SOUR:GEN:FREQ {freq}MHz')

    def set_signal_source_pow(self, power):
        """
        设置源功率，dBm
        :return:
        """
        self.Fswp.write(f'SOUR:GEN:LEV {power}')

    def set_signal_source_on(self, on_off):
        """
        设置源功率开关,ON,OFF
        :return:
        """
        self.Fswp.write(f'SOUR:GEN:STAT {on_off}')

    def query_vcochar_freq(self):
        """
        读取trac1,freq
        :return:
        """
        freq_value = self.Fswp.query("TRAC1? TRACE1")
        freq_value = freq_value.split(',')
        freq_value = [freq_value[i] for i in range(1, len(freq_value), 2)]  # 第一个值为vt电压，第二个值为freq，步进为2
        freq_value = [float(item) / 1e9 for item in freq_value]
        return freq_value

    def query_vcochar_power(self):
        """
        读取trac2,功率
        :return:
        """
        power = self.Fswp.query("TRAC2? TRACE1")
        power = power.split(',')
        power = [power[i] for i in range(1, len(power), 2)]
        return power

    def query_vcochar_sen(self):
        """
        读取trac3,调谐灵敏度
        :return:
        """
        sen = self.Fswp.query(f"TRAC3? TRACE1")
        sen = sen.split(',')
        sen = [sen[i] for i in range(1, len(sen), 2)]
        sen = [float(item) / 1e6 for item in sen]
        return sen

    def query_vcochar_vt(self):
        """
        读取trac1
        :return:
        """
        vt = self.Fswp.query("TRAC1? TRACE1")
        vt = vt.split(',')
        vt = [vt[i] for i in range(0, len(vt), 2)]
        return vt

    def query_vcochar_icc(self):
        """
        读取trac4
        :return:
        """
        icc = self.Fswp.query(f"TRAC4? TRACE1")
        icc = icc.split(',')
        icc = [icc[i] for i in range(1, len(icc), 2)]
        icc = [float(item) / 1e6 for item in icc]
        return icc


class FswpVcoChar(Fswp):
    def __init__(self, instrument_address):
        super().__init__(instrument_address)

    def query_freq(self):
        """
        读取trac1
        :return:
        """
        freq = self.Fswp.query("TRAC1? TRACE1")
        freq = freq.split(',')
        freq = [freq[i] for i in range(1, len(freq), 2)]
        freq = [float(item) / 1e9 for item in freq]
        return freq

    def query_vt(self):
        """
        读取trac1
        :return:
        """
        vt = self.Fswp.query("TRAC1? TRACE1")
        vt = vt.split(',')
        vt = [vt[i] for i in range(0, len(vt), 2)]
        return vt

    def query_power(self):
        """
        读取trac2
        :return:
        """
        power = self.Fswp.query("TRAC2? TRACE1")
        power = power.split(',')
        power = [power[i] for i in range(1, len(power), 2)]
        return power

    def query_sen(self):
        """
        读取trac3,调谐灵敏度
        :return:
        """
        sen = self.Fswp.query(f"TRAC3? TRACE1")
        sen = sen.split(',')
        sen = [sen[i] for i in range(1, len(sen), 2)]
        sen = [float(item) / 1e6 for item in sen]
        return sen

    def query_icc(self):
        """
        读取trac4
        :return:
        """
        icc = self.Fswp.query(f"TRAC4? TRACE1")
        icc = icc.split(',')
        icc = [icc[i] for i in range(1, len(icc), 2)]
        icc = [float(item) / 1e6 for item in icc]
        return icc

    def set_freq_search_range(self, freq_low, freq_high):
        self.Fswp.write(f"ADJ:CONF:FREQ:LIM:LOW {freq_low}GHz")
        self.Fswp.write(f"ADJ:CONF:FREQ:LIM:HIGH {freq_high}GHz")


class SpotNoiseTune(Fswp):
    def __init__(self, instrument_address):
        super().__init__(instrument_address)

    def query_phase(self, trace):
        phase = self.Fswp.query(f"TRAC1? TRACE{trace}")
        phase = phase.split(',')
        phase = [phase[i] for i in range(1, len(phase), 2)]
        phase[-1] = phase[-1].rstrip("\n")
        return phase

    def query_phase_vt(self, trace):
        phase_vt = self.Fswp.query(f"TRAC1? TRACE{trace}")
        phase_vt = phase_vt.split(',')
        phase_vt = [phase_vt[i] for i in range(0, len(phase_vt), 2)]
        return phase_vt


if __name__ == '__main__':
    addr_fswp = 'TCPIP0::172.16.30.150::inst0::INSTR'
    fswp = Fswp(addr_fswp)
    fswp.set_cent_freq(10)
    fswp.close()
