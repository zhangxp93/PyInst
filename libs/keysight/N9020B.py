from typing import Union

import pyvisa
import time
import logging





class N9020b:
    def __init__(self, instrument_address):
        """
        设置N9020B仪器地址，初始化类
        :param instrument_address:
        """
        self.instrument_address = instrument_address
        self.rm = pyvisa.ResourceManager()
        self.N9020b = None

    def open(self):
        """
        打开N9020B的连接
        """
        if self.N9020b is None:
            self.N9020b = self.rm.open_resource(self.instrument_address)
            time.sleep(0.01)
            response = self.N9020b.query("*IDN?")
            logging.info(f"Instrument identification: {response}, 成功连接N9020b")
            time.sleep(0.001)
        else:
            logging.warning('连接已经打开')

    def close(self):
        """
        关闭仪器n9020b端口
        :return:
        """
        if self.N9020b is not None:
            self.N9020b.close()
            self.N9020b = None
            logging.info('关闭仪器n9020b端口')
        else:
            logging.warning('端口已经关闭')

    def set_freq(self, freq):
        """
        设置频率,单位GHz
        :param freq:
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f'SENS:FREQ {freq}GHz')
            time.sleep(0.001)
            logging.info(f'设置频率: {freq} GHz')
        else:
            logging.error("请先打开连接")

    def set_freq_cent(self, freq):
        """
        设置中心频率，单位GHz
        :param freq:
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f'FREQ:CENT {freq}GHz')
            time.sleep(0.001)
            logging.info(f'设置中心频率: {freq} GHz')
        else:
            logging.error("请先打开连接")

    def set_freq_span(self, freq: Union[float | int, str]):
        """
        设置频谱的跨度 (span)，单位为 GHz
        :param freq: 可以是浮点数（GHz）或字符串 'max' 表示最大跨度
        :return:
        """
        if self.N9020b:
            if isinstance(freq, float | int):
                self.N9020b.write(f'FREQ:SPAN {freq}GHz; *WAI')  # 设置后使用 *WAI 等待命令执行完成
            elif isinstance(freq, str) and freq.lower() == 'max':
                self.N9020b.write(f'FREQ:SPAN MAX; *WAI')  # 设置后使用 *WAI 等待命令执行完成
            else:
                logging.error(f'无效的频谱跨度值: {freq}')
                return
            time.sleep(0.001)  # 稍作延迟以确保指令被正确执行
            logging.info(f'已设置频谱跨度为: {freq} GHz')
        else:
            logging.error("请先连接仪器")

    def set_freq_start(self, freq: float):
        if self.N9020b:
            self.N9020b.write(f'FREQ:STAR {freq}GHz')
            time.sleep(0.001)
            logging.info(f'设置起始频率: {freq} GHz')
        else:
            logging.error("请先打开连接")

    def set_freq_stop(self, freq: float):
        if self.N9020b:
            self.N9020b.write(f'FREQ:STOP {freq}GHz')
            time.sleep(0.001)
            logging.info(f'设置结束频率: {freq} GHz')
        else:
            logging.error("请先打开连接")

    def set_ref_level(self, level: float):
        """
        设置参考电平 (Reference Level)
        :param level: 参考电平值，单位 dBm
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f'DISP:WIND:TRAC:Y:RLEV {level}dBm')  # 设置参考电平
            time.sleep(0.001)  # 延迟以确保指令执行
            logging.info(f'已设置参考电平为: {level} dBm')
        else:
            logging.error("请先连接仪器")

    def set_rbw(self, rbw: float, unit: str = 'Hz'):
        """
        设置分辨带宽 (Resolution Bandwidth, RBW)
        :param rbw: 分辨带宽值
        :param unit: 带宽的单位，默认是 Hz（可选 kHz, MHz）
        :return:
        """
        valid_units = ['Hz', 'KHz', 'MHz']

        if unit not in valid_units:
            logging.error(f"无效的单位: {unit}. 请选择其中一个: {valid_units}")
            return

        if self.N9020b:
            # 构建 SCPI 命令
            self.N9020b.write(f'BAND:RES {rbw}{unit}; *WAI')  # 设置后使用 *WAI 等待命令执行完成
            logging.info(f'已设置分辨带宽为: {rbw} {unit}')
        else:
            logging.error("请先连接仪器")

    def set_rbw_auto(self):
        if self.N9020b:
            try:
                self.N9020b.write('BAND:RES AUTO; *WAI')  # 设置 RBW 为自动模式并等待
                logging.info('已将分辨率带宽设置为自动模式')
            except Exception as e:
                logging.error(f"设置 RBW 时发生错误: {e}")
        else:
            logging.error("请先连接仪器")

    def set_vbw(self, vbw: float, unit: str = 'Hz'):
        """
        设置视频带宽 (Video Bandwidth, VBW)
        :param vbw: 视频带宽值
        :param unit: 带宽的单位，默认是 Hz（可选 kHz, MHz）
        :return:
        """
        valid_units = ['Hz', 'kHz', 'MHz']

        if unit not in valid_units:
            logging.error(f"无效的单位: {unit}. 请选择其中一个: {valid_units}")
            return

        if self.N9020b:
            try:
                # 构建 SCPI 命令
                self.N9020b.write(f'BAND:VID {vbw}{unit}; *WAI')  # 设置后使用 *WAI 等待命令执行完成
                logging.info(f'已设置视频带宽为: {vbw} {unit}')
            except Exception as e:
                logging.error(f"设置视频带宽时发生错误: {e}")
        else:
            logging.error("请先连接仪器")

    def set_vbw_auto(self):
        if self.N9020b:
            try:
                self.N9020b.write('BAND:VID AUTO; *WAI')  # 设置 VBW 为自动模式并等待
                logging.info('已将视频带宽设置为自动模式')
            except Exception as e:
                logging.error(f"设置 VBW 时发生错误: {e}")
        else:
            logging.error("请先连接仪器")

    def set_peak_search(self):
        """
        peak search
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK1:MAX:PEAK")
            logging.info('执行peak search')
        else:
            logging.error("请先打开连接")

    def set_marker_frequency(self, frequency: float, mark_number: int = 1):
        """
        设置指定mark标记的频率
        :param frequency: 频率值，单位为 Hz
        :param mark_number: 标记编号，默认为 1
        :return:
        """
        if self.N9020b:
            try:
                self.N9020b.write(f'CALC:MARK{mark_number}:FREQ {frequency} Hz; *WAI')  # 设置指定标记的频率并等待
                logging.info(f'已将标记{mark_number}的频率设置为: {frequency} Hz')
            except Exception as e:
                logging.error(f"设置标记{mark_number}频率时发生错误: {e}")
        else:
            logging.error("请先连接仪器")

    def set_mark_del_on(self, x):
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK{x}:MODE DELT")
            logging.info(f'开启delt标记: MARK{x}')
        else:
            logging.error("请先打开连接")

    def set_mark_aoff(self):
        """
        关闭所有mark
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK:AOFF")
            logging.info('关闭所有标记')
        else:
            logging.error("请先打开连接")

    def set_mark_del_freq(self, x: int, freq):
        """
        delt频率，GHz
        :param x:1,2,3
        :param freq:
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK{x}:X {freq}MHz")
            logging.info(f'设置MARK{x}的delt频率为: {freq} MHz')
        else:
            logging.error("请先打开连接")

    def query_mark_delt_x(self, x):
        """
        读取偏移频率
        :return:
        """
        if self.N9020b:
            value = self.N9020b.query(f'CALC:MARK{x}:X?')
            logging.info(f'读取MARK{x}的偏移频率: {value}')
            return value
        else:
            logging.error("请先打开连接")

    def query_mark_x_freq(self):
        """
        读取mark频率,单位GHz
        :return:
        """
        if self.N9020b:
            value = self.N9020b.query(f"CALC:MARK:X?")
            value = float(value.replace("\n", "").replace("\r", "")) / 1e9  # 删除字符串中的换行符和回车符
            logging.info(f'读取MARK频率为:{value} GHz')
            return value
        else:
            logging.error("请先打开连接")

    def query_mark_y_power(self):
        """
        读取mark功率,单位dBm
        :return:
        """
        if self.N9020b:
            value = self.N9020b.query(f"CALC:MARK:Y?")
            value = float(value.replace("\n", "").replace("\r", ""))  # 删除字符串中的换行符和回车符
            logging.info(f'读取MARK频率为:{value} dBm')
            return value
        else:
            logging.error("请先打开连接")

    def set_peak_search_continuous_on(self):
        """
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK:CPS ON")
            logging.info(f'set_peak_search_continuous 成功')
        else:
            logging.error("请先打开连接")

    def set_mark_to_cf(self):
        """
        :return:
        """
        if self.N9020b:
            self.N9020b.write(f"CALC:MARK:CENT")
            logging.info(f'CALC:MARK:CENT 成功')
        else:
            logging.error("请先打开连接")

    def save_png(self, file_addr):
        if self.N9020b:
            self.N9020b.write(f'MMEM:STOR:SCR "F:\\{file_addr}.PNG"')
            logging.info(f'保存屏幕截图到: F:\\{file_addr}.PNG')
        else:
            logging.error("请先打开连接")


if __name__ == '__main__':
    addr = 'USB0::0x2A8D::0x1D0B::MY55480187::INSTR'
    n9020b = N9020b(addr)
    n9020b.open()   # 实例化之后需要手动打开仪器连接(After instantiation, you need to manually open the instrument connection).
    n9020b.set_peak_search_continuous_on()
    freq = n9020b.query_mark_x_freq()
    power = n9020b.query_mark_y_power()
    print(freq,power)
    n9020b.close()


