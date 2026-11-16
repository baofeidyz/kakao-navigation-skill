# Kakao REST API Key 申请与配置教程

**中文** | [English](rest-api-key-setup.en.md) | [한국어](rest-api-key-setup.ko.md)

本教程用于配置本 Skill 所需的 Kakao REST API Key，覆盖 Kakao Local 地点搜索和 Kakao Mobility 汽车路线接口。参考项目 [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server) 提供了早期申请流程；下面以当前 Kakao 官方界面和规则为准。

## 1. 注册并登录 Kakao Developers

1. 打开 [Kakao Developers](https://developers.kakao.com/)。
2. 使用 Kakao 账号登录；没有账号时先注册。
3. 进入应用管理页面。

## 2. 创建应用

1. 在顶部选择“应用（App）”。
2. 选择“创建应用（Create app）”。
3. 填写应用名称、公司或开发者信息等必填内容并保存。

应用创建后通常会自动生成 REST API、JavaScript、Native App 和 Admin 等不同类型的 Key。本 Skill **只使用 REST API Key**，不要误用 JavaScript Key、Native App Key 或 Admin Key。

## 3. 启用 Kakao Map API

地点搜索、地址解析和坐标转换属于 Kakao Map REST API：

1. 打开刚创建的应用。
2. 进入“카카오맵（Kakao Map）→ 사용 설정（使用设置）”。
3. 将状态设置为 `ON`。

从 2026-07-21 起，Kakao Map API 的使用和免费额度规则发生过调整：开发者账号下第一个启用 Kakao Map API 的应用可获得免费额度标识；第二个及之后的应用，或需要超出免费额度时，可能需要连接 Biz Wallet 并启用付费 API。请以控制台显示和 [Kakao Map 官方说明](https://developers.kakao.com/docs/ko/kakaomap/common) 为准。

## 4. 创建或取得 REST API Key

Kakao 在 2025-12-03 调整了应用和密钥菜单。当前路径是：

1. 进入“应用 → 选择应用 → 应用 → 平台密钥（Platform Key）”。
2. 找到已有的 REST API Key，或选择“添加 REST API Key”。
3. 给 Key 设置容易识别的名称，例如 `kakao-navigation-local`。
4. 确认 Key 状态为启用，并复制 REST API Key 的值。

请把 Key 当作凭据处理。不要把它提交到 GitHub、写进 `SKILL.md`、README、源代码或公开的 `.env` 文件。

### Client Secret 说明

新建 REST API Key 时 Client Secret 可能默认启用。Client Secret 主要用于 Kakao 登录等 OAuth Token 请求。本 Skill 调用 Local 和 Directions API 时使用 `Authorization: KakaoAK ...` 头，不要求把 Client Secret 传给脚本，也不要把 Admin Key 当作替代品。

## 5. 配置允许调用的 IP

允许 IP 能降低 Key 泄露后的风险，但配置错误也会让本地 Agent 无法调用 API。

1. 进入“应用 → 平台密钥 → 选择 REST API Key → 调用允许 IP 地址”。
2. 生产服务器建议填写固定出口 IP 或合适的 CIDR。
3. 本地开发环境如果出口 IP 会变化，可以先不配置，确认调用成功后再逐步收紧。
4. 保存设置。

Kakao 当前最多允许为一个 Key 登记 10 项，并支持 IPv4、CIDR 或 Subnet Mask。配置后，只有登记来源可以调用。若收到 `ip mismatched` 或 `-401`，请检查实际出口 IP，或暂时清空错误的允许 IP 配置后重新验证。

## 6. 确认 Kakao Mobility Directions 权限

汽车路线接口使用同一个 Kakao Developers REST API Key，请查看 [Kakao Mobility Directions 入门文档](https://developers.kakaomobility.com/guide/navi-api/start)及账号控制台中的价格、额度和服务状态。

不要使用旧 IP、固定解析结果或自定义 hosts 映射；始终调用官方域名：

```text
https://apis-navi.kakaomobility.com
```

Kakao Mobility 的公开 Directions REST API 提供汽车路线，不代表已经获得步行或公交路线能力。

## 7. 在本地安全配置 Key

仅在当前终端临时配置：

```bash
export KAKAO_REST_API_KEY='复制的 REST API Key'
```

确认变量是否存在时不要打印完整值：

```bash
test -n "$KAKAO_REST_API_KEY" && echo 'KAKAO_REST_API_KEY is set'
```

需要长期配置时，使用操作系统的密钥链、CI Secret 或受权限保护的环境配置。不要提交 `.env`；本仓库已经在 `.gitignore` 中忽略它。

## 8. 验证地点搜索

在 Skill 根目录运行：

```bash
python3 scripts/kakao_api.py keyword '경복궁' --size 3
```

成功时会返回 `documents`，其中包含 `place_name`、地址、`x`（经度）、`y`（纬度）和 Kakao Place URL。

也可以先做不联网的请求检查：

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

## 9. 验证汽车路线

使用地点搜索返回的坐标，注意顺序始终是 `经度,纬度`：

```bash
python3 scripts/kakao_api.py directions \
  --origin 126.97689786832184,37.577613288258206 \
  --destination 127.027619208212,37.497952760023 \
  --priority RECOMMEND \
  --summary true
```

成功时应在 `routes` 中看到 `result_code: 0` 和 `길찾기 성공`，并获得米、秒、出租车费和过路费等摘要。实际时间受实时交通和请求时间影响。

## 常见问题

| 现象 | 检查项 |
|---|---|
| `KAKAO_REST_API_KEY is not set` | 当前终端没有导出环境变量 |
| HTTP `401` / Kakao `-401` | Key 类型错误、Key 已停用、允许 IP 不匹配或复制错误 |
| `appKeyType is ADMIN_KEY` | 错用了 Admin Key，应改用 REST API Key |
| Local API 返回权限或产品错误 | 检查 Kakao Map 使用状态、Biz Wallet/付费设置及当前额度 |
| `429` | 已触发速率或配额限制，停止重试并检查控制台 |
| 地点搜索成功、路线失败 | 分别检查 Kakao Map 与 Kakao Mobility 的产品状态、额度和请求参数 |
| 搜索结果为空 | 改用韩文地点名、移除过小半径，或补充行政区信息 |

## 安全收尾

- Key 一旦出现在聊天记录、截图、公开日志或 Git 历史中，应立即在“平台密钥”中轮换。
- 不要把 Key 作为 URL 查询参数；本 Skill 只通过 `Authorization` 请求头发送。
- 对生产环境配置允许 IP，并定期检查配额和异常调用。
- 不要在来自不受信任 Pull Request 的 CI 中暴露 Secret。

## 官方文档

- [Kakao REST API 入门](https://developers.kakao.com/docs/ko/rest-api/getting-started)
- [应用和 REST API Key 设置](https://developers.kakao.com/docs/ko/app-setting/app)
- [Kakao Map 使用说明](https://developers.kakao.com/docs/ko/kakaomap/common)
- [2025 应用和密钥菜单变更](https://developers.kakao.com/docs/ko/getting-started/app-key-migration)
- [Kakao Mobility Directions 入门](https://developers.kakaomobility.com/guide/navi-api/start)
