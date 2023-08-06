from distutils.command.upload import upload
import numpy as np
import pandas as pd
from matplotlib import image,pyplot as plt
import matplotlib.patches as mpatches
from lazypredict.Supervised import LazyRegressor
#sklearn------------------------------------------------------
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
#RDKIT---------------------------------------------------------
from rdkit.Chem import AllChem
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
from rdkit.ML.Descriptors import MoleculeDescriptors
from rdkit.Avalon import pyAvalonTools
#streamlit-----------------------------------------------------
import streamlit as st
from PIL import Image
import base64
import io
#RFMODEL------------------------------------------------------
with open('RF_CN.pickle', 'rb') as f:
    model = pickle.load(f)

st.set_page_config(page_title='Buchwald−Hartwig C−N cross-coupling yield Prediction App', layout='wide')

st.sidebar.markdown('<h2 style="color:#5a03fc;background-color:powderblue; border-radius:10px;text-align:center"> Use this Sidebar for Buchwald−Hartwig C−N cross-coupling yield Prediction </h2>',unsafe_allow_html=True)	

#Display linkedin page on the main page
st.markdown(""" This Web Application was developed by [ZhaoWeiRen](http://faculty.dlut.edu.cn/yangli/zh_CN/xsxx/966679/content/215023.htm), a postgraduate in Dalian University of Technology.""")
st.markdown('`Buchwald-Hartwig-type C-N cross-coupling reactions` are a class of chemical reactions that involve the formation of a carbon-nitrogen bond through the coupling of an aryl or vinyl halide or triflate with an amine or an amide. These reactions are widely used in organic synthesis to construct complex molecules, including natural products, pharmaceuticals, and materials.')
st.markdown("===================================================================================================================================")

st.markdown("")
df = pd.read_csv('input1.csv')
df.columns = ['base_smiles', 'ligand_smiles', 'aryl_halide_smiles', 'additive_smiles', 'product_smiles']
df1 = pd.read_csv('input2.csv')
st.table(df.head())
st.markdown("`Input file`You can refer to the table above to create your input file. The contents of each column must match the contents of the table, and the order can't be changed to prevent inaccurate predictions")
st.markdown("===================================================================================================================================")
st.table(df1.head())
st.markdown("`Model secection` You can refer to the table above to create your input file. Note that the last column of the table must be the model's predicted value")
st.markdown("===================================================================================================================================")


def plot_graph(data):
	plt.rcParams['font.sans-serif']=['SimHei']
	plt.rcParams['axes.unicode_minus']=False
	a = np.linspace(-0.1, 100,1000)
	plt.scatter(data['Actual'].values, data['Predicted'].values,label='data', alpha=0.5, cmap='viridis')
	plt.plot(a,a, label='diagonal', ls='--', c='k')
	plt.text(80, 20, '$R^2$=0.94',fontsize=15, horizontalalignment='center', verticalalignment='center')
	plt.title('test set', fontsize=15)
	plt.xlabel('Predicted', fontsize=10)
	plt.ylabel('Experimental', fontsize=10)
	plt.ylim(-0.1, 101)
	plt.xlim(-0.1, 101)
	plt.grid(alpha=0.5)
	plt.legend()
	st.pyplot(plt)

test = pd.read_csv('test_1240.csv')
plot_graph(test)

def file_download(data, file):
	df = data.to_csv(index=False)
	f = base64.b64encode(df.encode()).decode()
	link = f'<a href ="data:file/csv; base64,{f}" download={file}> Download {file} file</a>'
	return link

def std(smiles):
    mols = [Chem.MolFromSmiles(smi, sanitize=False) for smi in smiles]
    smiles = [Chem.MolToSmiles(mol) for mol in mols]
    return smiles

def FPS(smile):
	mol = Chem.MolFromSmiles(smile, sanitize=False)
	smile1 = Chem.MolToSmiles(mol)
	mol1 = Chem.MolFromSmiles(smile1, sanitize=False)
	Avs1 = pyAvalonTools.GetAvalonFP(mol, nBits=512)
	a = np.array(Avs1)
	return a

file = st.sidebar.file_uploader("===========================================")
st.sidebar.markdown("======================================")
st.sidebar.markdown("""**If you upload your CSV file, click the button at the buttom of the page to get the csv file** """)
prediction = st.button("predict CN cross-coupling yield")
prediction1 = st.button("ML model Report")

if prediction:
	df = pd.read_csv(file)
	df.columns = range(5)
	for i in range(5):
		df[i] = std(df[i].astype(str))
	smiles = [str(x) for x in df[0]]
	mols = [Chem.MolFromSmiles(x) for x in smiles]
	Avs1 = [pyAvalonTools.GetAvalonFP(mol, nBits=512) for mol in mols]
	a = np.array(Avs1)
	for i in range(1,5):
		smiles = [str(x) for x in df[i]]
		mols = [Chem.MolFromSmiles(x, sanitize=False) for x in smiles]
		Avs = [pyAvalonTools.GetAvalonFP(mol, nBits=512) for mol in mols]
		a = np.concatenate((a, np.array(Avs)), axis=1)
		df1 = pd.DataFrame(a)
	X = df1.values
	Y_Prediction = model.predict(X)
	predicted = pd.DataFrame(Y_Prediction, columns=['predicted yield (%)'])
	output = pd.concat([df, predicted], axis=1)
	st.sidebar.markdown('''## Your output is shown in the following table:''')
	st.sidebar.write(output)
	st.sidebar.markdown(file_download(output, "predicted_CN_cross-coupling_yield.csv"), unsafe_allow_html=True)
elif prediction1:
	df1 = pd.read_csv(file)
	df1.columns = range(df1.shape[1])
	X = df1.drop(df1.shape[1]-1, axis=1).values
	y = df1[df1.shape[1]-1].values
	X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state =42)
	reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
	models, predictions = reg.fit(X_train, X_test, y_train, y_test)
	model = pd.DataFrame(models.sort_values(['R-Squared'],ascending=False))
	st.sidebar.markdown('''## Your output is shown in the following table:''')
	st.sidebar.write(model)
	st.sidebar.markdown(file_download(model, "ML_model_Report.csv"), unsafe_allow_html=True)

else:
	st.markdown('<div style="border: 2px solid #4908d4; border-radius:20px; padding:3%; text-align:center"> <h5> If you want to test this model, please use the sidebar.If you have many molecules,you can put their SMILES strings in a "SMILES" column, upload them and click the button which says "Predict CN cross-coupling reaction yield"shown in the sidebar.</h5> <h5 style="color:white; background-color:#0a0605; border-radius:10px; padding:3%; opacity:0.7;"> Please also note that predcition is more reliable if the compounds to be predicted are similar with training dataset.</h5></div>',unsafe_allow_html=True)
	st.markdown("===================================================================================================================================")
	