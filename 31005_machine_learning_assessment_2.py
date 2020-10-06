# -*- coding: utf-8 -*-
"""31005_machine_learning_assessment_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LASKReqFD2GCVvg2eaU8CjGErMAlPFM4

# **31005: Machine Learning**

## **Assessment 2**

#### Summary
In this notebook, we implement a decision tree algorithm from scratch. The choice of algorithm is the **Classification and Regression Tree (CART)** algorithm. CART constructs binary trees using the feature and threshold that yield the largest information gain at each node. The algorithm will be trained on the **IRIS dataset**.

### **Import required packages**
"""

import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree as sktree

"""### **Create CART_decision_tree Class**"""

class CART_decision_tree(object):
    """
    A recursively defined data structure to store a tree.
    Each node can contain other nodes as its children
    """
    def __init__(self, tree = 'cls', criterion = 'gini', prune = 'depth', max_depth = 4, min_criterion = 0.05):

        self.feature = None
        self.featurename = None
        self.label = None
        self.n_samples = None
        self.gain = None
        self.left = None
        self.right = None
        self.threshold = None
        self.depth = 0

        self.root = None
        self.criterion = criterion
        self.prune = prune
        self.max_depth = max_depth
        self.min_criterion = min_criterion
        self.tree = tree

    def fit(self, features, target):
        """
        The function accepts a training dataset, from which it builds the tree 
        structure to make decisions or to make children nodes (tree branches) 
        to do further inquiries.

        Parameters:
        features (dataframe): [n * p] n observed data samples of p attributes
        target (series): [n] target values
        """
        self.root = CART_decision_tree()
        if(self.tree == 'cls'):
            self.root._grow_tree(features, target, self.criterion)
        else:
            self.root._grow_tree(features, target, 'mse')
        self.root._prune(self.prune, self.max_depth, self.min_criterion, self.root.n_samples)

    def predict(self, features):
        """
        The function accepts a test dataset, from which it traverses the CART tree to output an
        array of predictions.

        Parameters:
        features (dataframe): [n * p] n observed data samples of p attributes

        Returns:
        list: [n] predicted values
        """                   
        #iterates over each test example and recusively invokes the internal method "_predicts" to check
        #if the current node attribute is below or above the threshold value until a prediction can be made.                                                                                
        return [self.root._predict(features.iloc[f,:]) for f in range(features.shape[0])]

    def print_tree(self):
        """
        Helper function to print tree decision structure.
        """
        self.root._show_tree(0, '')

    def _grow_tree(self, features, target, criterion = 'gini'):
        """"
        The internal function grows the tree by splitting the data into two branches based on some threshold
        value. The current node is assigned the feature that provides the best split with the corresponding
        threshold value.

        Parameters:
        features (dataframe): [n * p] n observed data samples of p attributes
        target (series): [n] target values
        criterion (string): Type of impurity criterion measure. default = 'gini'
        """
        self.n_samples = features.shape[0]
        
        #if all classes are the same, node is labelled as the class and returned. Terminates recrsion.
        if len(pd.unique(target)) == 1:                                                                             
            self.label = target.iloc[0]
            return

        best_gain = 0.0
        best_feature = None
        best_threshold = None

        if criterion in {'gini', 'entropy'}:
            #calculates which class has the most instances in the data and assigns node with that label.
            self.label = max([(c, len(target[target == c])) for c in np.unique(target)], key = lambda x : x[1])[0]  
        else:
            #calculates the mean in a regression problem and assigns node with that label.
            self.label = np.mean(target)                                                                            

        #calculates impurity criterion of the parent node.
        impurity_node = self._calc_impurity(criterion, target)                                                      
        
        #iterates over all split decisions to determine the best information gain, feature and threshold.
        for col in range(features.shape[1]):                                                                        
            feature_level = pd.unique(features.iloc[:,col])
            
            #create a list of candidate thresholds.
            thresholds = (feature_level[:-1] + feature_level[1:]) / 2.0                                             

            for threshold in thresholds:
                #calculates dataset for left child node.
                target_l = target[features.iloc[:,col] <= threshold] 
                #calculates left child node impurity criterion.                                             
                impurity_l = self._calc_impurity(criterion, target_l) 
                #calculates ratio of samples/total samples.                                             
                n_l = float(target_l.shape[0]) / self.n_samples                                                     

                #calculates dataset for right child node.
                target_r = target[features.iloc[:,col] > threshold]
                #calculates right child node impurity criterion.                                              
                impurity_r = self._calc_impurity(criterion, target_r)
                #calculates ratio of samples/total samples.                                              
                n_r = float(target_r.shape[0]) / self.n_samples                                                     

                #calculates information gain.
                information_gain = impurity_node - (n_l * impurity_l + n_r * impurity_r)                            
                if information_gain > best_gain:
                    best_gain = information_gain
                    best_feature = col
                    best_threshold = threshold

        self.feature = best_feature
        self.featurename = features.columns[best_feature]
        self.gain = best_gain
        self.threshold = best_threshold
        #iteratively splits the tree and creates children nodes based on spilt criterion.
        self._split_tree(features, target, criterion)                                                               

    def _split_tree(self, features, target, criterion):
        """"
        The internal function splits the dataset, creates left and right child nodes and recursively grows the tree.

        Parameters:
        features (dataframe): [n * p] n observed data samples of p attributes
        target (series): [n] target values
        criterion (string): Type of impurity criterion measure. default = 'gini'
        """
        #left child node
        features_l = features[features.iloc[:, self.feature] <= self.threshold]                                     
        target_l = target[features.iloc[:, self.feature] <= self.threshold]
        self.left = CART_decision_tree()
        self.left.depth = self.depth + 1
        self.left._grow_tree(features_l, target_l, criterion)

        #right child node
        features_r = features[features.iloc[:, self.feature] > self.threshold]                                      
        target_r = target[features.iloc[:, self.feature] > self.threshold]
        self.right = CART_decision_tree()
        self.right.depth = self.depth + 1
        self.right._grow_tree(features_r, target_r, criterion)

    def _calc_impurity(self, criterion, target):
        """"
        The internal function calculates the impurity criterion depending on chosen measure and returns the value.

        Parameters:
        criterion (string): Type of impurity criterion measure
        target (series): [n] target values
        
        Returns:
        float: Impurity criterion
        """
        if criterion == 'gini':
            return 1.0 - sum([(float(len(target[target == c])) / float(target.shape[0])) ** 2.0 for c in np.unique(target)])
        elif criterion == 'mse':
            return np.mean((target - np.mean(target)) ** 2.0)
        else:
            entropy = 0.0
            for c in np.unique(target):
                p = float(len(target[target == c])) / target.shape[0]
                if p > 0.0:
                    entropy -= p * np.log2(p)
            return entropy            

    def _prune(self, method, max_depth, min_criterion, n_samples):
        """"
        The internal function tunes the depth of the tree depending on parameters. Reduces overfitting of the data.

        Parameters:
        method (string): Method of pruning. default = 'depth'
        max_depth (int): Maximum depth of the tree
        min_criterion (float): Minimum criterion value
        n_samples (int): Number of samples in the current node
        """
        if self.feature is None:
            return

        self.left._prune(method, max_depth, min_criterion, n_samples)
        self.right._prune(method, max_depth, min_criterion, n_samples)

        pruning = False

        if method == 'impurity' and self.left.feature is None and self.right.feature is None: 
            if (self.gain * float(self.n_samples) / n_samples) < min_criterion:
                pruning = True
        elif method == 'depth' and self.depth >= max_depth:
            pruning = True

        if pruning is True:
            self.left = None
            self.right = None
            self.feature = None

    def _predict(self, d):
        """"
        The internal function takes in a row of input values and recursively checks a threshold value until a
        predicted label is returned.

        Parameters:
        d (series): [1 * p] Observed data samples of p attributes

        Returns:
        string: Predicted label
        """
        if self.feature != None:
            if d[self.feature] <= self.threshold:
                return self.left._predict(d)
            else:
                return self.right._predict(d)
        else:
            return self.label

    def _show_tree(self, depth, cond):
        """
        Internal helper function to print tree decision structure.
        """
        base = '|---' * depth + cond
        if self.feature != None:
            print(base + 'if ' + self.featurename + ' <= ' + f"{self.threshold:.2f}")
            self.left._show_tree(depth+1, 'then ')
            self.right._show_tree(depth+1, 'else ')
        else:
            print(base + '{class is: ' + str(self.label) + ', number of samples: ' + str(self.n_samples) + '}')

"""### **Load Iris dataset from seaborn library and split into train and test sets**"""

iris = sns.load_dataset('iris')
X, y = iris.iloc[:, 0:4], iris['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 42)

"""### **Create instance of CART decision tree**

*   Fit the training data and print CART Decision Tree
*   Make predictions on iris data test set and print accuracy
*   Compare accuracy to Sklearn Decision Tree Classifier
"""

print('\nCART Decision Tree (entropy)\n-------------------------------------------------------------------')
CARTtree = CART_decision_tree(tree = 'cls', criterion = 'entropy', prune = 'depth', max_depth = 3)
CARTtree.fit(X_train, y_train)
CARTtree.print_tree()

pred = CARTtree.predict(X_test)
print("\nCART Decision Tree Prediction Accuracy:    {}".format(sum(pred == y_test) / len(pred)))

dtree = sktree.DecisionTreeClassifier(criterion = 'entropy')
dtree.fit(X_train, y_train)
sk_pred = dtree.predict(X_test)
print("Sklearn Library Tree Prediction Accuracy:  {}".format(sum(sk_pred == y_test) / len(pred)))

print('\nCART Decision Tree (gini)\n-------------------------------------------------------------------')
CARTtree_gini = CART_decision_tree(tree = 'cls', criterion = 'gini', prune = 'depth', max_depth = 3)
CARTtree_gini.fit(X_train, y_train)
CARTtree_gini.print_tree()

pred = CARTtree_gini.predict(X_test)
print("\nCART Decision Tree Prediction Accuracy:    {}".format(sum(pred == y_test) / len(pred)))

dtree2 = sktree.DecisionTreeClassifier(criterion = 'gini')
dtree2.fit(X_train, y_train)
sk_pred = dtree2.predict(X_test)
print("Sklearn Library Tree Prediction Accuracy:  {}".format(sum(sk_pred == y_test) / len(pred)))