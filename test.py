from robdd import *


def test():
    """the ROBDD-CTL example in the slide"""
    t = []
    t.append(eval("((~a1)&(~a2))|((~a1)&a2)|(a1&(~a2))"))
    t[0].output("t0.html")
    P1 = eval(
        "((~a1)&(~a2)&(~a1')&(~a2'))|((~a1)&(~a2)&(~a1')&a2')|((~a1)&(~a2)&a1'&(~a2'))|((~a1)&a2&a1'&a2')|(a1&(~a2)&(~a1')&a2')|(a1&(~a2)&a1'&a2')|(a1&a2&(~a1')&(~a2'))"
    )
    i = 1
    while True:
        P2 = labelAppend(t[i - 1], "'")
        P = evalNode(Node("&", nodeType.operator, P1, P2))
        Pe = findable(P)
        V = evalNode(Node("&", nodeType.operator, t[0], Pe))
        iter = evalNode(Node("&", nodeType.operator, V, t[i - 1]))
        iter.output(f"t{i}.html")
        t.append(iter)
        if t[i] == t[i - 1]:
            break
        i += 1


test()
