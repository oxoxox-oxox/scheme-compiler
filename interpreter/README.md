# Scheme编译器教程

## 概述

这是一个用Python编写的Scheme编译器，包含以下四个主要组件：

1. **Tokenizer（分词器）** - 将源代码分解为token
2. **Parser（解析器）** - 将token转换为AST（抽象语法树）
3. **Environment（环境）** - 管理变量和函数的作用域
4. **Evaluator（求值器）** - 执行AST

---

## 1. Tokenizer（分词器）

### 目的

将Scheme代码字符串转换成token列表。

### 工作原理

```python
def tokenize(s: str) -> List[str]:
    # (+ 1 2) -> ['(', '+', '1', '2', ')']
    s = re.sub(r'([()\'`])', r' \1 ', s)  # 在括号周围添加空格
    s = re.sub(r'\s+', ' ', s)             # 合并多个空格
    return [token for token in s.split() if token]
```

### 示例

```python
tokenize("(define x 10)")    # ['(', 'define', 'x', '10', ')']
tokenize("(+ 1 2)")          # ['(', '+', '1', '2', ')']
tokenize("(lambda (x) x)")   # ['(', 'lambda', '(', 'x', ')', 'x', ')']
```

---

## 2. Parser（解析器）

### 目的

将token列表转换为嵌套列表（S表达式）。

### S表达式

Scheme中的所有代码都是S表达式：

- **Atom**：数字、字符串、符号
- **List**：`(item1 item2 ...)`

### 工作原理

```python
def parse(tokens):
    # 递归读取token
    # 遇到'(' - 开始读取列表
    # 遇到')' - 结束读取列表
    # 其他 - 转换为atom（数字或符号）
```

### 示例

```python
parse(['(', '+', '1', '2', ')'])
# 结果: ['+', '1', '2']

parse(['(', 'define', 'x', '10', ')'])
# 结果: ['define', 'x', '10']

parse(['(', 'lambda', '(', 'x', ')', 'x', ')'])
# 结果: ['lambda', ['x'], 'x']
```

---

## 3. Environment（环境）

### 目的

管理变量和函数作用域，实现词法作用域。

### 结构

```python
class Environment:
    def __init__(self, params=None, args=None, outer=None):
        self.data = {}      # 存储当前作用域的变量
        self.outer = outer  # 父作用域
    
    def define(var, val):  # 定义变量
    def get(var):          # 获取变量
    def set(var, val):     # 修改变量
```

### 作用域链

```
全局环境
    ↑
  define x = 10
    ↑
函数f的局部环境（参数 x=5）
    ↑
  lambda的局部环境（参数 x=3）
```

---

## 4. Evaluator（求值器）

### 目的

执行S表达式并返回结果。

### 求值规则

#### 原子（Atom）

```scheme
; 数字直接返回
5                    → 5
3.14                 → 3.14

; 符号查找环境
x                    → (环境中x的值)
```

#### 特殊形式（Special Forms）

##### 1. quote - 引号

```scheme
'x                   → 'x (不求值)
(quote (+ 1 2))      → (+ 1 2)
```

##### 2. if - 条件语句

```scheme
(if test then-expr else-expr)

(if (> 5 3) 100 200) → 100
(if (< 5 3) 100 200) → 200
```

##### 3. define - 定义变量或函数

```scheme
; 定义变量
(define x 10)

; 定义函数（语法糖）
(define (square x) (* x x))
; 等价于
(define square (lambda (x) (* x x)))
```

##### 4. lambda - 匿名函数

```scheme
(lambda (x y) (+ x y))

; 调用
((lambda (x) (* x x)) 5) → 25
```

##### 5. begin - 顺序执行

```scheme
(begin
  (define x 10)
  (+ x 5))           → 15
```

##### 6. cond - 多路条件

```scheme
(cond 
  ((> x 10) 'large)
  ((> x 5) 'medium)
  (else 'small))
```

#### 函数调用

```scheme
; 求值所有参数，然后调用函数
(+ 1 2 3)            → 6
(* 2 3 4)            → 24
```

---

## 5. 内置函数

### 算术运算

```scheme
(+    1 2 3)         → 6
(-    10 3)          → 7
(*    2 3 4)         → 24
(/ 20 4)             → 5.0
(// 20 3)            → 6
(% 10 3)             → 1
```

### 比较

```scheme
(>  5 3)             → #t
(<  5 3)             → #f
(>= 5 5)             → #t
(<= 5 5)             → #t
(=  5 5)             → #t
```

### 逻辑

```scheme
(and #t #t)          → #t
(or  #f #t)          → #t
(not #t)             → #f
```

### 列表

```scheme
(list 1 2 3)         → [1, 2, 3]
(cons 1 '(2 3))      → [1, 2, 3]
(car  '(1 2 3))      → 1
(cdr  '(1 2 3))      → [2, 3]
(null? '())          → #t
(list? '(1 2))       → #t
```

### 类型检查

```scheme
(number?   5)        → #t
(integer?  5)        → #t
(float?    3.14)     → #t
(symbol?   'x)       → #t
```

---

## 6. 编程示例

### 示例1：阶乘（Factorial）

```scheme
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(factorial 5)        → 120
```

### 示例2：列表求和

```scheme
(define (sum lst)
  (if (null? lst)
      0
      (+ (car lst)
         (sum (cdr lst)))))

(sum '(1 2 3 4 5))   → 15
```

### 示例3：映射（Map）

```scheme
(define (map f lst)
  (if (null? lst)
      '()
      (cons (f (car lst))
            (map f (cdr lst)))))

(map (lambda (x) (* x x)) '(1 2 3 4))
                     → [1, 4, 9, 16]
```

### 示例4：过滤（Filter）

```scheme
(define (filter pred lst)
  (if (null? lst)
      '()
      (if (pred (car lst))
          (cons (car lst) (filter pred (cdr lst)))
          (filter pred (cdr lst)))))

(filter (lambda (x) (> x 3)) '(1 2 3 4 5))
                     → [4, 5]
```

### 示例5：二分查找

```scheme
(define (binary-search target lst low high)
  (if (> low high)
      -1
      (let ((mid (// (+ low high) 2)))
        (cond
          ((= (car (cdr lst mid)) target) mid)
          ((< (car (cdr lst mid)) target) 
           (binary-search target lst (+ mid 1) high))
          (else
           (binary-search target lst low (- mid 1)))))))
```

---

## 7. 使用方法

### 方法1：运行REPL（交互式）

```bash
python analyse.py
```

```
>>> (+ 1 2)
3
>>> (define x 10)
x
>>> (+ x 5)
15
>>> (quit)
```

### 方法2：运行示例

```bash
python examples.py
```

### 方法3：在代码中使用

```python
from analyse import tokenize, parse, evaluate, create_global_env

env = create_global_env()
code = "(+ (* 2 3) 4)"
tokens = tokenize(code)
ast = parse(tokens)
result = evaluate(ast, env)
print(result)  # 10
```

---

## 8. 核心算法流程图

```
Scheme源代码
    ↓
Tokenizer（分词）
    ↓
Token列表
    ↓
Parser（解析）
    ↓
AST（抽象语法树）
    ↓
Evaluator（求值）
    ├→ 原子? → 返回值
    ├→ 特殊形式? → 特殊处理
    └→ 函数调用 → 求值参数 → 调用函数
    ↓
结果
```

---

## 9. 常见问题

### Q1：什么是S表达式？

A：S表达式是Scheme的基本语法单位。是Symbolic Expression的缩写。

- 原子：`5`, `'x`
- 列表：`(+ 1 2)`（第一个元素是操作符，后面是参数）

### Q2：如何定义递归函数？

A：使用`define`定义命名函数，可以在函数体中递归调用自己。

### Q3：如何处理错误？

A：当前实现抛出Python异常。可以使用try-except捕获。

### Q4：如何扩展内置函数？

A：在`create_global_env()`函数中调用`env.define()`添加新函数。

---

## 10. 进阶扩展

### 可以添加的功能

1. **变量修改**

   ```scheme
   (set! x 20)
   ```

2. **Let绑定**

   ```scheme
   (let ((x 10) (y 20)) (+ x y))
   ```

3. **更多列表函数**

   ```scheme
   (length lst)
   (reverse lst)
   (append lst1 lst2)
   ```

4. **高阶函数**

   ```scheme
   (fold + 0 '(1 2 3 4))
   ```

5. **闭包**

   ```scheme
   (define (make-adder x)
     (lambda (y) (+ x y)))
   (define add5 (make-adder 5))
   (add5 3)  → 8
   ```

6. **尾调用优化**
   - 防止栈溢出

7. **模块系统**
   - 支持导入和命名空间

---

现在你已经理解了Scheme编译器的完整工作原理！

可以运行 `python examples.py` 查看各种使用示例。
或者运行 `python analyse.py` 使用交互式REPL。
