java swing 2048小游戏 欢迎来玩

环境1.8jdk

---

## 深度学习练手项目（文本）

从零到一的中文情感分类项目见：[`text_sentiment/`](text_sentiment/README.md)

```bash
cd text_sentiment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/make_sample_data.py
python scripts/train.py
python scripts/infer.py --text "这部电影太好看了"
```
