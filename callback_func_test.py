# -*- coding: utf-8 -*-
import time


def callback():
    print("这是一个callback函数")


def test_callback(call):
    print("这是在test_callback中")
    # 模拟延时效果
    time.sleep(1)
    print('开始调用callback函数')
    time.sleep(1)
    # 开始回调
    call()
    print('调用完成')


if __name__ == '__main__':
    test_callback(callback)
