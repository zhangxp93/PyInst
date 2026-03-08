---
name: PyInst Instrument Control
description: 使用PyInst项目控制和通信连接的测试仪器（如频谱仪、信号源等），支持SCPI指令的发送和查询。
---

# PyInst 仪器控制技能 (PyInst Instrument Control)

## 1. 技能概述
本技能用于指导 Agent 如何在 `PyInst` 项目中对硬件测试仪器（如 Rohde & Schwarz FSWP、Keysight N9020B 等）进行自动化操作与控制。该项目基于 `pyvisa`，支持通过 TCP/IP、USB、GPIB 等方式与仪器进行 SCPI 指令交互。

## 2. 核心模块与文件结构
- **入口点**: `main.py`
- **配置文件**: `.yaml` 或 `.json`（用于存储仪器地址等，默认读取 `config.yaml` 或者可以直接传入地址字符串）
- **基类模块**: `libs.baseinstrument.BaseInstrument` (提供了 `write()`, `query()`, `wait_opc()`, `close()` 等基础及包装后的功能)
- **具体设备驱动**:
  - `libs.rs.*`: 包含 R&S 系列仪器（如 `Fswp` 等）
  - `libs.keysight.*`: 包含 Keysight 系列仪器（如 `N9020b` 等）

## 3. 标准操作流程

### 3.1 引入并初始化仪器
通过类的实例化并传入仪器的连接地址（例如 IP 地址或 VISA 资源字符串），可以自动建立连接。
```python
import libs

# 定义仪器地址（TCP/IP示例）
fswp_addr = 'TCPIP::192.168.1.1::INSTR'

# 实例化并连接仪器
fswp = libs.Fswp(fswp_addr)
```

### 3.2 发送指令与查询
继承自 `BaseInstrument` 的设备实例提供了以下便捷方法：
- **写入无需返回的指令 (`write`)**:
  ```python
  # check_complete=True 时会等待指令完全执行完毕 (*OPC?)
  fswp.write('SENSE1:FREQ:CENT 1GHz', check_complete=True)
  ```
- **写入并等待返回结果 (`query`)**:
  ```python
  idn = fswp.query('*IDN?')
  print(f"仪器的ID为: {idn}")
  ```

### 3.3 等待动作完成 (OPC)
- 如果仪器需要执行耗时操作，可以通过 `wait_opc(timeout=10)` 定期轮询仪器完成状态。
- 也可以通过 `set_opc_timeout(timeout=10, poll_interval=0.5)` 临时修改查询超时参数。

### 3.4 关闭连接
完成自动化测试或指令交互后，请务必关闭连接以释放 Visa 资源：
```python
fswp.close()
```

## 4. 最佳实践与注意事项
1. **指令异常处理**: 基本底层方法都带有 `@handle_instrument_error` 装饰器，遇到超时或通信错误会自动重试或记录 Log。业务逻辑若需要进行复杂的容错，需额外捕获 `pyvisa.VisaIOError`。
2. **连接保护**: 为确保操作的健壮性，建议确保 `close()` 总是被调用，或者在后续版本中使用上下文管理器。
3. **查阅文档**: 若遇到无法识别的指令，请优先核查具体的仪器厂家编程手册（SCPI Programmer Manual）。
4. **更新日志策略 (🔥重要)**: **每次完成代码修改、Bug 修复或新增功能后，都必须主动且同步地在项目根目录的 `CHANGELOG.md` 中记录本次的变更。** 必须确保每次改动对项目历史清晰可见。
