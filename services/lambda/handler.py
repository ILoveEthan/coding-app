import sys
from io import StringIO

def lambda_handler(event):
    # TODO implement
    code = event['answer']
    test = event['test']
    solution = event['solution']
    
    test_code = code + '\nprint(' + test + ')'
    
    buffer = StringIO()
    sys.stdout = buffer
    
    try:
        exec(test_code)
    except Exception as e:
        return e
    
    sys.stdout = sys.stdout
    if buffer.getvalue()[:-1] == solution:
        return True
    return False

test1 = {
    "answer": "def sum(x,y):\n    return x+y",
    "test": "sum(1,1)",
    "solution": "2"
}

sumlist = {
    "answer": "def sum_list(x):\n    return sum(x)",
    "test": "sum_list([10, 11, 12, 13, 14, 15, 16])",
    "solution": "91"
}

if __name__=="__main__":
    print(lambda_handler(test1))