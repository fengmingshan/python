from flask import Flask,render_template,request
from config import Config
from forms import Text_form
import os
from sklearn.externals import joblib
from keras.models import load_model
import re
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from func import loadStopWords
from func import replace_spcial
from func import cutWords
from keras.preprocessing import sequence
from func import symbol_map


app = Flask(__name__)
app.config.from_object(Config)

data_path = r'D:\2020年工作\2020年NOC工单智能化项目'
os.chdir(data_path)

graph = tf.get_default_graph()
sess = tf.Session()
set_session(sess)

# 载入tokenizer模型用来统计词频
token = joblib.load('./token_file.pkl')
word_index = token.word_index

# 读取模型
model = load_model('./lstm_model_15_epochs_nosample.h5')

# 读取分类字典
with open('./label_dict.txt','r') as f:
    label_dict = eval(f.read())


def pred_class(msg):
    global token,model,symbol_map

    msg = msg.translate(symbol_map)
    msg = replace_spcial(msg)
    # 替换换行符
    msg = re.sub('\d','',msg)

    stopWords = loadStopWords()
    X_cut = cutWords(msg,stopWords) # 分词
    xtest_seq = token.texts_to_sequences(X_cut) #

    max_len = 216
    xtest_pad = sequence.pad_sequences(xtest_seq, maxlen=max_len)

    # 预测
    y_pred_prob = model.predict(xtest_pad, verbose=0)[0]
    y_pred_list = y_pred_prob.tolist()
    y_pred_class = y_pred_list.index(max(y_pred_list))
    return y_pred_class

@app.route('/',methods=['GET','POST'])
def text_classify():
    global graph,sess,label_dict
    form = Text_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            res_dict = request.form.to_dict()
            msg = res_dict['content'].translate(symbol_map)
            msg = replace_spcial(msg)
            msg = re.sub('\d', '', msg)
            stopWords = loadStopWords()
            cutword = cutWords(msg, stopWords)  # 分词
            cutword = ' '.join(str(cutword))
            with graph.as_default():
                set_session(sess)
                y_pred = pred_class(msg)
                label_text = label_dict.get(y_pred)
            form.content.data = res_dict['content']
            form.cutword.data = cutword
            form.result.data = str(y_pred) + ': ' + label_text
            return render_template('index.html',form=form)
    return render_template('index.html',form=form)

if __name__ == '__main__':
    app.run()
