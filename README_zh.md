# 海信空调 Home Assistant 集成

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[English](README.md) | **中文**

这是海信智能家电设备的官方 Home Assistant 核心集成，通过 ConnectLife 云服务提供支持。

## 功能特性

- 🌡️ **气候控制**：完整的空调控制（温度、模式、风速、摆风）
- 💧 **湿度管理**：除湿机和加湿器控制
- 🔥 **热水系统**：热泵和热水器管理
- 📊 **实时监控**：温度、湿度和能耗传感器
- 🏠 **分区控制**：兼容系统的多区域气候管理
- ⚡ **能耗追踪**：每日能耗监控
- 🔧 **故障检测**：实时错误代码监控和警报

## 支持设备


| 设备类型       | 型号         | 功能                   |
| ---------------- | -------------- | ------------------------ |
| **分体式空调** | 009-199 系列 | 完整气候控制，能耗监控 |
| **窗式空调**   | 008-399 系列 | 气候控制，基础传感器   |
| **移动空调**   | 006-299 系列 | 气候控制，移动功能     |
| **除湿机**     | 007 系列     | 湿度控制，风速管理     |
| **热泵**       | 035-699 系列 | 制热/制冷，热水        |
| **风管机系统** | 多种型号     | 分区控制，高级气候管理 |

## 安装

### 前置条件

- Home Assistant 2023.1.0 或更高版本
- 已注册设备的 ConnectLife 账户
- 用于云 API 访问的活跃网络连接

### 安装方法（核心集成）

此集成作为 Home Assistant 的核心集成提供。安装方法：

1. 转到 **设置** → **设备与服务**
2. 点击 **添加集成**
3. 搜索 "Hisense ConnectLife"
4. 按照配置步骤操作

### 方法 2：手动安装

1. 从 [GitHub releases][releases] 下载最新版本
2. 解压归档文件
3. 将 `custom_components/hisense_ac_plugin` 文件夹复制到您的 Home Assistant `custom_components` 目录
4. 重启 Home Assistant

## 配置

### 步骤 1：网络配置（Windows 用户）

为了正确的 OAuth2 认证，您需要配置本地 DNS 解析：

1. 导航到 `C:\Windows\System32\drivers\etc\`
2. 右键点击 `hosts` 文件并选择"编辑"
3. 添加以下行：
   ```
   127.0.0.1 homeassistant.local
   ```
4. 保存文件

**注意**：此步骤是设置过程中 OAuth2 重定向正常工作所必需的。

### 步骤 2：添加集成

1. 转到 **设置** → **设备与服务**
2. 点击 **添加集成**
3. 搜索 "Hisense Air Conditioner"
4. 按照配置流程操作

### 步骤 3：身份验证

1. 输入您的 ConnectLife 账户凭据
2. 完成 OAuth2 授权过程
3. 等待设备发现完成

**重要提示**：

- 设置期间请禁用 VPN/代理服务
- 确保您的 ConnectLife 账户已注册设备
- 初始同步可能需要 1-2 分钟

## 使用方法

### 气候控制

集成为每个空调设备创建气候实体：

```yaml
# 自动化示例
automation:
  - alias: "夜间降温"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: climate.set_temperature
      target:
        entity_id: climate.living_room_ac
      data:
        temperature: 24
        hvac_mode: cool
```

### 能耗监控

自动创建能耗传感器：

- `sensor.{设备名称}_daily_energy`：每日能耗（kWh）
- `sensor.{设备名称}_power`：当前功耗（W）

### 分区控制

对于多区域系统，创建独立的区域开关：

- `switch.{设备名称}_zone_1`：区域 1 控制
- `switch.{设备名称}_zone_2`：区域 2 控制

## 实体类型


| 平台             | 描述             | 示例实体                           |
| ------------------ | ------------------ | ------------------------------------ |
| **Climate**      | 空调设备，热泵   | `climate.living_room_ac`           |
| **Sensor**       | 温度，湿度，能耗 | `sensor.bedroom_temperature`       |
| **Switch**       | 区域，特殊功能   | `switch.turbo_mode`                |
| **Number**       | 目标值，设置     | `number.display_brightness`        |
| **Humidifier**   | 除湿机控制       | `humidifier.basement_dehumidifier` |
| **Water Heater** | 热水系统         | `water_heater.main_unit`           |

## 故障排除

### 常见问题

#### 认证失败

**症状**：登录失败或显示"凭据无效"
**解决方案**：

- 验证您的 ConnectLife 用户名和密码
- 设置期间暂时禁用双因子认证
- 尝试登录 ConnectLife 应用以验证凭据

#### 设备未找到

**症状**：设置后没有设备出现
**解决方案**：

- 在 ConnectLife 应用中验证设备在线
- 检查网络连接
- 从 **设置** → **设备与服务** 重启集成

#### OAuth2 重定向错误

**症状**：登录后显示"页面未找到"
**解决方案**：

- 确保 hosts 文件修改已正确完成
- 重启浏览器
- 禁用 VPN/代理服务

#### 连接超时

**症状**：集成显示"不可用"状态
**解决方案**：

- 检查 Home Assistant 日志获取具体错误信息
- 验证 ConnectLife 服务状态
- 重启 Home Assistant

### 调试日志

要启用调试日志，请将以下内容添加到您的 `configuration.yaml`：

```yaml
logger:
  default: warning
  logs:
    custom_components.hisense_ac_plugin: debug
```

### 获得帮助

1. 查看 [故障排除 Wiki][wiki]
2. 搜索现有的 [GitHub Issues][issues]
3. 创建新问题时请包含：
   - Home Assistant 版本
   - 集成版本
   - 设备型号
   - 错误日志（删除敏感数据）

## 贡献

欢迎贡献！请在提交 pull request 之前阅读我们的 [贡献指南](CONTRIBUTING.md)。

### 开发环境设置

```bash
git clone https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration.git
cd HomeAssistantPluginIntegration
# 设置您的开发环境
```

## 许可证

此项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

## 免责声明

此集成非海信官方产品。它使用 ConnectLife 云 API 进行设备通信。使用风险自负。

## 支持

- ⭐ 如果您觉得有用，请为此仓库加星
- 🐛 通过 [GitHub Issues][issues] 报告错误
- 💡 通过 [GitHub Discussions][discussions] 请求功能

---

**❤️ 为 Home Assistant 社区制作**

[releases-shield]: https://img.shields.io/github/release/Connectlife-LLC/HomeAssistantPluginIntegration.svg?style=for-the-badge
[releases]: https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/Connectlife-LLC/HomeAssistantPluginIntegration.svg?style=for-the-badge
[commits]: https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration/commits/main
[license-shield]: https://img.shields.io/github/license/Connectlife-LLC/HomeAssistantPluginIntegration.svg?style=for-the-badge
[issues]: https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration/issues
[discussions]: https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration/discussions
[wiki]: https://github.com/Connectlife-LLC/HomeAssistantPluginIntegration/wiki
