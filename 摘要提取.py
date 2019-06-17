from pyhanlp import *

TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")

def getSummar(sentence,num):
    return ",".join(HanLP.extractSummary(sentence, num)) + "。"

if __name__ == "__main__":
    document = '''
    宋浩京转达了朝鲜领导人对中国领导人的亲切问候，代表朝方对中国党政领导人和人民哀悼金日成主席逝世表示深切谢意。
         '''
    print(getSummar(document, 3))