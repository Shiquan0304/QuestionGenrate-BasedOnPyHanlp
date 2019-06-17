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
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么时候", False), "", True))
        # 替换位置在开头
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "", False), "什么时候", True))

    # 与核心词为动宾关系
    if(str(word.DEPREL) == "动宾关系"):
        # 替换位置在原位置
        questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))

    # 为定中关系
    if (str(word.DEPREL) == "定中关系"):
        # 如果为简称略语
        if (AttributeMatch[str(word.POSTAG)] == "简称略语"):
            # 替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "谁"), "", False, True))
        else:
            # 替换位置在原处
            questions.append(changeSentence(changeWord(word, wordList, sentence_seg, "什么"), "", True))

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

def QG(sentence):
    questions = []

    # 1.句子划分
    if (len(sentence) > 100):
        sentence_seg = HanLP.parseDependency(getSummar(sentence, 5))
    else:
        sentence_seg = HanLP.parseDependency(sentence)
    # print(dir(sentence_seg))

    # 2.遍历每个划分词
    for word in sentence_seg.iterator():  # 通过dir()可以查看sentence_seg的方法
        # print(dir(word))
        # print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
        # print(AttributeMatch[str(word.POSTAG)],word.POSTAG,word.LEMMA)

        if (not (str(word.POSTAG) in AttributeMatch.keys())):
            break

        # *2.0防止标点符号无意义
        if (AttributeMatch[str(word.POSTAG)] == "标点符号"):
            continue

        # 句子分词列表
        wordList = [word0.LEMMA for word0 in sentence_seg.iterator()]

        # 2.1如果指向核心关系/核心词，即为第一层关系
        if (str(word.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            rule_word(word, wordList, sentence_seg, questions)

        # 3.1二级关系
        if (word.HEAD.HEAD and str(word.HEAD.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            rule_word(word, wordList, sentence_seg, questions)

        # 4.1三级关系
        if (word.HEAD.HEAD and word.HEAD.HEAD.HEAD and str(word.HEAD.HEAD.HEAD.DEPREL) == "核心关系"):
            # print(word.LEMMA,word.HEAD.LEMMA, word.DEPREL, AttributeMatch[str(word.POSTAG)], word.POSTAG)

            rule_word(word, wordList, sentence_seg, questions)

    # 输出问句
    print("\r\n".join([question.replace("。", "？") for question in set(questions)]))
    print()
    #print(set(questions))

if __name__ == "__main__":
    sentence = "以色列国防军20日对加沙地带实施轰炸，造成3名巴勒斯坦武装人员死亡。"
    sentence = """Python在设计上坚持了清晰划一的风格，这使得Python成为一门易读、易维护，并且被大量用户所欢迎的、用途广泛的语言。"""

    sentences = [
        "在一个非常美丽的乡下，有森林、小溪和一座漂亮的房子，这是贝拉拉的家。",
"贝拉拉家养了一只鸭子、一只小鸡，还有一只猫。",
"这只鸭子马上要变成鸭妈妈了，因为她的小鸭子快要孵出来了。",
"终于，蛋一个接着一个“噼！噼！”开始裂了，出来一个个可爱的、毛绒绒的小鸭子，他们还“吱，吱！”的叫，鸭妈妈“嘎，嘎”的回答他们，好像在说：“好美丽的世界啊！”",
"可是还有一个大的鸭蛋没有裂开，于是鸭妈妈继续坐在巢里，这时有一只老鸭子路过说：“哈喽！最近还好吗？”鸭妈妈说：“还有一枚蛋需要花很长时间。",
"”老鸭子说：“让我看看你那枚没裂开的蛋”，看完后他告诉鸭妈妈，那颗蛋是枚鸡蛋。",
"她劝鸭妈妈带着其他小鸭子去学游泳，鸭妈妈说它在坐一段时间看看，等它裂开。",
"终于这枚大蛋裂开了，出来一只又大又丑的鸭子，和其他小鸭子不一样。",
"鸭妈妈想：这小家伙会不会真是火鸡呢？鸭妈妈想了一个办法，这一天阳光明媚，非常暖和，它带着孩子们去游泳。",
"鸭妈妈扑通跳进水里，小鸭子们也一个接着一个跟着跳下去。",
"水淹到了它们头上，但是它们马上又冒出来了，游得非常漂亮。",
"它们的小腿很灵活地划着。",
"它们全都在水里，连那个丑陋的灰色小家伙也跟它们在一起游。",
"真好！它不是火鸡。",
"小鸭子们跟着妈妈游得很开心，这一天很顺利。",
"可是过了几天，小鸡们都啄这只丑鸭子，而且情况一天比一天糟。",
"大家都要赶走这只可怜的小鸭，连它自己的兄弟姊妹也对它生气起来。",
"它们老是说：“你这个丑妖怪，希望猫儿把你抓去才好！”",
"有一天丑小鸭看见蓝天上飞过一群白天鹅，丑小鸭羡慕极了。",
"它想：要是我也能拥有一双像白天鹅一样——又宽又坚硬的翅膀该多好呀！那样，我就能飞到外面的世界去看看。",
"”丑小鸭慢慢长大，终于有一天它离开了家。",
"这是一个寒冷的冬天，丑小鸭走了很久走累了，倒在了地上。",
"这时，一位农夫路过，好心的农夫救了丑小鸭，把它抱回家并它做了一个温暖舒适的家。",
"到了第二年春天，丑小鸭终于长大了。",
"它也不再是那只灰色的丑小鸭，它有雪白的羽毛，变成了一只白天鹅。",
"这一天它在河里游泳，天空中一群白天鹅飞过，它们和丑小鸭打招呼，很快它们就成了好朋友，一起游过一条小河，不知不觉来到了贝拉拉家的附近。",
"它们轻飘飘地浮在水上，羽毛发出飕飕的响声。",
"小鸭们认出了丑小鸡，心里感到一种说不出的难过。",
"鸭妈妈高兴地为丑小鸭祝福，看着丑小鸭和白天鹅们越飞越高、越飞越快、越飞越远。"
    ]

    for i in sentences:
        QG(i)