# 英语复习

手机上复习英语说法的网页：先看中文、自己说出英文，再看答案、听发音，按「忘了 / 模糊 / 记得」安排下次复习。

- 卡片在 `cards.json`，每课由老师（Claude）挑好后加入。
- 复习进度只存在各自设备的浏览器里。
- 复习间隔：记得 1、3、7、14、30、60、120、240、365 天；连续记对 9 次即「毕业」，不再出现。模糊明天再来，忘了本轮再来一次。
- 每天最多复习 50 张，超出的留到明天；漏掉的日子不会攒成一大堆。
- 每课平均挑 3 张，特别有用的课最多 5 张。

## 发音

每张卡的 `audio` 是用 Kokoro（af_heart 声音）离线生成的录音，网页优先播放它，没有时才用设备自带语音。

生成方法（在装有 KokoroTTS.app 和 mLearn 的 Mac 上，完全离线）：

1. `tools/convert.py tools/kokoro-v1_0.pth`：把 KokoroTTS.app 自带的模型转换成 Python 可用的格式（只需一次，文件不入库）。
2. `tools/speak.py audio af_heart "<id>=<英文句子>" ...`：生成 `audio/<id>.m4a`。

两个脚本都用 mLearn 的 Python 环境运行：`~/Library/Application Support/mlearn/env/bin/python`，并设置 `HF_HUB_OFFLINE=1`。
