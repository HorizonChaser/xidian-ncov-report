# 用 Github Action 实现自动填报

## 停用方法

~~我写到最开头就应该不会有看不到的人了吧...~~

- 从 GitHub 上直接删除这个仓库 (最直接)
- 或者在仓库根目录下新建一个名为 `NOSUBMIT` 的文件

## 食用方法

### 对于疫情通

0. 本地安装好 Python 环境与**依赖** (大概也就一个 `requests`)
1. fork 这个仓库, 然后下载到本地
2. 在命令行中切换到这个仓库, 比如 `cd "xidian-ncov-report"`
3. 运行 `dump_geo.py`, 比如 `python dump_geo.py`, 之后按要求输入, 得到位置信息, 复制下来
   - 注意, 按学校要求, 您应当每天都更新您的位置信息
   - 开发者不对您因未及时更新信息导致的任何问题负责
4. 在本仓库的 Settings - Secrets 中, 新增以下四个 Secret:
   - `GEO_INFO`: 必须项, 在第 3 步中保存的位置信息
   - `USERNAME`: 必须项, 统一身份认证账号
   - `PSWD`: 必须项, 统一身份认证密码
   - `SCKEY`: 必须项, [Server 酱](https://sct.ftqq.com) 的推送 key, 用于实现微信推送
     - 要是不需要的话这一项的内容可以填aaa
5. 在 `./.github/workflows/daliy-commit.yaml` 中
   - 合理设置第 5 行的 cron 表达式, 例如 `5 0 * * *`
   - 把最后一行的 `submit_3chk.py` 改成 `submit.py`
6. 没了, 建议从 Actions 中手动运行一次看看成不成功

### 对于晨午晚检

0. 在本仓库的 Settings - Secrets 中, 新增以下四个 Secret:
   - `GEO_INFO`: 必须项, 在第 3 步中保存的位置信息
   - `USERNAME`: 必须项, 统一身份认证账号
   - `PSWD`: 必须项, 统一身份认证密码
   - `SCKEY`: 必须项, [Server 酱](https://sct.ftqq.com) 的推送 key, 用于实现微信推送
     - 要是不需要的话这一项的内容可以填aaa
1. 没了, 建议从 Actions 中手动运行一次看看成不成功

---

以下来自原开发者 Apache553 的 `readme.md`, 操作方法已经不同

---

# 疫情通

先使用configure.py设置需要填报的信息
然后使用submit.py提交

定位信息可通过在configure时填在国外来跳过
然后使用submit.py dump_geo来取得定位信息(不会提交)
然后再重新configure

# 晨午检

先使用configure_3chk.py设置需要填报的信息
然后使用submit_3chk.py提交

注意在对应的时间段进行提交

# 另外的取得定位信息的方式
访问https://blog.apache553.com/location.html
大概不会好使，手机使用需给予定位权限
