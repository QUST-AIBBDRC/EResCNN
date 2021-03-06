# This code is used for feature evaluation methods, 
# users must have provide labels for their sequencing data
# The output file will be generated in same folder of this code
# -------------------------------------------------------------

# load packages:
import sys,os
import re
import pandas as pd
import numpy as np
import scipy.io as sio
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier,GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from keras.models import Sequential
from keras.layers import Dense,Input,Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import Conv1D, MaxPooling1D
from keras.models import Model
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from sklearn.metrics import roc_curve,auc
from scipy import interp

# find the path
#Script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# read selected features
Script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# read selected features
filename = sys.argv[1]
yeast_data=sio.loadmat(filename)

protein_A=yeast_data.get('protein_A')#取出字典里的data
protein_B=yeast_data.get('protein_B')
X_shu_=np.hstack((protein_A,protein_B))
protein_label=yeast_data.get('protein_label') 
column=protein_A.shape[1]
y_shu_=protein_label.T.ravel()
def get_shuffle(dataset,label):    
    #shuffle data
    index = [i for i in range(len(label))]
    np.random.shuffle(index)
    dataset = dataset[index]
    label = label[index]
    return dataset,label,index 
X_shu,y_shu,index=get_shuffle(X_shu_,y_shu_) 
# Origanize data
X= X_shu
y= y_shu

def to_class(p):
    return np.argmax(p, axis=1)

def to_categorical(y, nb_classes=None):
    y = np.array(y, dtype='int')
    if not nb_classes:
        nb_classes = np.max(y)+1
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1
    return Y

# split data to 5 folds
skf= StratifiedKFold(n_splits=5)

# Evaluation method
# Feature evaluation SVM
clf_svm = SVC(probability=True)
ac_svm=[] # list to store accuracy
tprs_svm = [] # list to store tprs for ROC plotting
aucs_svm = [] # list to store aucs for ROC plotting

# Feature evaluation KNN
clf_knn = KNeighborsClassifier()
ac_knn=[]
tprs_knn = []
aucs_knn = []

# Feature evalution RandomForest
clf_rf  = RandomForestClassifier(n_estimators=100)
ac_rf = []
tprs_rf = []
aucs_rf = []

# Feature evaluation LightGBM
clf_lgbc=LGBMClassifier()
ac_lgbc=[]
tprs_lgbc = []
aucs_lgbc = []

# Feature evaluation xgboost
clf_xgb = XGBClassifier()
ac_xgb=[]
tprs_xgb = []
aucs_xgb = []

# Feature evaluation AdaBoost
clf_ada = AdaBoostClassifier()
ac_ada=[]
tprs_ada = []
aucs_ada = []

# Feature evaluation Bagging Classifier
clf_bag = BaggingClassifier()
ac_bag=[]
tprs_bag = []
aucs_bag = []

# Feature evaluation ExtraTree
clf_tree = ExtraTreesClassifier(n_estimators=100)
ac_tree=[]
tprs_tree = []
aucs_tree = []

# Feature evaluation Gaussian Naive Bayes
clf_gnb = GaussianNB()
ac_gnb=[]
tprs_gnb = []
aucs_gnb = []

# Feature evaluaton Gradient Boosting
clf_gbc = GradientBoostingClassifier()
ac_gbc=[]
tprs_gbc = []
aucs_gbc = []

# Feature evaluation deep neural network 
[sample_num,input_dim]=np.shape(X)
out_dim=2

ac_dnn=[]
tprs_dnn = []
aucs_dnn = []

# Feature evaluation convolutional neural network 
[sample_num,input_dim]=np.shape(X)
out_dim=2

ac_cnn=[]
tprs_cnn = []
aucs_cnn = []

# Feature evaluation recurrent neural network 
[sample_num,input_dim]=np.shape(X)
out_dim=2

ac_rnn=[]
tprs_rnn = []
aucs_rnn = []



for train, test in skf.split(X,y):
    clf_svm= clf_svm.fit(X[train], y[train]) #train model
    ac_svm.append(accuracy_score(y[test],clf_svm.predict(X[test]))) # add to accuracy list
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_svm.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_svm.append(interp(mean_fpr, fpr, tpr)) # add mean_fpr to tprs list
    tprs_svm[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_svm.append(roc_auc) # add aucs to auc list 
       
    clf_knn = clf_knn.fit(X[train], y[train])
    ac_knn.append(accuracy_score(y[test],clf_knn.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_knn.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_knn.append(interp(mean_fpr, fpr, tpr))
    tprs_knn[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_knn.append(roc_auc)
    
    clf_rf = clf_rf.fit(X[train], y[train])
    ac_rf.append(accuracy_score(y[test],clf_rf.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_rf.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_rf.append(interp(mean_fpr, fpr, tpr))
    tprs_rf[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_rf.append(roc_auc)
    
    clf_lgbc = clf_lgbc.fit(X[train], y[train])
    ac_lgbc.append(accuracy_score(y[test],clf_lgbc.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_lgbc.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_lgbc.append(interp(mean_fpr, fpr, tpr))
    tprs_lgbc[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_lgbc.append(roc_auc)
    
    clf_xgb = clf_xgb.fit(X[train], y[train])
    ac_xgb.append(accuracy_score(y[test],clf_xgb.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_xgb.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_xgb.append(interp(mean_fpr, fpr, tpr))
    tprs_xgb[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_xgb.append(roc_auc)
    
    clf_ada = clf_ada.fit(X[train], y[train])
    ac_ada.append(accuracy_score(y[test],clf_ada.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_ada.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_ada.append(interp(mean_fpr, fpr, tpr))
    tprs_ada[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_ada.append(roc_auc)
    
    clf_bag = clf_bag.fit(X[train], y[train])
    ac_bag.append(accuracy_score(y[test],clf_bag.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_bag.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_bag.append(interp(mean_fpr, fpr, tpr))
    tprs_bag[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_bag.append(roc_auc)
    
    clf_tree = clf_tree.fit(X[train], y[train])
    ac_tree.append(accuracy_score(y[test],clf_tree.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_tree.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_tree.append(interp(mean_fpr, fpr, tpr))
    tprs_tree[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_tree.append(roc_auc)
    
    clf_gnb = clf_gnb.fit(X[train], y[train])
    ac_gnb.append(accuracy_score(y[test],clf_gnb.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_gnb.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_gnb.append(interp(mean_fpr, fpr, tpr))
    tprs_gnb[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_gnb.append(roc_auc)
    
    clf_gbc = clf_gbc.fit(X[train], y[train])
    ac_gbc.append(accuracy_score(y[test],clf_gbc.predict(X[test])))
    mean_fpr = np.linspace(0, 1, 100)
    probas_ = clf_gbc.fit(X[train], y[train]).predict_proba(X[test])
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs_gbc.append(interp(mean_fpr, fpr, tpr))
    tprs_gbc[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs_gbc.append(roc_auc)


# Plot Figure 1
performance = [ac_svm,ac_knn,ac_rf,ac_lgbc,ac_xgb,ac_ada,ac_bag,ac_tree,ac_gnb,ac_gbc]
methods = ['SVM', 'KNN', 'RandomForest', 'LightGBM','xgboost','AdaBoost','Bagging','ExtraTree', 'Gaussian Naive Bayes','Gradient Boosting']

# accuracy
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('Box Plot')
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(performance, notch=0, sym='+', vert=1, whis=1.5)
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
               alpha=0.5)
ax.set_axisbelow(True)
ax.set_title('Comparison of Classification Accuracy between Ten Classifiers')
ax.set_xlabel('Classifiers')
ax.set_ylabel('Classification Accuracy')
boxColors=['red','chocolate','orange','darkgoldenrod','green','slategrey','c','blue','fuchsia','deeppink']
numBoxes = 10
medians = list(range(numBoxes))
for i in range(numBoxes):
    box = bp['boxes'][i]
    boxX = []
    boxY = []
    for j in range(5):
        boxX.append(box.get_xdata()[j])
        boxY.append(box.get_ydata()[j])
    boxCoords = list(zip(boxX, boxY))
    boxPolygon = Polygon(boxCoords, facecolor=boxColors[i])
    ax.add_patch(boxPolygon)
    # Now draw the median lines back over what we just filled in
    med = bp['medians'][i]
    medianX = []
    medianY = []
    for j in range(2):
        medianX.append(med.get_xdata()[j])
        medianY.append(med.get_ydata()[j])
        plt.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]
    # Finally, overplot the sample averages, with horizontal alignment
    # in the center of each box
    plt.plot([np.average(med.get_xdata())], [np.average(performance[i])],
             color='w', marker='*', markeredgecolor='k')

# Set the axes ranges and axes labels
ax.set_xlim(0.5, numBoxes + 0.5)
xtickNames = plt.setp(ax, xticklabels=methods)
plt.setp(xtickNames, rotation=45, fontsize=8)
plt.savefig('AC_Comparsion_'+filename+'.pdf')
plt.show()

results = pd.DataFrame(performance,index=methods)
results['mean'] = results.mean(axis=1)
results.to_csv("AC_"+filename+".csv")

# Figure two ROC CURVE
fig2, ax = plt.subplots(figsize=(13, 6))
fig2.canvas.set_window_title('ROC Plot')

plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', alpha=.8)
mean_tpr = np.mean(tprs_svm, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_svm)
plt.plot(mean_fpr, mean_tpr, color='red',
         label=r'SVM (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_knn, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_knn)
plt.plot(mean_fpr, mean_tpr, color='chocolate',
         label=r'KNN (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_rf, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_rf)
plt.plot(mean_fpr, mean_tpr, color='orange',
         label=r'RF (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_lgbc, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_lgbc)
plt.plot(mean_fpr, mean_tpr, color='darkgoldenrod',
         label=r'LightGBM (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_xgb, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_xgb)
plt.plot(mean_fpr, mean_tpr, color='green',
         label=r'xgBoost (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_ada, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_ada)
plt.plot(mean_fpr, mean_tpr, color='slategrey',
         label=r'AdaBoost (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_bag, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_bag)
plt.plot(mean_fpr, mean_tpr, color='c',
         label=r'Bagging (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_tree, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_tree)
plt.plot(mean_fpr, mean_tpr, color='blue',
         label=r'ExtraTree (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_gnb, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_gnb)
plt.plot(mean_fpr, mean_tpr, color='fuchsia',
         label=r'Gaussian Naive Bayes (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

mean_tpr = np.mean(tprs_gbc, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs_gbc)
plt.plot(mean_fpr, mean_tpr, color='deeppink',
         label=r'Gradient Boosting (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)


plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.savefig('ROC_Comparsion_'+filename+'.pdf')
plt.show()