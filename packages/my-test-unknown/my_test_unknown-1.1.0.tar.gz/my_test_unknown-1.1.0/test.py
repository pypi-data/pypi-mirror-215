class MyException(Exception):
    pass


try:
    x = -1

    if x < 0:
        raise MyException("Sorry, no numbers below zero")
except MyException as e:
    print("捕获到异常:", e)
