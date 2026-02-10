import math

FUNCTIONS = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "arcsin": lambda x: math.degrees(math.asin(x)),
    "arccos": lambda x: math.degrees(math.acos(x)),
    "arctan": lambda x: math.degrees(math.atan(x)),
    "ln": lambda x: math.log(x),
    "log": lambda x: math.log10(x),
    "exp": lambda x: math.exp(x),
    "sqrt": lambda x: math.sqrt(x),
    "abs": lambda x: abs(x),              #قدر مطلق
}

OPERATORS = {"+", "-", "*", "/", "^"}
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
RIGHT_ASSOC = {"^"}  # توان راست‌همبند است


def is_number(token: str) -> bool:   #تشخیص میده توکن عدد هست یا نه
    try:
        float(token)
        return True
    except ValueError:
        return False


def tokenize(expr: str) -> list[str]:
    expr = expr.replace(" ", "")
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isdigit() or ch == ".":
            j = i
            dot = 0
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    dot += 1
                    if dot > 1:
                        raise ValueError("عدد اعشاری نامعتبر است.")
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue

        if ch.isalpha():
            j = i
            while j < len(expr) and expr[j].isalpha():
                j += 1
            name = expr[i:j]
            if name not in FUNCTIONS:
                raise ValueError(f"تابع ناشناخته: {name}")
            tokens.append(name)
            i = j
            continue

        if ch in OPERATORS or ch in ("(", ")"):
            tokens.append(ch)
            i += 1
            continue

        raise ValueError(f"کاراکتر نامعتبر: {ch}")

    return tokens


def infix_to_postfix(expr: str) -> list[str]:
    tokens = tokenize(expr)
    output: list[str] = []
    stack: list[str] = []
    prev = None   

    for tok in tokens:
        if is_number(tok):
            output.append(tok)
            prev = "num"
            continue

        if tok in FUNCTIONS:
            stack.append(tok)
            prev = "func"
            continue

        if tok == "(":
            stack.append(tok)
            prev = "("
            continue

        if tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("پرانتزها نامتوازن هستند.")
            stack.pop()  # '('

            if stack and stack[-1] in FUNCTIONS:
                output.append(stack.pop())

            prev = ")"
            continue

        if tok in OPERATORS:
            if tok == "-" and (prev is None or prev in ("op", "(")):
                output.append("0")

            while stack and stack[-1] in OPERATORS:
                top = stack[-1]
                if tok in RIGHT_ASSOC:
                    should_pop = PRECEDENCE[top] > PRECEDENCE[tok]
                else:
                    should_pop = PRECEDENCE[top] >= PRECEDENCE[tok]

                if should_pop:
                    output.append(stack.pop())
                else:
                    break

            stack.append(tok)
            prev = "op"
            continue

        raise ValueError(f"توکن نامعتبر: {tok}")

    while stack:
        if stack[-1] in ("(", ")"):
            raise ValueError("پرانتزها نامتوازن هستند.")
        output.append(stack.pop())

    return output


def apply_operator(op: str, a: float, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b      
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("تقسیم بر صفر مجاز نیست.")
        return a / b
    if op == "^":
        return a ** b
    raise ValueError(f"عملگر ناشناخته: {op}")


def safe_call_function(name: str, x: float) -> float:
    if name in ("ln", "log") and x <= 0:
        raise ValueError("برای ln/log ورودی باید مثبت باشد.")
    if name == "sqrt" and x < 0:        
        raise ValueError("برای sqrt ورودی نباید منفی باشد.")
    if name in ("arcsin", "arccos") and not (-1 <= x <= 1):
        raise ValueError("برای arcsin/arccos ورودی باید بین -1 و 1 باشد.")
    return FUNCTIONS[name](x)


def evaluate_postfix(postfix: list[str]) -> float:      #postfix list into number
    stack: list[float] = []

    for tok in postfix:
        if is_number(tok):
            stack.append(float(tok))
            continue

        if tok in FUNCTIONS:
            if not stack:
                raise ValueError("ورودی تابع ناقص است.")
            x = stack.pop()
            stack.append(safe_call_function(tok, x))
            continue

        if tok in OPERATORS:
            if len(stack) < 2:
                raise ValueError("عبارت نامعتبر است (کمبود عملوند).")
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_operator(tok, a, b))
            continue

        raise ValueError(f"توکن نامعتبر در postfix: {tok}")

    if len(stack) != 1:
        raise ValueError("عبارت نامعتبر است (عملوند اضافی).")
    return stack[0]


def calculate(expr: str) -> float:
    return evaluate_postfix(infix_to_postfix(expr))


if __name__ == "__main__":
    while True:
        s = input("عبارت را وارد کنید یا exit : ").strip()
        if s.lower() == "exit":
            break
        try:
            print("=", calculate(s))
        except Exception as e:
            print("خطا:", e)                      