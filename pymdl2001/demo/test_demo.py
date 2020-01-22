from unittest import TestCase
from demo.demo_module import *
import demo


class TestDemoClass(TestCase):
    demo = DemoClass()

    def test_demo(self):
        # self.fail() # 自动生成的时候就有，作用未知
        # 单元测试失败样例
        # TestCase.assertEqual(self, 2, 3, '这里的单元测试不通过')
        # TestCase.assertEqual(self, 2, 3)
        # 单元测试成功样例
        TestCase.assertEqual(self, 2, 2, '这里的单元测试不通过')
        TestCase.assertEqual(self, 2, 2)

        TestCase.assertEqual(self, demo.demo(), None)
        TestCase.assertEqual(self, DemoClass.demo(self.demo), "Hello world.\nHello Demo.")
        TestCase.assertEqual(self, DemoClass.demo(self.demo), "Hello world.\nHello Demo.")

    def test_demo_add(self):
        TestCase.assertEqual(self, DemoClass.demo_add(self.demo, 1, 3), 4)
