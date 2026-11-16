# Kakao Navigation Skill

**中文** | [English](README.en.md) | [한국어](README.ko.md)

这是一个面向 AI Agent 的韩国地点检索与汽车路线规划 Skill，基于 Kakao Local 和 Kakao Mobility 官方 REST API。

它能帮助 Agent 准确识别韩国地点、区分同名地点和连锁店分店、解析地址、检索周边设施、比较驾车时间、规划多站路线并查询未来出发时间，避免凭空猜测坐标或把汽车路线误当成步行、公交路线。

## 让 AI Agent 安装

直接把仓库地址交给支持 Skill 的 Agent，例如：

```text
帮我安装这个 skill：https://github.com/baofeidyz/kakao-navigation-skill
```

```text
Install this skill: https://github.com/baofeidyz/kakao-navigation-skill
```

### 给 AI Agent 的安装说明

当用户要求把本仓库安装为 Skill 时：

1. 仓库根目录就是 Skill 目录，因为根目录包含 `SKILL.md`。
2. 将它以 `kakao-navigation` 的名称安装到当前 Agent 的标准 Skills 目录。
3. 不要复制 `.git`、本地缓存、`.env` 或任何凭据。
4. 告知用户需要单独配置 `KAKAO_REST_API_KEY`；根据宿主 Agent 的机制，新 Skill 通常在下一轮对话或重启后生效。
5. 不要要求用户把 REST API Key 提交到仓库。

使用 Codex 内置 Skill Installer 时，等价的确定性命令是：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo baofeidyz/kakao-navigation-skill \
  --path . \
  --name kakao-navigation
```

如果目标目录已经存在，安装器会停止而不是覆盖已有 Skill。更新或移除旧版本应由用户明确执行。

### 手动安装

```bash
git clone https://github.com/baofeidyz/kakao-navigation-skill.git
mkdir -p ~/.codex/skills
rsync -a --exclude .git kakao-navigation-skill/ ~/.codex/skills/kakao-navigation/
```

安装后重启 Agent，或开始新一轮对话，让 Agent 重新发现 Skill。

## 配置 Kakao API

请按照 [Kakao REST API Key 申请与配置教程](docs/rest-api-key-setup.md) 完成账号、应用、Kakao Map API、REST API Key、允许 IP 和调用验证配置。教程已根据 Kakao 2025 年应用密钥菜单改版及 2026 年 Map API 额度规则更新。

配置完成后，只通过运行环境注入密钥：

```bash
export KAKAO_REST_API_KEY='your-rest-api-key'
```

不要把密钥放进提示词、截图、Shell 历史、提交到 Git 的 `.env` 或示例命令中。如果密钥已经暴露，请立即在 Kakao Developers 中轮换。

## 支持能力

- 关键词地点搜索和分类周边搜索
- 地址正向解析与坐标反向解析
- 行政区查询和坐标系转换
- 最多包含 5 个经停点的当前汽车路线
- 指定未来出发时间的汽车路线
- 多经停点、多起点和多目的地路线请求
- 将 Kakao API 证据与行程规划推断明确分开的旅游规划方法

这里使用的 Kakao 公开 REST API **不提供步行或公共交通路线**。Skill 不会把汽车预计时间标记为步行、地铁或公交结果。

## CLI 示例

在安装后的 Skill 目录执行：

```bash
python3 scripts/kakao_api.py keyword '경복궁' --size 3

python3 scripts/kakao_api.py category FD6 \
  --x 126.97689786832184 \
  --y 37.577613288258206 \
  --radius 1500 \
  --sort distance

python3 scripts/kakao_api.py directions \
  --origin 126.97689786832184,37.577613288258206 \
  --destination 127.027619208212,37.497952760023 \
  --priority RECOMMEND \
  --summary true
```

无需密钥或网络即可检查请求构造：

```bash
python3 scripts/kakao_api.py --dry-run keyword '경복궁 맛집' \
  --x 126.9769 --y 37.5776 --radius 1500 --sort distance
```

查看全部参数：

```bash
python3 scripts/kakao_api.py --help
python3 scripts/kakao_api.py directions --help
```

## 仓库结构

```text
.
├── SKILL.md                    Agent 入口与决策规则
├── agents/openai.yaml          Skill 界面元数据
├── docs/                       REST API Key 三语申请教程
├── references/
│   ├── local-api.md            Kakao Local API 参考
│   ├── navigation-api.md       Kakao Mobility 路线 API 参考
│   └── travel-planning.md      基于证据的行程规划规则
└── scripts/
    ├── kakao_api.py            无第三方依赖的 REST CLI
    └── test_kakao_api.py       请求构造测试
```

## 发布前验证

CLI 只使用 Python 标准库：

```bash
python3 -m unittest -v scripts/test_kakao_api.py
python3 -m py_compile scripts/kakao_api.py scripts/test_kakao_api.py
python3 scripts/kakao_api.py --dry-run keyword '경복궁'
```

如果已经安装 Codex `skill-creator`，还可以执行：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

真实 API 测试需要 `KAKAO_REST_API_KEY`，并可能消耗账户额度。不要在不受信任的 Pull Request CI 环境中运行真实接口测试。

## 官方资料与维护

- [Kakao Local REST API](https://developers.kakao.com/docs/latest/ko/local/dev-guide)
- [Kakao Mobility 路线 API](https://developers.kakaomobility.com/guide/navi-api/start)
- [汽车路线](https://developers.kakaomobility.com/guide/navi-api/directions)
- [未来汽车路线](https://developers.kakaomobility.com/guide/navi-api/future)

修改接口域名、请求字段、数量限制或鉴权规则前，应重新核对官方文档。较早的 [`CaChiJ/kakao-navigation-mcp-server`](https://github.com/CaChiJ/kakao-navigation-mcp-server) 为初始使用场景提供了参考，但本 Skill 没有继承其中未经实际接口支持的“步行路线”描述。

## 开源协议

[MIT](LICENSE)
