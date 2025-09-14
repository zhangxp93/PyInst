# 分支使用说明

点击后续列表的版本号链接，可前往对应备份分支页面。

部分备份分支含有体积较大的二进制库，会让你花费长时间下载。因此，建议只下载你需要用的分支。

方法1：将所需的分支，fork到你自己的账号下，然后clone你自己仓库。

方法2：使用以下命令手动clone指定分支：

```
git clone --single-branch --branch [分支名] https://github.com/zhangxp93/PyInst.git
```

方法3：在本仓库手动下载指定分支的zip源码包。

`[分支名]` 可以是 `main` 、`release/1.0.0` 等，详见下方列表。

`main`、`dev` 等分支，可能含有开发中的不稳定的新功能。如果用于研究学习或二次开发，建议选择 `release` 开头的分支。

# 更新日志 CHANGE LOG

### [release/v0.0.1](https://github.com/zhangxp93/PyInst.git) `2025.09.14`
- 项目第一个版本发布
- 支持基于 PyVISA 的仪器控制
- 实现对 Keysight 和 Rohde & Schwarz 仪器的 SCPI 命令控制
- 支持多种连接方式（USB、GPIB、TCP/IP）

### [main](https://github.com/zhangxp93/PyInst.git) `2024.11.24`
- "梦开始的地方"