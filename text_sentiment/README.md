# 从零到一：中文文本情感分类（PyTorch）

一个可跑通的深度学习练手项目：输入一句中文评论，预测 **正面 / 负面**。

适合路径：

1. 跑通训练与推理  
2. 读懂数据 → 词表 → 模型 → 训练循环  
3. 自己改模型 / 超参 / 数据集做对比实验  

---

## 你将学到什么

| 模块 | 内容 |
|------|------|
| 数据 | CSV 标注、train/val 划分、按字分词 |
| 词表 | `<pad>` / `<unk>`、文本编码 |
| 模型 | TextCNN、BiLSTM |
| 训练 | loss、准确率、F1、早停、checkpoint |
| 推理 | 加载最优模型，预测单句情感 |

---

## 环境准备

```bash
cd text_sentiment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

生成（或重新生成）示例数据：

```bash
python scripts/make_sample_data.py
```

---

## 三步跑通

### 1) 训练

```bash
python scripts/train.py --config configs/train.yaml
```

换 BiLSTM：

```bash
python scripts/train.py --model bilstm
```

### 2) 推理

```bash
python scripts/infer.py --text "这部电影太好看了，强烈推荐"
python scripts/infer.py --text "质量太差，完全不推荐"
```

### 3) 看结果

- 最优模型：`checkpoints/best_model.pt`
- 词表：`checkpoints/vocab.json`
- 训练曲线数据：`checkpoints/history.json`

---

## 项目结构

```text
text_sentiment/
├── configs/train.yaml          # 超参配置（优先改这里）
├── data/sample/                # 入门示例数据
├── scripts/
│   ├── make_sample_data.py     # 生成样本
│   ├── train.py                # 训练入口
│   └── infer.py                # 推理入口
├── src/
│   ├── datasets/               # Dataset / Vocab
│   ├── models/                 # TextCNN / BiLSTM
│   ├── trainers/               # 训练与验证
│   └── utils/                  # 配置、随机种子
└── checkpoints/                # 训练产出
```

---

## 建议练习顺序（从零到一）

### Level 1：跑通
- 按上面命令训练 + 推理
- 观察 `val_acc` / `val_f1` 是否上升

### Level 2：读代码
1. `src/datasets/vocab.py`：文本怎么变成数字  
2. `src/models/textcnn.py`：卷积如何抓局部短语特征  
3. `src/trainers/trainer.py`：一个 epoch 里发生了什么  

### Level 3：动手改
- 把 `model.name` 从 `textcnn` 换成 `bilstm`，对比 F1  
- 改 `lr`、`embed_dim`、`max_len`，每次只改一个变量  
- 在 `data/sample/train.csv` 里加 20 条你自己的评论再训练  

### Level 4：进阶挑战
- 接入真实公开数据（如微博情感 / ChnSentiCorp）  
- 加 `tensorboard` 画 loss 曲线  
- 换成预训练模型（如 `bert-base-chinese`）做迁移学习  

---

## 数据格式

CSV 两列：

```csv
text,label
这部电影太好看了,1
质量太差不推荐,0
```

- `label=1`：正面  
- `label=0`：负面  

---

## 常见问题

**Q: 为什么默认按字切分？**  
中文入门不依赖 `jieba` 等分词库，稳定好懂；英文可把配置改成 `tokenize: word`。

**Q: 样本很少，准确率波动大正常吗？**  
正常。示例数据用于学会流程；要冲高分请换更大真实数据集。

**Q: 没有 GPU 能跑吗？**  
可以，配置里 `device: auto` 会自动用 CPU。
