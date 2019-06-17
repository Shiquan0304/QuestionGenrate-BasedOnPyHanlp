from 词性分析 import *
from 摘要提取 import *

def kill_son(seg, wordlist, keyword):
    for word in seg.iterator():
        if(str(word.HEAD.LEMMA) == keyword):
            wordlist[word.ID - 1] = ""
    return wordlist

def changeWord(word, wordlist, seg, replaceword = "", isKillSon = True):
    # 指定词语去除
    wordlist[word.ID-1] = replaceword
    # print(wordlist)
    if(isKillSon):
        kill_son(seg, wordlist, word.LEMMA)
    return "".join(wordlist)

def changeSentence(sentence, insert, isFront = True):
    if isFront:
        return insert + sentence.replace("。", "？")
    return sentence.replace("。", insert + "？")

def rule_word(word, wordList, sentence_seg, questions):
    # 找到时间标签，替换
    if(AttributeMatch[str(word.POSTAG)] == "时间词"):
        # 替换位置在原处
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么时候"), "", True))
        # 替换位置在开头
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, ""), "什么时候", True))

    # 与核心词为动宾关系
    if(str(word.DEPREL) == "动宾关系"):
        # 替换位置在原位置
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))

    # 为定中关系
    if (str(word.DEPREL) == "定中关系"):
        # 如果为简称略语
        if (AttributeMatch[str(word.POSTAG)] == "简称略语"):
            # 替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "谁"), "", True))

    # 为介宾关系
    if (str(word.DEPREL) == "介宾关系"):
        # 如果为名词
        if (AttributeMatch[str(word.POSTAG)] == "名词"):
            # 替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))

        # 为动宾关系
        if (str(word.DEPREL) == "动宾关系"):
            # 替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么", False), "", False))

        # 为定中关系
        if (str(word.DEPREL) == "定中关系"):
            # 如果为简称略语
            if (AttributeMatch[str(word.POSTAG)] == "地名"):
                # 替换位置在原处
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "哪里"), "", True))
        # 为主谓关系
        if (str(word.DEPREL) == "主谓关系"):
            # 3.1.1.1.1替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))
    return questions

if __name__ == "__main__":
    sentence = "以色列国防军20日对加沙地带实施轰炸，造成3名巴勒斯坦武装人员死亡。"
    sentence = "就是我们怎么进行问句生成的, 首先找种子问句, 就是找它相关的词出来话，我会生成大量的这样一些问句，然后人工也会筛选一些是这样的。"
    questions = []

    # 1.句子划分
    sentence_seg = HanLP.parseDependency(sentence)
    # print(dir(sentence_seg))

    # 2.遍历每个划分词
    for word in sentence_seg.iterator():  # 通过dir()可以查看sentence_seg的方法
        # print(dir(word))
        # print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
        # print(AttributeMatch[str(word.POSTAG)],word.POSTAG,word.LEMMA)

        # *2.0防止标点符号无意义
        if (AttributeMatch[str(word.POSTAG)] == "标点符号"):
            continue
            pass

        # 句子分词列表
        wordList = [word0.LEMMA for word0 in sentence_seg.iterator()]


        # 2.1如果指向核心关系/核心词，即为第一层关系
        if(str(word.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            # 2.1.1找到时间标签，替换
            if(AttributeMatch[str(word.POSTAG)] == "时间词"):
                # 2.1.1.1替换位置在原处
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么时候"), "", True))
                # 2.1.1.2替换位置在开头
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, ""), "什么时候", True))
                continue

            # 2.1.2与核心词为动宾关系
            if (str(word.DEPREL) == "动宾关系"):
                # 2.1.2.1替换位置在原位置
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))
                continue

        # 3.1二级关系
        if(word.HEAD.HEAD and str(word.HEAD.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            # 3.1.1为定中关系
            if (str(word.DEPREL) == "定中关系"):
                # 3.1.1.1如果为简称略语
                if(AttributeMatch[str(word.POSTAG)] == "简称略语"):
                    # 3.1.1.1.1替换位置在原处
                    questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "谁"), "", True))
                    continue

            # 3.1.2为介宾关系
            if (str(word.DEPREL) == "介宾关系"):
                # 3.1.2.1如果为名词
                if(AttributeMatch[str(word.POSTAG)] == "名词"):
                    # 3.1.2.1.1替换位置在原处
                    questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))
                    continue

            # 3.1.2为动宾关系
            if (str(word.DEPREL) == "动宾关系"):
                # 3.1.2.1.1替换位置在原处
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么", False), "", False))
                continue

        # 4.1三级关系
        if (word.HEAD.HEAD and word.HEAD.HEAD.HEAD and str(word.HEAD.HEAD.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            # 为定中关系
            if (str(word.DEPREL) == "定中关系"):
                # 3.1.1.1如果为简称略语
                if(AttributeMatch[str(word.POSTAG)] == "地名"):
                    # 3.1.1.1.1替换位置在原处
                    questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "哪里"), "", True))
                    continue

            # 为主谓关系
            if (str(word.DEPREL) == "主谓关系"):
                # 3.1.1.1.1替换位置在原处
                questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))
                continue

    # 输出问句
    print("\r\n".join([question.replace("。","？") for question in set(questions)]))
