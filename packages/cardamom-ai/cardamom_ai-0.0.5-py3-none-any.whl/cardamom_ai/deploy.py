from json import dumps
from sys import stderr
from os import environ
from tempfile import NamedTemporaryFile
import time

import requests

from cardamom_ai.serialize_sklearn import serialize_sklearn_classifier

def deploy_model(model, name):
    out = NamedTemporaryFile(mode='w+', delete=False)
    status, ctype = serialize_sklearn_classifier(model, out)
    if status != 0:
        return status
    outname = out.name
    out.close()
    out2 = open(outname, 'r')

    res = requests.post(
        f"https://{environ['CARDAMOM_HOST']}/sign_url/{name}"
    )
    res.raise_for_status()
    json = res.json()
    if 'errorMessage' in json:
        print(json['errorMessage'])
        return -1
    status = json["status_url"]
    res = requests.put(
        json["sign_url"],
        headers={
            "Content-Type": ctype,
        },
        data=out2,
    )
    out2.close()
    res.raise_for_status()
    print("Sent data successfully")
    for _ in range(12):
        time.sleep(6)
        print(f"Checking status at {status}")
        res = requests.get(status)
        if res.status_code != 200:
            continue
        if res.text == "\"COMPLETE\"":
            break
    else:
        return -4
    return f"https://{environ['CARDAMOM_HOST']}/{name}"

if __name__ == "__main__":
    import argparse
    from pickle import load
    import sys

    from traceback import print_exception

    parser = argparse.ArgumentParser(
            description='Deploys an example ML Model to CardamomAI')

    parser.add_argument('model', type=str, help='Path to model')

    args = parser.parse_args()
    with open(args.model, 'rb') as fp:
        clf = load(fp)
        predict_endpoint = deploy_model(clf, args.model)
    if not isinstance(predict_endpoint, str):
        sys.exit(predict_endpoint)
    for _ in range(10):
        time.sleep(5)
        try:
            res = requests.post(predict_endpoint)
            if res.status_code == 200:
                print(dumps(res.json(), indent=2))
                break
        except:
            pass
