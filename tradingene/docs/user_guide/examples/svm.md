## Using SVM

Full ```python``` code see [here](https://github.com/iburenko/tradingene/blob/master/tradingene/examples/svm.py); ```ipython``` notebook is [here](https://github.com/iburenko/tradingene/blob/master/tradingene/examples/SVM.ipynb).

With the Tradingene framework you are allowed to use all variety of machine learning methods, not restricting yourself with neural networks only. Two most popular libraries ```sklearn``` and ```keras``` are fully available for use as in the Framework so in the Platform.   

A sample script presented below implements a simple trading robot that makes trades according to the signals of an ```SVC``` model. To utilize such a model we import the required library first:

```python
from sklearn.svm import SVC
```

Next a model must be created and trained:
```python
# Creating an SVC model
model = SVC(tol=1e-4, degree=4)
train_output = np.reshape(data['train_output'], (np.shape(data['train_output'])[0], ))
model.fit(data['train_input'], train_output)
```

Eventually when implementing the ```onBar()``` function we use the ```predict``` method of the ```SVC``` class just like we do with neural networks:
```python
prediction = model.predict([inp])[0]
```
