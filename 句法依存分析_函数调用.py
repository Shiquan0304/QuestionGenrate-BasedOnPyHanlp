#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from pyhanlp import *
CRFnewSegment = HanLP.newSegment("crf")
CoreStopWordDictionary = JClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
StandardTokenizer = JClass("com.hankcs.hanlp.tokenizer.StandardTokenizer")
Segment = JClass("com.hankcs.hanlp.seg.Segment")
Term = JClass("com.hankcs.hanlp.seg.common.Term")
URLTokenizer = SafeJClass("com.hankcs.hanlp.tokenizer.URLTokenizer")
TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")

StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
HanLP.Config.ShowTermNature = True  # False


sentences = [
    "宋浩京转达了朝鲜领导人对中国领导人的亲切问候，代表朝方对中国党政领导人和人民哀悼金日成主席逝世表示深切谢意。"
]



# 获得无标点符号的分词
def get_no_token_sentence(senten):
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    result_list = re.split(pattern, senten)
    return [x for x in result_list if x != '']

# 去除停词
def remove_stop_word(senten):
    # 使用停用词的简单例子
    # term_list = CRFnewSegment.seg(sentence)
    term_list = HanLP.segment(senten)
    CoreStopWordDictionary.apply(term_list)
    print(term_list)
    print([i.word for i in term_list])
    return [i.word for i in term_list]

# 关键词获取
def get_keyword(senten):
    keyword_list = HanLP.extractKeyword(senten, 5)
    # print(keyword_list)
    return keyword_list

# 抽取数目
def extract_number(senten):
    sen = StandardTokenizer.segment(senten)
    return ([i.word for i in sen.iterator() if (str(i.nature) == 'mq')])

# 命名实体识别
def name_recognition(senten):
    segment = HanLP.newSegment().enableNameRecognize(True).enableTranslatedNameRecognize(True).enableJapaneseNameRecognize(True);
    term_list = segment.seg(senten)
    # print(term_list)
    return ([i.word for i in term_list if(str(i.nature) in ["nr","rr","nrf","nrj"] )])

# 机构识别
def institution_recognition(senten):
    segment = HanLP.newSegment().enableOrganizationRecognize(True)
    term_list = segment.seg(senten)
    print(term_list)
    return ([i.word for i in term_list if(str(i.nature) in ["nt"] )])

# 地点识别
def place_recognition(senten):
    segment = HanLP.newSegment().enablePlaceRecognize(True)
    term_list = segment.seg(sentence)
    print(term_list)
    return ([i.word for i in term_list if(str(i.nature) in ["ns"] )])

# Url识别
def url_recognition(senten):
    term_list = URLTokenizer.segment(senten)
    # print(term_list)
    return ([i.word for i in term_list if(str(i.nature) == "xu")])

def analyse_sentence(input_sentence):
    # 设置
    segment = HanLP.newSegment().\
        enableNameRecognize(True).\
        enableTranslatedNameRecognize(True).\
        enableJapaneseNameRecognize(True).\
        enableOrganizationRecognize(True).\
        enablePlaceRecognize(True)

    # 主要分词
    term_list = segment.seg(input_sentence)

    # 5个关键词
    keyword_sen = HanLP.extractKeyword(input_sentence, 5)
    keyword_list = [i for i in keyword_sen]
    # 句子中所有数目
    num_sen = StandardTokenizer.segment(input_sentence)
    number_list = [i.word for i in num_sen.iterator() if (str(i.nature) == 'mq')]
    # 命名实体识别
    name_list = [i.word for i in term_list if(str(i.nature) in ["nr","rr","nrf","nrj"])]
    # 机构识别
    organization_list = [i.word for i in term_list if(str(i.nature) in ["nt"])]
    # 地点识别
    place_list = [i.word for i in term_list if(str(i.nature) in ["ns"])]
    # Url识别
    url_sen = URLTokenizer.segment(input_sentence)
    url_list = [i.word for i in url_sen if(str(i.nature) == "xu")]

    print(term_list)
    return set(keyword_list),set(number_list),set(name_list),set(organization_list),set(place_list),set(url_list)

if  __name__ == "__main__":
    for sentence in sentences:
        sentences_now = get_no_token_sentence(sentence)
        #for sen in sentences_now:
        print("句子：",sentence)
        print(analyse_sentence(sentence))
        # print(remove_stop_word(sentence))
        # sentence_list = HanLP.extractSummary(sentence, 1)
        # print(sentence_list)
        analyse = HanLP.parseDependency(sentence)
        for word in analyse.iterator():  # 通过dir()可以查看sentence的方法
            # print(dir(word))
            print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
            # print(word.ID,word.POSTAG)
            # pass
        print("\r\n")
