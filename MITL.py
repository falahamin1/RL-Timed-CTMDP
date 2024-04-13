# class LTLNode:
#     def __init__(self, operator, *subformulas,  lbound = None, ubound = None):
#         if operator == "F" or operator == "G" or operator == "U":
#             if lbound == None or ubound == None: 
#                 print("Error, Please provide bounds.")
#                 return
#             else:
#                 self.lbound = lbound 
#                 self.ubound = ubound
#         self.operator = operator
#         self.subformulas = subformulas


#     def __str__(self):
#         if self.subformulas:
#             subformula_strs = ', '.join(str(subformula) for subformula in self.subformulas)
#             return "{}({})".format(self.operator, subformula_strs)
#         return self.operator

# # Examples of usage
# # Propositions are represented as nodes with no children
# p = LTLNode('p')
# q = LTLNode('q')

# # Operators are nodes with children
# not_p = LTLNode('NOT', p)
# p_and_q = LTLNode('AND', p, q)
# eventually_p = LTLNode('F', p, 0, 2)
# always_q = LTLNode('G', q, 2, 3)
# p_until_q = LTLNode('U', p, q, 3, 5)

# # Printing examples
# print(p)  # p
# print(not_p)  # NOT(p)
# print(p_and_q)  # AND(p, q)
# print(eventually_p)  # F(p)
# print(always_q)  # G(q)
# print(p_until_q)  # U(p, q)


class LTLNode:
    def __init__(self, operator, *subformulas, ubound=None, lbound=None):
        self.operator = operator
        self.subformulas = subformulas
        self.ubound = ubound
        self.lbound = lbound

    def __str__(self):
        subformula_strs = ', '.join(str(subformula) for subformula in self.subformulas)
        bounds_strs = []
        if self.ubound is not None:
            bounds_strs.append("ubound={}".format(self.ubound))
        if self.lbound is not None:
            bounds_strs.append("lbound={}".format(self.lbound))

        if bounds_strs:
            return "{}({}, {})".format(self.operator, subformula_strs, ', '.join(bounds_strs))
        return "{}({})".format(self.operator, subformula_strs)

# Example usage
p = LTLNode('p')
q = LTLNode('q')
p_until_q_with_bounds = LTLNode('U', p, q, ubound=10, lbound=3)
not_p = LTLNode('NOT', p)
p_and_q = LTLNode('AND', p, q)
eventually_p = LTLNode('F', p, lbound=0, ubound= 2)
always_q = LTLNode('G', q, lbound= 2, ubound= 3)
p_until_q = LTLNode('U', p, q, lbound= 3, ubound= 5)

print(p)  # p
print(not_p)  # NOT(p)
print(p_and_q)  # AND(p, q)
print(eventually_p)  # F(p)
print(always_q)  # G(q)

print(p_until_q_with_bounds)  # U(p, q, ubound=10, lbound=3)
