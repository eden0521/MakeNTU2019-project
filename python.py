import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os
import time
from time import sleep
import jieba
import jieba.posseg as pseg
import serial
import tempfile

print_control=0
err_msg1 = "Google Speech Recognition could not understand audio"
err_msg2 = "Could not request results from Google Speech Recognition service"
err_msg3 = 'waiting timeout'
command_msg = "天氣真好"
num = ['一', '二', '兩', '三', '四', '五', '六', '七', '八', '九']
vocab_list = [['紅茶', 'BT'], ['綠茶', 'GT'],
              ['茶水', 'WT'], ['礦泉水', "WT"], ['開水', 'WT'], ['白開水', 'WT'], ['冷水', 'WT'], ['自來水', 'WT'], ['水', 'WT'], ['純水', 'WT'],
              ['鮮奶', 'MK'], ['奶', 'MK'],['奶精', 'MK'], ['牛奶', 'MK'],['奶茶', 'MK'],
              ['糖', 'SG'], ['砂糖', 'SG'], ['白糖', 'SG'], ['黑糖', 'SG'],
             ['一些', 'SOME'], ['一點', 'SOME'], ['一小匙', 'SOME'], ['不要太多', 'SOME'],
             ['一小杯', 'SC'], ['小杯', 'SC'], ['半杯', 'SC'],
              ['一中杯', 'MC'], ['中杯', 'MC'], ['一杯', 'MC'],
             ['一大杯', 'LC'], ['大杯', 'LC'],
              ['一匙', 'SP'], ['一小匙', 'SSP'], ['一大匙', 'LSP'],
              ['二小匙', 'SP'], ['兩小匙', 'SP'], 
              ['一份', 'SC'], ['二份', 'MC'], ['兩份', 'MC'], ['一分', 'SC'], ['二分', 'MC'], ['兩分', 'MC'], 
             ['不加', 'no'], ['不要', 'no'], ['無', 'no'], ['沒有', 'no'], ['沒', 'no'],
              ['跟', 'yes'], ['和', 'yes'], ['加上', 'yes'], ['加', 'yes'], ['還有', 'yes'], ['還加上', 'yes'], ['再加上', 'yes'], ['再加', 'yes'], ['再', 'yes'],
             ['冰', 'a'], ['冰的', 'a'], ['冷', 'a'], ['冷的', 'a'], ['溫', 'a'], ['溫的', 'a'], ['熱', 'a'], ['熱的', 'a'],
             ['無糖', 'SA'], ['去糖', 'SA'], ['微糖', 'SA'], ['半糖', 'SA'], ['少糖', 'SA'], ['全糖', 'SA'], ['多糖', 'SA'],
              ['無', 'no'], ['去', 'no'], ['微', 'BIT'], ['半', 'HALF'], ['少', 'FEW'], ['全', 'FULL'], ['多', 'FULL'], 
              ['多一點', 'FEW'], ['少一點', 'BIT'],['多一點點', 'FEW'], ['少一點點', 'BIT'],['中一點', 'HALF'], ['中一點點', 'HALF']
             ]
for item in [['{}匙'.format(i), 'SP'] for i in num[1:]]:
    vocab_list.append(item)
for item in [['{}杯'.format(i), 'LC'] for i in num[1:]]:
    vocab_list.append(item)
for item in [['{}分'.format(i), 'LC'] for i in num[1:]]:
    vocab_list.append(item)
for item in [['{}份'.format(i), 'LC'] for i in num[1:]]:
    vocab_list.append(item)
target_tag = []
vocab_dict = {}
jieba.suggest_freq(('喝', '牛奶'), True)
jieba.suggest_freq(('喝', '水'), True)
jieba.suggest_freq(('喝', '一杯'), True)
jieba.suggest_freq(('水', '加'), True)
jieba.suggest_freq(('加', '大'), True)

for vocab in vocab_list:
    vocab_dict[vocab[0]] = vocab[1]
    jieba.add_word(vocab[0], tag=vocab[1])
    if vocab[1] not in target_tag and vocab[1] != 'a':
        target_tag.append(vocab[1])

useful_tag = ['n', 'm',] + target_tag
correct_number_tag = {'no':0, 'SOME':0.7, 'SC':0.3, 'MC':0.5, 'LC':0.7, 'MORE':0.7, 'FULL':0.9, 'FEW':0.7, 'HALF':0.5, 'BIT':0.3, 'NONE':0, 'SP':0.5, 'SSP':0.3, 'LSP':0.7, }
special_word = {'多':'MORE', '全':'FULL', '少':'FEW', '半':'HALF', '微':'BIT', '無':'NONE', '沒':'NONE'}
correct_item_tag = ['BT', 'GT', 'MT', 'WT', 'MK', 'SG']
mismatch_sentence = False
        
def recognize_output(sentence, debug):
    if debug:
        print(sentence)

def recognize_speech(r, m, debug=True):
    #print(r.energy_threshold)
    with m as source:
        #r = sr.Recognizer()
        try:
            audio = r.listen(source, timeout=0.5)
            
            try:
                sentence = r.recognize_google(audio, language='zh-TW')
                #sentence = r.recognize_sphinx(audio, language='zh-TW')
            except sr.UnknownValueError:
                sentence = "Google Speech Recognition could not understand audio"
                
            except sr.RequestError as e:
                sentence = "Could not request results from Google Speech Recognition service"
                
        except sr.WaitTimeoutError:
            sentence = 'waiting timeout'
    global print_control
    if debug == False:
        if print_control%3 == 0:
            print('                        ', end='\r')
            print('waiting right command.', end='\r') 
        elif print_control%3 == 1: 
            print('                        ', end='\r')
            print('waiting right command..', end='\r')
        elif print_control%3 == 2:
            print('                        ', end='\r')
            print('waiting right command...', end='\r')
            
            
        if print_control<100:    
            print_control=print_control+1  
        else: 
            print_control = 0
            
    else:
        if sentence != err_msg3:
            print(sentence)        
    return sentence

def extract_sentence(sentence, vocab_dict, useful_tag):
    words = jieba.cut(sentence)
    trans_words, trans_tags = [], []
    for word in words:
        if word in vocab_dict:
            trans_words.append(word)
            trans_tags.append(vocab_dict[word])
    extract_words, extract_tags = [], []
    for word, tag in zip(trans_words, trans_tags):
        if tag == 'SA':
            extract_words.append(word[0])
            if word[0] in vocab_dict:
                extract_tags.append(vocab_dict[word[0]])
            else:
                extract_tags.append('NONE')
            extract_words.append(word[1])
            if word[1] in vocab_dict:
                extract_tags.append(vocab_dict[word[1]])
            else:
                extract_tags.append('n')
        elif tag in useful_tag:
            extract_words.append(word)
            if len(word) == 1:
                if word in vocab_dict: 
                    extract_tags.append(vocab_dict[word])
                else:
                    extract_tags.append(tag)
            else:    
                extract_tags.append(tag)
    return extract_words, extract_tags
    
def convert_extracted_word(extract_words, extract_tags, correct_number_tag, correct_item_tag):
    global mismatch_sentence
    num_count, item_count = 0, 0
    for tag in extract_tags:
        print(tag)
        if tag in correct_number_tag: 
            num_count+=1
        if tag in correct_item_tag: 
            item_count+=1
            
    concate_element = ['yes', 'no']
    separate_idx=[i for i, tag in enumerate(extract_tags) if tag in concate_element]
    
    
    num_words, num_tags, item_words, item_tags = [], [], [], []
    try:
        if extract_tags[0] in correct_number_tag and set(extract_tags[1:]) < set(correct_item_tag):
            for word, tag in zip(extract_words[1:], extract_tags[1:]):
                num_words.append(extract_words[0])
                num_tags.append(extract_tags[0])
                item_words.append(word)
                item_tags.append(tag)
                
        elif set(extract_tags) < set(correct_item_tag):
                for word, tag in zip(extract_words, extract_tags):
                    num_words.append('一杯')
                    num_tags.append('MC')
                    item_words.append(word)
                    item_tags.append(tag)
        else:
            if num_count == item_count:
                print('same')  
                for i, tag in enumerate(extract_tags):
                    if tag in correct_number_tag: 
                        num_words.append(extract_words[i])
                        num_tags.append(tag)
                    if tag in correct_item_tag:
                        item_words.append(extract_words[i])
                        item_tags.append(tag)
            
            else:
                print('not same')
                for i in range(len(separate_idx)+1):
                    try:
                        if i == 0:
                            word_segment = extract_words[0:separate_idx[i]]
                            tag_segment = extract_tags[0:separate_idx[i]]

                        elif i == len(separate_idx):
                            word_segment = extract_words[separate_idx[i-1]:]
                            tag_segment = extract_tags[separate_idx[i-1]:]

                        else:
                            word_segment = extract_words[separate_idx[i-1]:separate_idx[i]]
                            tag_segment = extract_tags[separate_idx[i-1]:separate_idx[i]]
                    except IndexError:
                        mismatch_sentence = True
                        word_segment = []
                        tag_segment = []
                    #一杯  紅茶  加  牛奶  一點  糖
                    # 0     1    2   3     4    5   
                    num_word, num_tag, item_word, item_tag = separate_do(word_segment, tag_segment, correct_number_tag, correct_item_tag)

                    num_words.append(num_word)
                    num_tags.append(num_tag)
                    item_words.append(item_word)
                    item_tags.append(item_tag)
    except IndexError:
        mismatch_sentence = True
    return num_words, num_tags, item_words, item_tags
        
def separate_do(word_segment, tag_segment, correct_number_tag, correct_item_tag):
    #print(tag_segment)
    num_word, num_tag, item_word, item_tag = '', '', '', ''
    for i, tag in enumerate(tag_segment):
        #print(tag)
        if tag in correct_number_tag:
            num_word += word_segment[i]
            num_tag += tag
            #print('num_word, num_tag: ', num_word, num_tag)
        if tag in correct_item_tag:
            item_word += word_segment[i]
            item_tag += tag
            #print('item_word, item_tag: ', item_word, item_tag)
    return num_word, num_tag, item_word, item_tag


def arduino_input(sp, drink_type, output_time): # sp, string, float
    low_flag = 0
    while 1:
        start = time.time()
        sleep_time = 0;
        ## amount of drink
        if output_time == 0:  ##no drink, give middle
            sleep_time = 2
            #sp.close()
        else:
            sleep_time = output_time
        
        ##choose one drink
        #['BT', 'GT', 'MT', 'WT', 'MK', 'SG']  
        if mismatch_sentence:  ##no drink
            google_speak('為什麼..紅茶覺得重?..................因為..紅..茶..拿...鐵') 
            print('為什麼..紅茶覺得重?..................因為..紅..茶..拿...鐵') 
            #sp.close()
            break;
#             sp.write('a'.encode())
#             sleep(sleep_time)
#             sp.write('b'.encode())
#             sleep(sleep_time)
        elif(drink_type == 'WT'):   #water
            sp.write('a'.encode())
            sleep(sleep_time)
            sp.write('b'.encode())
            sleep(sleep_time)
#             break;

        elif(drink_type == 'BT'): #black tea
            sp.write('c'.encode())
            sleep(sleep_time)
            sp.write('d'.encode())
            sleep(sleep_time)
#             break;
        elif(drink_type == 'GT'): #green tea
            sp.write('e'.encode())
            sleep(sleep_time)
            sp.write('f'.encode())
            sleep(sleep_time)
#             break;
        elif(drink_type == 'MK'): #milk
            ##print('DETECT :  ',drink_list[0])
            sp.write('g'.encode())
            sleep(sleep_time)
            sp.write('h'.encode())
            sleep(sleep_time)
#             break;
        end = time.time()
        print('while loop top cost {} secs'.format(end-start))
        string = sp.readline()
#         while string == None:
#             string = sp.readline()
            
        print(string + b'--  123')
        
        if(string == b'low\r\n' and low_flag == 0):
            low_flag = 1
        if(string == b'high\r\n' and low_flag == 1): 
            #sp.close()
            sp.write('j'.encode())
            break;
            
        if(string == b'black_low\r\n' and low_flag == 0):
            low_flag = 1
        if(string == b'black_high\r\n' and low_flag == 1): 
            #sp.close()
            break;
        if(string == b'water_low\r\n' and low_flag == 0):
            low_flag = 1
        if(string == b'water_high\r\n' and low_flag == 1): 
            #sp.close()
            break;
        if(string == b'green_low\r\n' and low_flag == 0):
            low_flag = 1
        if(string == b'green_high\r\n' and low_flag == 1): 
            #sp.close()
            break;
        if(string == b'milk_low\r\n' and low_flag == 0):
            low_flag = 1
        if(string == b'milk_high\r\n' and low_flag == 1): 
            #sp.close()
            break;
            
def google_speak(sentence, lang='zh-TW'):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play()

def init():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold=False
    recognizer.energy_threshold=4000
    microphone = sr.Microphone()
    with microphone as source: 
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('done.')
        
    jieba.add_word("紅茶", freq=None, tag='n')
        
    return recognizer, microphone
    
    
def main():
    recognizer, microphone = init()
    global mismatch_sentence
    sentence=''
    while sentence != command_msg:
        sentence = recognize_speech(recognizer, microphone, debug=True)
        if sentence == command_msg:
            print('                        ', end='\r')
            print('指令正確')
            google_speak('嗨，要喝甚麼')
            print('嗨，要喝甚麼')
            sp.write('k'.encode())
    print(sentence)
    while sentence == err_msg1 or sentence == err_msg2 or sentence == err_msg3 or sentence == command_msg:
        sentence = recognize_speech(recognizer, microphone, debug=True)
        
    print('接收指令')
    extract_words, extract_tags = extract_sentence(sentence, vocab_dict, useful_tag)
    if extract_words == False and extract_tags == False:
        mismatch_sentence=True
    print('word', "  ".join(extract_words))
    print('詞性', "   ".join(extract_tags))

    num_words, num_tags, item_words, item_tags = convert_extracted_word(extract_words, extract_tags, correct_number_tag, correct_item_tag)
    
    if num_words == False or item_words == False:
        mismatch_sentence = True
    print(num_words, item_words)
    print(num_tags, item_tags)
#     sp = arduino_init()
#     sp.write('k'.encode())
    total_cost = 0
    alpha = 2.5
    for drink_type, output_type in zip(item_tags, num_tags):
        if output_type in correct_number_tag:
            output_time = correct_number_tag[output_type] * alpha
            total_cost = total_cost + output_time
        else:
            output_time = correct_number_tag['MC'] * alpha
            total_cost = total_cost + output_time
    print("total_cost:", total_cost)
    if total_cost > 3.0:
        alpha = alpha * (3.0 / total_cost)-0.2
    print('alpha_adjust: ', alpha)
    for drink_type, output_type in zip(item_tags, num_tags):    
        if output_type in correct_number_tag:
            output_time = correct_number_tag[output_type] * alpha
            
        else:
            output_time = correct_number_tag['MC'] * alpha
        
        arduino_input(sp, drink_type, output_time)
    if mismatch_sentence == False:
        google_speak('製作完成')
##################################################
if __name__ == "__main__":
    sp = serial.Serial()
    sp.port = 'COM3'
    sp.baudrate = 9600
    sp.timeout = 5
    sp.open()
    while 1:
        mismatch_sentence=False
        main()
    sp.close()