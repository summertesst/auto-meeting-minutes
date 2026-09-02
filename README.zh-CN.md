# 自动会议纪要

[English](README.md)

用于在 Windows 本地捕获 Microsoft Teams 实时字幕、生成会议纪要草稿，并在本地浏览会议归档的工具。

> **隐私优先：** 此仓库不包含任何真实字幕、会议纪要、参会人员信息、组织信息、凭据或生成后的归档数据。使用前请阅读 [PRIVACY.md](PRIVACY.md)。

## 功能流程

```text
Teams 实时字幕窗口
        |
        v
Windows UI Automation 字幕采集
        |
        v
本地字幕文件 (.txt)
        |
        +--> 纪要草稿和本地归档网站
        |
        +--> 可选的 Copilot 语义任务确认
```

守护程序检测 Teams 实时字幕窗口，通过 Windows UI Automation 读取可访问文本，并写入带时间戳的本地字幕文件。会议结束后，程序生成会议纪要草稿并刷新本地归档。

行动项不通过正则表达式自动猜测；它需要基于完整上下文进行人工或 AI 语义复核。

## 环境要求

- Windows 10/11
- 推荐 Python 3.9 或更新版本
- 已启用实时字幕功能的 Microsoft Teams
- 已获得参会人和所在组织对于字幕采集/处理的必要许可

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

## 快速开始

1. 将 `config.example.py` 复制为 `scripts\config.py`，并按需要修改配置。
2. 创建本地运行目录：

   ```powershell
   New-Item -ItemType Directory -Force output\transcripts, output\summaries, site\pages
   ```

3. 启动字幕守护程序：

   ```powershell
   python scripts\caption_daemon.py
   ```

4. 在 Teams 会议中开启实时字幕。字幕和草稿会仅保存在本地 `output\` 目录。
5. 会后用语义任务确认流程审核行动项，然后构建归档站点：

   ```powershell
   python scripts\build_meeting_site.py
   Start-Process site\index.html
   ```

## 项目结构

| 路径 | 用途 |
|---|---|
| `scripts\capture_core.py` | 读取 Teams 实时字幕的辅助功能树。 |
| `scripts\caption_daemon.py` | 系统托盘守护程序；检测会议并协调采集。 |
| `scripts\summary_generator.py` | 生成结构化的会议纪要**草稿**。 |
| `scripts\build_meeting_site.py` | 从本地纪要构建本地归档网站。 |
| `scripts\watchdog_restart.py` | 可选的守护程序重启脚本。 |
| `skills\semantic-task-confirmation\SKILL.md` | PMO 风格的语义行动项复核规则。 |
| `site\` | 空白静态本地归档页面。 |
| `examples\` | 完全虚构的示例输入和输出。 |
| `docs\` | 架构、流程和使用说明。 |

## 语义任务确认

`semantic-task-confirmation` skill 使用七阶段流程确认行动项：

1. 准备并标准化原始字幕。
2. 判断发言意图。
3. 提取候选未来行动。
4. 验证负责人。
5. 验证行动和交付物。
6. 验证截止时间和议题。
7. 去重，并归类为 `confirmed`、`possible` 或 `rejected`。

一条 confirmed 任务必须包含明确负责人、未来行动、可验证交付物、来源证据和议题。未明确截止时间时记录为 `TBD`，不会因此自动拒绝。个人任务列表只包含明确分配给该用户的事项。

## 空白网站

`site\index.html` 是安全的空白本地归档页面，不会加载任何会议数据。执行 `build_meeting_site.py` 后会在本地生成 `site\data.js` 和 `site\pages\`；这些文件已被 `.gitignore` 排除，绝不能提交。

## 发布前检查

发布 fork 或二次开发版本前，请检查：

```powershell
git ls-files
git grep -inE "password|token|secret|@|C:\\Users|transcript|meeting minutes"
```

请人工复查结果。姓名、日期、项目名称、文件名和会议内容即使不匹配上述关键词，也可能属于敏感信息。

## 许可证

本项目使用 [MIT License](LICENSE)。
