
import jieba
import joblib
import numpy as np


MODEL = None
TF = None
def load_model(model_path: str, tf_path: str) -> None:
    """"
    加载贝叶斯分类器的模型和权重
    参数：
        model_path (str): 贝叶斯分类器模型的路径
        tf_path (str): 贝叶斯分类器权重的路径

    返回：
        None
    """
    global MODEL 
    global TF

    MODEL = joblib.load(model_path)
    TF = joblib.load(tf_path)


def text_classification(name: str) -> str:
    """
    输入精英科技产品的系统名称，返回对应的产品线名称。

    参数：
        name (str): 精英科技产品的系统名称

    返回：
        str: 该系统对应的产品线名称
    """
    assert MODEL != None and TF != None
    
    words = jieba.cut(name)
    s = ' '.join(words)

    test_features = TF.transform([s]) 
    predicted_labels = MODEL.predict(test_features)
    predicted_probs = MODEL.predict_proba(test_features)
    label, prob = predicted_labels[0], np.max(predicted_probs)
    if prob < 0.3:
        return "该系统没有对应的产品线！"
    else:
        return name + ": " + label



    
    






