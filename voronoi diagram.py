﻿"""
#------------------------------------------
# $LAN=Python$
# Author : 陳柏憲  Bo-Xian Chen
# Student ID : M053040020
# Date : 2016/10/05
#------------------------------------------
"""
# [            Voronoi Diagram             ]
from _io import open
from ctypes.wintypes import BOOLEAN
from fractions import *  # process Fraction
import math
import random
from tkinter import filedialog

from SimpleGUICS2Pygame.simpleguics2pygame import Canvas
from numpy import cross
from sympy import *  # process polynomial

import numpy as np  # process vector


try:
    import simplegui

    SIMPLEGUICS2PYGAME = False
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    SIMPLEGUICS2PYGAME = True

color_list = ['Aquz', 'Blue', 'Fuchsia', 'Gray', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Silver', 'Teal', 'Yellow']

# intialize globals
width = 600
height = 600
point_begin = 0
point_end = 0
ind = 0
point_num = []
store_list = []
point_list = []
show_point = []
line_list = []
ball_radius = 1
ball_color = "BLACK"
start_control = False
i = 0

# read file with comment
def read_file_comment():
    clear_window()
    # file = open("test1.txt", 'r')
    file = filedialog.askopenfile(initialdir="/", mode='r', title="Select file")
    Flag = False;
    global point_list
    global i
    while (file != None):
        f_str = file.readline()
        
        f_list = list(f_str)
        print(f_str, end="")
        
        if(f_str == "0\n"):
#       print(f_str)
            file.close
            break
        elif (f_str == '\n'):
            continue
        elif(f_list[0] != '#'):
            # print(f_str,end='')
            if(Flag == False and int(f_str) > 0):
                count = int(f_str)
                Flag = True
                point_num.append(count)
    
            elif(Flag == True and count):
                pos = f_str.split(' ');
                pos_ls = list((int(pos[0]), int(pos[1])))
#                print(pos_ls)
                store_list.append(pos_ls)
                count = count - 1
                i += 1
                if(count == 0):
                    Flag = False
            else:
                pass    

# read file without comment
def read_file():
    clear_window()
    file = filedialog.askopenfile(initialdir="/", mode='r', title="Select file")
    Flag = False;
    global point_list
    global line_list
    global i
    global point_begin
    global point_end
    global ind
    point_begin = 0
    point_end = 0
    ind = 0
        
    while (file != None):
        f_str = file.readline()
        # file.readline()
        # print(f_str)

        f_list = list(f_str)
        print(f_list)
#             print(f_str)
        if(f_list[0] == "0" or f_list == []):
#             print(f_str)
            file.close
            break
        elif (f_str == '\n'):
            continue
        elif(f_list[0] == 'P'):
            # 拿掉P
            p = f_str[2:]
            # 切割兩點位置
            sp_point = p.split(" ")
            point_list.append([int(sp_point[0]), int(sp_point[1])])
        elif(f_list[0] == 'E'):
            # 拿掉E
            print(point_list)
            e = f_str[2:]
            sp_edge = e.split(" ")
            line_list.append([[int(sp_edge[0]), int(sp_edge[1])], [int(sp_edge[2]), int(sp_edge[3])]])
            print(line_list)
        elif(f_list[0] != '#'):
        # print(f_str,end='')
            if(Flag == False and int(f_str) > 0):
                count = int(f_str)
                Flag = True
                point_num.append(count)
                
            elif(Flag == True and count):
                pos = f_str.split(' ');
                pos_ls = list((int(pos[0]), int(pos[1])))
                print(pos_ls)
                store_list.append(pos_ls)
                count = count - 1
                i += 1
                if(count == 0):
                    Flag = False
            else:
                pass

# Write points to file 
def write_file():
    global point_list
    global line_list
    sort_point = sorted(point_list)
    sort_line = sorted(line_list)
    file = filedialog.asksaveasfile(initialdir="/", mode='w', title="Store file", defaultextension=".txt")
    if file is None:
        return
    # 寫入點
    for i in sort_point:
        print (type(i))
        str1 = str(i[0])
        str2 = str(i[1])
        file.write("P " + str1 + " " + str2 + "\n")
    # 寫入線段
    for i in sort_line:
        print (type(i))
        p1 = str(i[0][0])
        p2 = str(i[0][1])
        p3 = str(i[1][0])
        p4 = str(i[1][1])
        file.write("E " + p1 + " " + p2 + " " + p3 + " " + p4 + "\n")
    file.close()

# 讀取下一筆資料
def next_file():
    global ind
    global point_list
    global point_begin
    global point_end
    global point_num
    global line_list
    global endtest_lable
    if(point_end < len(store_list) and len(store_list) != 0):
        point_list = []
        line_list = []
        point_end += point_num[ind]
        for i in range(point_begin, point_end):
            point_list.append(store_list[i])
        point_begin += point_num[ind]
        ind += 1
    elif(point_end > 0 and point_begin > 0):
        endtest_lable.set_text("Just one is final test")
        pass    
    
# clear the window
def clear_window():
    global point_list
    global line_list
    point_list = []
    line_list = []
    endtest_lable.set_text("")
    frame.set_canvas_background("White") 
   
# helper function
def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# define event handler for mouse click, draw
def click(pos):
    point_list.append(list(pos))
    # print(pos)
    global i
    i += 1
    
#    if distance(point, pos) < ball_radius:
#        if ball_color == "Red":
#            ball_color = "Green"
#    else:
#        point = [pos[0], pos[1]]
#        ball_color = "Red"

# Draw the canvas 
def draw(canvas):
        global i
        i %= len(color_list)
        for point in point_list:
            canvas.draw_circle(point, ball_radius, 2, "Black", ball_color)
        for line in line_list:    
            canvas.draw_line(line[0], line[1], 2, "Navy")
#             frame.set_canvas_background(color_list[i])
#         canvas.draw_line([0,0], [height,width], 2, color_list[i])

# implement step by step
def step_by_step(canvas):
   pass


def list2int(numlist):
    return int(numlist[0])

def del_dup_point():
    global point_list
    del_point_list = []
    [del_point_list.append(i) for i in point_list  if not i in del_point_list]
    return del_point_list

# 修正 將 Fraction 轉型為 str 時會分母為1的情形 
# def fix_slope(sr):
#     if (len(sr) == 1 or len(sr) == 2):
#         return sr + "/1"
#     return sr

# 求內心 formula: A(x1，y1)，B(x2，y2)，C(x3，y3)，BC=a，AC=b，AB=c, then heart_point=( (ax1+bx2+cx3)/(a+b+c)，(ay1+by2+cy3)/(a+b+c) ) 
def heart(pa, pb, pc):
    global point_list
    dis_a = distance(pb, pc)
    dis_b = distance(pa, pc)
    dis_c = distance(pa, pb)
    
    # sum of triangal edge distance
    dis_sum = dis_a + dis_b + dis_c
    
    # 內心 點位置
    heart_point = [int((pa[0] * dis_a + pb[0] * dis_b + pc[0] * dis_c) / dis_sum), int((pa[1] * dis_a + pb[1] * dis_b + pc[1] * dis_c) / dis_sum)]
    
    # 檢查內心位址
    # point_list.append(heart_point)
    print("內心", heart_point)
    
    return heart_point 
     

# 求得兩向量交點
def intersection(a1, a2, b1, b2):
    a = a2 - a1
    b = b2 - b1
    s = b1 - a1
    return a1 + a * cross(s, b) / cross(a, b)

def point_line(point_ls):
    # 只有一點(終止條件)
    if(len(point_ls) == 1):
        print("---Only one point---")
        
    # 兩點(終止條件)     
    if(len(point_ls) == 2):
        print("---Two points---")
        
        # 處理當時進來的點
        point_l = point_ls 
        
        # 定義兩點
        a = np.array(point_l[0])
        b = np.array(point_l[1])
        
        # 求得兩點向量
        vector = a - b
        
        # 法向量
        nor_vector = np.array([vector[1], -vector[0]])
        
        # 兩點中點
        mid = [(point_l[1][0] + point_l[0][0]) / 2, (point_l[1][1] + point_l[0][1]) / 2]
        
        # 兩點平行，垂直線
        if(nor_vector[0] == 0):
            line_list.append([[mid[0], 0], [mid[0], 600]])
        # 兩點垂直，水平線
        elif(nor_vector[1] == 0):
            line_list.append([[0, mid[1]], [600, mid[1]]])
        # 任意兩點
        else:    
            # 畫線兩點
            up = mid
            down = mid
            while(up[0] >= 0 and up[1] >= 0 and up[0] <= 600 and up[1] <= 600):
                up = [up[0] - nor_vector[0] / 500, up[1] - nor_vector[1] / 500]
            while(down[0] >= 0 and down[1] >= 0 and down[0] <= 600 and down[1] <= 600):
                down = [down[0] + nor_vector[0] / 500, down[1] + nor_vector[1] / 500]
            
            print(up, down)
            line_list.append([[int(up[0]), int(up[1])], [int(down[0]), int(down[1])]])
        print(line_list)
            # 中垂線方程式
            
    # 三點(終止條件)     
    if(len(point_ls) == 3):
        print("---Three points---")
        
        # 初始化 點的位置
        a = np.array(point_ls[0])
        b = np.array(point_ls[1])
        c = np.array(point_ls[2])
        
        print("三點 : ",point_ls[0], point_ls[1], point_ls[2])
        
        # 三點平行共線(例外狀況 : 要先進行化簡)
        vector1 = b-a
        vector2 = c-b
        if(np.array_equal(vector1, vector2) or (vector1[0] / vector1[1] == vector2[0] / vector2[1])):
            point_line([point_ls[1], point_ls[0]])
            point_line([point_ls[2], point_ls[1]])
        else:
            # 求內心
            heart_point = heart(a, b, c)
        
            # 極座標找順序
            h2pa = math.atan2(heart_point[1] - a[1], heart_point[0] - a[0])
            h2pb = math.atan2(heart_point[1] - b[1], heart_point[0] - b[0])
            h2pc = math.atan2(heart_point[1] - c[1], heart_point[0] - c[0])
        
            # 極座標排序
            ordinate_in = [[h2pa, a], [h2pb, b], [h2pc, c]]
            print(h2pa, h2pb, h2pc)
            sorted_ordinate_in = sorted(ordinate_in)
            print(sorted_ordinate_in)
            #print(sorted_ordinate_in[0][1][0])
        
            # 求得兩點向量
            vector1 = sorted_ordinate_in[1][1] - sorted_ordinate_in[0][1]
            vector2 = sorted_ordinate_in[2][1] - sorted_ordinate_in[1][1]
            vector3 = sorted_ordinate_in[0][1] - sorted_ordinate_in[2][1]
        
            # 求法向量
            nor_vector1 = np.array([vector1[1], -vector1[0]])
            nor_vector2 = np.array([vector2[1], -vector2[0]])
            nor_vector3 = np.array([vector3[1], -vector3[0]])
            print("法向量", nor_vector1, nor_vector2, nor_vector3)
        
            # 兩點中點
            mid1 = [(sorted_ordinate_in[0][1][0] + sorted_ordinate_in[1][1][0]) / 2, (sorted_ordinate_in[0][1][1] + sorted_ordinate_in[1][1][1]) / 2]
            mid2 = [(sorted_ordinate_in[1][1][0] + sorted_ordinate_in[2][1][0]) / 2, (sorted_ordinate_in[1][1][1] + sorted_ordinate_in[2][1][1]) / 2]
            mid3 = [(sorted_ordinate_in[2][1][0] + sorted_ordinate_in[0][1][0]) / 2, (sorted_ordinate_in[2][1][1] + sorted_ordinate_in[0][1][1]) / 2]
            # mid2 = [(point_ls[1][0] + point_ls[2][0]) / 2, (point_ls[1][1] + point_ls[2][1]) / 2]
            # mid3 = [(point_ls[2][0] + point_ls[0][0]) / 2, (point_ls[2][1] + point_ls[0][1]) / 2]
            print(vector1 , vector2, vector3)
        
            # 求外心
            cir_point = circumcentre(mid1, mid2, nor_vector1, nor_vector2)
            cir_point2int = [int(cir_point[0]), int(cir_point[1])]
            print("外心 : " , cir_point2int)
        
        
            
            # 外心跑出邊框外
            if(cir_point[0] < 0 or cir_point[1] < 0 or cir_point[1] > 600 or cir_point[0] > 600):
                if(not np.array_equal(vector1, vector2)):
                    point_line([sorted_ordinate_in[0][1], sorted_ordinate_in[1][1]])
                    point_line([sorted_ordinate_in[1][1], sorted_ordinate_in[2][1]])
                else:
                    point_line([sorted_ordinate_in[1][1], sorted_ordinate_in[2][1]])
                    point_line([sorted_ordinate_in[0][1], sorted_ordinate_in[2][1]])
                    
            # 例外 : 三點不共線
            else:
            
            # point_list.append([round(cir_point[0],0), round(cir_point[1],0)]) 我只是拿來檢查外心的位置是否正確拉~
            
            # 判斷夾角
#                 ang_va1 = vector1[0] * vector3[0] + vector1[1] * vector3[1]
#                 ang_va2 = vector2[0] * vector3[0] + vector2[1] * vector3[1]
#                 ang_va3 = vector2[0] * vector1[0] + vector2[1] * vector1[1]
#                 print(ang_va1, ang_va2, ang_va3)
                
            # 向量方向 = 點向式 - 外心 
                out_vector1 = np.array(mid1) + np.array(nor_vector1) - np.array(cir_point2int)
                out_vector2 = np.array(mid2) + np.array(nor_vector2) - np.array(cir_point2int)
                out_vector3 = np.array(mid3) + np.array(nor_vector3) - np.array(cir_point2int)
                print("點向量:", out_vector1, out_vector2, out_vector3)
                
                #例外處理
                # -- -- --
                if(out_vector1[0]<0 and out_vector1[1]<0 and out_vector2[0]<0 and out_vector2[1]<0 and out_vector3[0]<0 and out_vector3[1]<0):
                    out_vector3=-out_vector3
                # +- +- +-
                if(out_vector1[0]>0 and out_vector1[1]<0 and out_vector2[0]>0 and out_vector2[1]<0 and out_vector3[0]>0 and out_vector3[1]<0):
                    out_vector1=-out_vector2
                # ++ ++ ++
                if(out_vector1[0]>0 and out_vector1[1]>0 and out_vector2[0]>0 and out_vector2[1]>0 and out_vector3[0]>0 and out_vector3[1]>0):
                    out_vector2=-out_vector2
                # -+ -+ -+
                if(out_vector1[0]<0 and out_vector1[1]>0 and out_vector2[0]<0 and out_vector2[1]>0 and out_vector3[0]<0 and out_vector3[1]>0):
                    out_vector3=-out_vector3
                # ++ ++ +-
                if(out_vector1[0]>0 and out_vector1[1]>0 and out_vector2[0]>0 and out_vector2[1]>0 and out_vector3[0]>0 and out_vector3[1]<0):
                    out_vector2=-out_vector2
                # -- -+ -+
                if(out_vector1[0]<0 and out_vector1[1]>0 and out_vector2[0]<0 and out_vector2[1]<0 and out_vector3[0]<0 and out_vector3[1]>0):
                    out_vector3=-out_vector3
                # +- +- ++ 
                if(out_vector1[0]>0 and out_vector1[1]<0 and out_vector2[0]>0 and out_vector2[1]<0 and out_vector3[0]>0 and out_vector3[1]>0):
                    out_vector1=-out_vector1
                    
#             if(ang_va3 == 0):
#                 if(point_list[2][1] > point_list[1][1]):
#                     if(out_vector1[0] == 0 and out_vector1[1] == 0):
#                         out_vector1 = np.array([-nor_vector1[0], -nor_vector1[1]])
#                     elif(out_vector2[0] == 0 and out_vector2[1] == 0):
#                         out_vector2 = np.array([-nor_vector2[0], -nor_vector2[1]])
#                     elif(out_vector3[0] == 0 and out_vector3[1] == 0):
#                         out_vector3 = np.array([nor_vector3[0], nor_vector3[1]])
#                 else:
#                     if(out_vector1[0] == 0 and out_vector1[1] == 0):
#                         out_vector1 = np.array([-nor_vector1[0], -nor_vector1[1]])
#                     elif(out_vector2[0] == 0 and out_vector2[1] == 0):
#                         out_vector2 = np.array([-nor_vector2[0], -nor_vector2[1]])
#                     elif(out_vector3[0] == 0 and out_vector3[1] == 0):
#                         out_vector3 = np.array([-nor_vector3[0], -nor_vector3[1]])
#             elif(ang_va1 == 0):
#                 if(out_vector1[0] == 0 and out_vector1[1] == 0):
#                     out_vector1 = np.array([-nor_vector1[0], -nor_vector1[1]])
#                 elif(out_vector2[0] == 0 and out_vector2[1] == 0):
#                     out_vector2 = np.array([-nor_vector2[0], -nor_vector2[1]])
#                 elif(out_vector3[0] == 0 and out_vector3[1] == 0):
#                     out_vector3 = np.array([-nor_vector3[0], -nor_vector3[1]])
#             else:
#                 if(out_vector1[0] == 0 and out_vector1[1] == 0):
#                     out_vector1 = np.array([nor_vector1[0], nor_vector1[1]])
#                 elif(out_vector2[0] == 0 and out_vector2[1] == 0):
#                     out_vector2 = np.array([-nor_vector2[0], -nor_vector2[1]])
#                 elif(out_vector3[0] == 0 and out_vector3[1] == 0):
#                     out_vector3 = np.array([-nor_vector3[0], -nor_vector3[1]])
            
            
            
            # 找交點(初始化)
                line1 = cir_point2int
                line2 = cir_point2int
                line3 = cir_point2int
            
            # 三向量找與邊框的交點
           
                while(line1[0] >= 0 and line1[1] >= 0 and line1[0] <= 600 and line1[1] <= 600):
                    line1 = [line1[0] + out_vector1[0] / 500, line1[1] + out_vector1[1] / 500]
                while(line2[0] >= 0 and line2[1] >= 0 and line2[0] <= 600 and line2[1] <= 600):
                    line2 = [line2[0] + out_vector2[0] / 500, line2[1] + out_vector2[1] / 500]
                while(line3[0] >= 0 and line3[1] >= 0 and line3[0] <= 600 and line3[1] <= 600):
                    line3 = [line3[0] + out_vector3[0] / 500, line3[1] + out_vector3[1] / 500]
            
            # 加入線的範圍, 將double 轉型 int 
                print(line1, line2, line3)
                line_list.append([[int(line1[0]), int(line1[1])], [int(cir_point2int[0]), int(cir_point2int[1])]])
                line_list.append([[int(line2[0]), int(line2[1])], [int(cir_point2int[0]), int(cir_point2int[1])]])
                line_list.append([[int(line3[0]), int(line3[1])], [int(cir_point2int[0]), int(cir_point2int[1])]])
                print(point_list)
                print(line_list)
            
# 內積求外心
def circumcentre(a1, b1, v1, v2):
    v3 = np.array(b1) - np.array(a1)
    return a1 + v1 * cross(v3, v2) / cross(v1, v2)
            
# Divide and Conquer
def divide_and_conquer():
    pass

# Start the Voronoi Diagram
def run():
    global point_list
#     point_list.append([487, 155])
#     point_list.append([498, 168])
#     point_list.append([502, 181])

    # del the duplicate point in the beginning
    point_list = del_dup_point()
    
    # sort the point before run
    point_list.sort()
    
    # process the relations between points and lines
    point_line(point_list)
    
# create frame
frame = simplegui.create_frame("Voronoi Diagram", width, height)

# initial canvas background
frame.set_canvas_background("White")

# register event handler
btm_start = frame.add_button("Run", run, 200);
lable1 = frame.add_label("\n", 1);
btm_start = frame.add_button("Step by step", step_by_step, 200);
lable1 = frame.add_label("\n", 1);
btm_fr_wc = frame.add_button("Read File(comment)", read_file_comment, 200);
lable2 = frame.add_label("\n", 1);
btm_fr_c = frame.add_button("Read File", read_file, 200);
lable4 = frame.add_label("\n", 1);
btm_fr_c = frame.add_button("Next", next_file, 200);
lable4 = frame.add_label("\n", 1);
btm_fr_wf = frame.add_button("Write File", write_file, 200);
lable3 = frame.add_label("\n", 1);
btm_clear = frame.add_button("Clear window", clear_window, 200);
lable3 = frame.add_label("\n", 1);
endtest_lable = frame.add_label("", 200)

# start frame
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.start()
