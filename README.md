## Implementation of Classification and Regression (CART) Decision Tree Algorithm

This repository presents the implementation of the CART decision tree algorithm on the IRIS dataset. CART constructs binary trees using the attribute and threshold that yield the largest information gain at each node. 

The greedy algorithm identifies a split on an attribute, such as “petal_length”, that results in the largest information gain (IG) for a given impurity criterion (such as Entropy or Gini). Once a split is determined, the tree recursively adds children nodes until no further information gain can be made. A method for pruning the tree is included in the implementation to limit the complexity of the decision tree and reduce overfitting. A print method is also included to aid in viewing the output predictions. 
