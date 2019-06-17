from pyhanlp import *
from Tools import *

# 标准分词
BasicTokenizer = JClass("com.hankcs.hanlp.tokenizer.BasicTokenizer")
# 单独词性获取
CRFnewSegment = HanLP.newSegment("crf")
# NLP分词，更精准的中文分词、词性标注与命名实体识别
NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")

# 开启词性显示
HanLP.Config.ShowTermNature = True

# 标准分词
def BasicTokenizerSeg(text):
    WordSegment = BasicTokenizer.segment(text)
    # print([str(word.word) for word in WordSegment.iterator()])  # 打印分词列表
    # print([AttributeMatch[str(word.nature)] for word in WordSegment.iterator()])  # 打印中文词性
    # print([str(word.nature) for word in WordSegment.iterator()])  # 打印词性
    return WordSegment

# 单独词性获取
def CRFTokenizerSeg(text):
    WordSegment = CRFnewSegment.seg(text)
    # print([str(word.word) for word in WordSegment.iterator()])  # 打印分词列表
    # print([AttributeMatch[str(word.nature)] for word in WordSegment.iterator()])  # 打印中文词性
    # print([str(word.nature) for word in WordSegment.iterator()])  # 打印词性
    return WordSegment

def NLPTokenizerSeg(text):
    WordSegment = NLPTokenizer.segment(text)
    # print([str(word.word) for word in WordSegment.iterator()])  # 打印分词列表
    # print([AttributeMatch[str(word.nature)] for word in WordSegment.iterator()])  # 打印中文词性
    # print([str(word.nature) for word in WordSegment.iterator()])  # 打印词性
    return WordSegment

if __name__ == "__main__":
    for sentence in Question:
        sentence_seg = NLPTokenizerSeg(sentence)
        # print([str(word.word) for word in sentence_seg.iterator()])  # 打印词性
        print([AttributeMatch[(str(word.nature)).lower()] for word in sentence_seg.iterator()])  # 打印词性