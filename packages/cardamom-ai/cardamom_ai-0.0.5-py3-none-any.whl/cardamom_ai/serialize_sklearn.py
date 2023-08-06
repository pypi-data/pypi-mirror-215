import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

"""
    Serializes a neural net
    nn (MLPClassifier): Neural Net
"""
def serialize_neural_net(nn, fp):
    print('[', file=fp)
    print('[ "classifier" ],', file=fp)
    features = nn.feature_names_in_.tolist() \
        if hasattr(nn, "feature_names_in_") \
        else [f'"{str(x)}"' for x in range(nn.n_features_in_)]
    classes = nn.classes_.tolist() \
        if nn.classes_.dtype == '<U34' \
        else [str(x) for x in nn.classes_]
    print(f'[ "neural_network", {len(features)}, {len(classes)} ],', file=fp)
    print(f'[ {len(features)} ],', file=fp)
    print(str(features).replace("'", '"') + ',', file=fp)
    print(f'[ {len(classes)} ],', file=fp)
    print(str(classes).replace("'", '"') + ',', file=fp)
    print(f'[ {3 * (nn.n_layers_ - 1) -1 + 1} ],', file=fp)
    print('[', file=fp)
    for i in range(nn.n_layers_ - 1):
        print('[ "matmul" ],', file=fp)
        t = np.transpose(nn.coefs_[i]).tolist()
        print(f'[ {len(t)}, {len(t[0])} ],', file=fp)
        print(str(np.transpose(nn.coefs_[i]).tolist()) + ",", file=fp)
        print('[ "offset" ],', file=fp)
        print(f'[ {len(nn.intercepts_[i])} ],', file=fp)
        print(str(nn.intercepts_[i].tolist()) + ",", file=fp)
        if i != nn.n_layers_ - 2: # Add activation function before out_
            print(f'[ "{str(nn.activation)}" ],', file=fp)
    print(f'[ "{str(nn.out_activation_)}" ]', file=fp)
    print('],', file=fp)
    print('[', file=fp)
    for i in range(nn.n_layers_ - 1): # Activation doesn't have coeffs
        print('"matmul",', file=fp)
        t = np.transpose(nn.coefs_[i]).tolist()
        print(f'[ {len(t)}, {len(t[0])} ],', file=fp)
        print('"offset",', file=fp)
        print(f'[ {len(nn.intercepts_[i])} ],', file=fp)
        if i != nn.n_layers_ - 2: # Add activation function before out_
            print(f'"{str(nn.activation)}",', file=fp)
            print(f'[ {len(nn.intercepts_[i])} ],', file=fp)
    print(f'"{str(nn.out_activation_)}",', file=fp)
    print(f'[ {len(nn.intercepts_[-1])} ]', file=fp)
    print(']]', file=fp)
    return 0


"""
    Serializes a decision tree
    dt (DecisionTreeClassifier): Decision Tree classifier
"""
def serialize_decision_tree(dt, fp):
    if (dt.tree_.n_outputs != 1):
        import sys
        print("This only works with 1 output.", file=sys.stderr)
        return 1
    print('[', file=fp)
    print('[ "classifier" ],', file=fp)
    features = dt.feature_names_in_.tolist() \
        if hasattr(dt, "feature_names_in_") \
        else [f'"{str(x)}"' for x in range(dt.n_features_in_)]
    classes = dt.classes_.tolist() \
        if dt.classes_.dtype == '<U34' \
        else [str(x) for x in dt.classes_]
    print(f'[ "decision_tree", {len(features)}, {len(classes)} ],', file=fp)
    print(f'[ {len(features)} ],', file=fp)
    print(str(features).replace("'", '"') + ',', file=fp)
    print(f'[ {len(classes)} ],', file=fp)
    print(str(classes).replace("'", '"') + ',', file=fp)
    print(f'[ {dt.tree_.node_count}, {len(classes)} ],', file=fp)
    print('[', file=fp)
    for i in range(dt.tree_.node_count):
        print(
            str(dt.tree_.value[i][0].tolist()) \
                if dt.tree_.n_outputs == 1
                else str(dt.tree_.value[i].tolist())
            , file=fp
        )
        if i == dt.tree_.node_count - 1:
            continue
        print(',', file=fp)
    print('],', file=fp)
    print(f'[ {dt.tree_.node_count} ],', file=fp)
    print('[', file=fp)
    for i in range(0, dt.tree_.node_count):
        print('[', file=fp)
        print(
            str(dt.tree_.feature[i]),
            str(dt.tree_.threshold[i]),
            str(dt.tree_.children_left[i]),
            str(dt.tree_.children_right[i]),
            sep=',',
            file=fp
        )
        print(']', file=fp)
        if i == dt.tree_.node_count - 1:
            continue
        print(',', file=fp)
    print(']]', file=fp)
    return 0

"""
    Serializes a gaussian naive bayes model
    gnb (GaussianNB): Gaussian Naive Bayes classifier
"""
def serialize_naive_bayes(gnb, fp):
    print("[", file=fp)
    print('[ "classifier" ],', file=fp)
    features = gnb.feature_names_in_.tolist() \
        if hasattr(gnb, "feature_names_in_") \
        else [f'"{str(x)}"' for x in range(gnb.n_features_in_)]
    classes = gnb.classes_.tolist() \
        if gnb.classes_.dtype == '<U34' \
        else [str(x) for x in gnb.classes_]
    print(f'[ "naive_bayes", {len(features)}, {len(classes)} ],', file=fp)
    print(f'[ {len(features)} ],', file=fp)
    print(str(features).replace("'", '"') + ',', file=fp)
    print(f'[ {len(classes)} ],', file=fp)
    print(str(classes).replace("'", '"') + ',', file=fp)
    print(f'[ {len(gnb.theta_)}, {len(gnb.theta_[0])} ],', file=fp)
    print(str(gnb.theta_.tolist()) + ",", file=fp)
    print(f'[ {len(gnb.var_)}, {len(gnb.var_[0])} ],', file=fp)
    print(str(gnb.var_.tolist()) + ",", file=fp)
    print(f'[ {len(gnb.class_prior_)} ],', file=fp)
    print(str(gnb.class_prior_.tolist()), file=fp)
    print(']', file=fp)
    return 0

"""
Serializes a generic model by dispatching to a specific one
"""
def serialize_sklearn_classifier(m, fp):
    if isinstance(m, DecisionTreeClassifier):
        return serialize_decision_tree(m, fp), "decision_tree"
    elif isinstance(m, MLPClassifier):
        return serialize_neural_net(m, fp), "neural_network"
    elif isinstance(m, GaussianNB):
        return serialize_naive_bayes(m, fp), "naive_bayes"
    else:
        raise NotImplementedError

if __name__ == "__main__":
    import argparse
    from pickle import load
    import sys

    from traceback import print_exception

    parser = argparse.ArgumentParser(description='Prints an example ML Model')

    parser.add_argument('model', type=str, help='Path to model')

    args = parser.parse_args()
    with open(args.model, 'rb') as fp:
        clf = load(fp)

    try:
        serialize_sklearn_classifier(clf, fp=sys.stdout)
    except NotImplementedError:
        print("Model not supported yet!", file=sys.stderr)
    except:
        print_exception(*sys.exc_info())
