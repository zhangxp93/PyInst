# 这是一个示例 Python 脚本。
import common
import libs

fswp_addr = 'TCPIP::192.168.1.1::INSTR'

common.setup_logging()


if __name__ == '__main__':
    fswp = libs.Fswp(fswp_addr)

