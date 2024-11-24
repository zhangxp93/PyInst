"""
@date: 2024-11-24
@author: zhangxp93
@contact: 937097345@qq.com

您可以免费地使用、修改和分发PyInst ，但必须包含原始作者的版权声明和下列许可声明。

You may use, modify, and distribute PyInst free of charge, but you must include
the original author's copyright notice and the following license notice.
"""

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


# 这是一个示例 Python 脚本。
import common
import libs

fswp_addr = 'TCPIP::192.168.1.1::INSTR'
n9020b_addr = 'TCPIP::192.168.1.2::INSTR'

common.setup_logging()


if __name__ == '__main__':
    fswp = libs.Fswp(fswp_addr)
    fswp.close()
    n9020b = libs.N9020b(n9020b_addr)
    n9020b.open()
    n9020b.close()

