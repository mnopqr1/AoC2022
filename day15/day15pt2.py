import day15

# failed attempts

# class Rectangle:
#     def __init__(self, ll: Pt, wh: Pt):
#         self.ll = ll #lower left
#         self.wh = wh
#         self.lr = Pt(self.ll.x + self.wh.x, self.ll.y) #lower right
#         self.ul = Pt(self.ll.x, self.ll.y + self.wh.y) #upper left
#         self.ur = Pt(self.ll.x + self.wh.x, self.ll.y + self.wh.y) #upper right

#     def contains(self, p: Pt):
#         return self.ll.x <= p.x <= self.lr.x and self.ll.y <= p.y <= self.ul.y

#     def intersects(self, other):
#         if self.ll.x <= other.ll.x:
#             left, right = self, other
#         else:
#             left, right = other, self
#         if left.lr.x < right.ll.x:
#             return False
#         else:
#             if left.ul.y < right.ll.y:
#                 return False
#             elif right.ul.y < left.ll.y:
#                 return False
#             else:
#                 return True
    
#     def remove(self, other):
#         if self.ll.x <= other.ll.x <= self.lr.x:
#             pass



# from random import randint
# def rpt(a,b):
#     return Pt(randint(a,b), randint(a,b))

# def test_rectangle_intersect():
#     N = 1000
#     points = [Pt(x,y) for x in range(-10,21) for y in range(-10, 21)]
#     for _ in range(N):
#         r1 = Rectangle(rpt(-10,10), rpt(1,10))
#         r2 = Rectangle(rpt(-10,10), rpt(1,10))
        
#         hasint = any(r1.contains(p) and r2.contains(p) for p in points)
#         assert r1.intersects(r2) == hasint, f"R1: {r1.ll, r1.wh}, R2: {r2.ll, r2.wh}, hasint: {hasint}"
#     # r1 = Rectangle(Pt(0,0), Pt(2,3))
#     # r2 = Rectangle(Pt(-2,-2), Pt(3,2))
#     # r3 = Rectangle(Pt(2,3), Pt(3,4))
#     # assert r1.intersects(r2)
#     # assert r1.intersects(r3)
#     # assert r2.intersects(r1)



# class RectRegion:
#     def __init__(self, g: Rectangle):
#         self.boxes = {g}

#     def remove(self, r: Rectangle):
#         for b in self.boxes:
#             if b.intersects(r):
#                 pass
