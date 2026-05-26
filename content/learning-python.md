title: Python 面向对象编程学习总结
date: 2026-05-24
summary: 通过实际代码案例，总结 Python OOP 的核心概念：类、继承、方法重写等。

## 从基础语法到面向对象

学完 Python 基础语法后，我开始接触面向对象编程（OOP）。刚开始觉得有点抽象，但通过一些实际的小例子，慢慢就理解了。

### 类和对象

类就像是一个蓝图，对象是根据蓝图创建出来的具体实例：

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"

# 创建对象
xiaoming = Student("小明", 18)
print(xiaoming.introduce())  # 我叫小明，今年18岁
```

### 继承

子类可以继承父类的属性和方法，实现代码复用：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name}说：汪汪！"

class Cat(Animal):
    def speak(self):
        return f"{self.name}说：喵喵！"
```

### 魔法方法

Python 有很多以双下划线开头和结尾的特殊方法，让我印象最深的是这几个：

- `__init__`：初始化对象
- `__str__`：定义打印对象时显示的内容
- `__eq__`：定义两个对象相等的比较规则

理解了 OOP 之后，写代码的思路完全不一样了，开始懂得如何设计一个"类"来解决问题，而不仅仅是写一堆函数。
