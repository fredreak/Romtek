# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:44:01 2021
@author: fredr
"""
import numpy as np
import matplotlib.pyplot as plt

def a(phi, N, m): #2501,8 - 9,81 = 2491,99
    return (N*np.cos(phi)/m, (N*np.sin(phi)/m-9.81))

def r_burn(t, a_x, a_y):
    return (0.9*(a_x**2)*(t**2), 0.9*(a_y**2)*(t**2))
    
def plot(x, y, x_label, y_label, style = "o-", c = "blue"):
    plt.figure()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, style, color = c)
    # plt.xticks(x, x_label[])
    plt.show()
    return 1

def main():
    #SET PARAMETERS
    phi = 60
    t_burnout = 2
    t_final =   300
    iterations = 500000
    N = 2501.8 #2501.8
    m = (13.308 - 8.496/2)

    #INITIALIZE
    iterations_burnout = round(iterations*(t_burnout/t_final))
    delta = t_final / iterations
    phi = phi * 2 * np.pi / 360
    a_x, a_y = a(phi, N, m)
    x_series = np.zeros(iterations+1)
    y_series = np.zeros(iterations+1)
    T = np.zeros(iterations+1)
    
    #ITERATE STAGE 1
    for i in range(1, iterations_burnout+1):
        T[i]=i*delta
        x_series[i], y_series[i] = r_burn(i*delta, a_x, a_y)
    x_0, y_0 =x_series[iterations_burnout],y_series[iterations_burnout]
    v_0_x, v_0_y = 0.9*a_x*T[iterations_burnout], 0.9*a_y*T[iterations_burnout]
    print("Vx, Vy ", v_0_x, "\n", v_0_y)
    
    #ITERATE STAGE 2 
    for i in range(1, iterations - iterations_burnout): #t = 0 bør svare til at du er i burnout
        t = i*delta
        true_i = i+iterations_burnout
        y_new = y_0 + v_0_y*t - 9.81 * t**2
        if(y_new < 0): #BREAK IF y<0. 
            print("Broken")
            T = T[:(true_i)]
            x_series, y_series = x_series[:(true_i)], y_series[:(true_i)]
            break
        T[(i+iterations_burnout)]=true_i*delta
        x_series[true_i], y_series[true_i] = (x_0 + v_0_x*t), y_new
       
    #Plot
    plot(x_series,y_series, "x", "y", "-")
    plot(T, y_series, "T", "y", "-")
    plot(T, x_series, "T", "x", "-")
    
print("Romtek ran as ", __name__)
if __name__ == "__main__":
    main()
