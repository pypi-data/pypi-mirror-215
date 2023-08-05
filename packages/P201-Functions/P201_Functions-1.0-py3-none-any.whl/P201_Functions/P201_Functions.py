"""
This module contains the following functions:

constant_fit_plot()
constant_fit_plot_errors()

linear_fit_plot()
linear_fit_plot_errors()

quadratic_fit_plot()
quadratic_fit_plot_errors()

exp_fit_plot()
charging_fit_plot()

weighted_average()
set_dark_mode()

More information on each of these functions are included in their function-specific docstrings!
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

reg = linear_model.LinearRegression()

from scipy.optimize import curve_fit

def constantfitfunction(x,*paramlist):
    return paramlist[0]

def constant_fit_plot_core(xi,yi,labelstring="Constant Fit",linestring="r-",plot_name=plt):
    
    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(1)]
    popt, pcov = curve_fit(constantfitfunction,xi,yi,p0=init_vals)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([constantfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,16.0,axis=0)
    upper = np.percentile(ysample,84.0,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f)" % (labelstring,popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[0],perr[0]

def constant_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Constant Fit",linestring="r-"):
    """
    constant_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Constant Fit",linestring="r-")
    
    Fits a set of (x,y) data with a constant function, y = C.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        y-intercept, error in y-intercept
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        intercept,dintercept = constant_fit_plot_core(xi,yi,labelstring,linestring)
        return intercept,dintercept
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return 1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            # Takes the x and y values to make a trendline
            intercept,dintercept = constant_fit_plot_core(x_data_cut,y_data_cut,labelstring,linestring,plot_name)
            return intercept,dintercept
        
def constant_fit_plot_errors_core(xi,yi,sigmai,labelstring="Constant Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(1)]
    popt, pcov = curve_fit(constantfitfunction,xi,yi,p0=init_vals,sigma=sigmai,absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,100)
    ysample=np.asarray([constantfitfunction(xi,*pi) for pi in ps])
    
    #print(ps,ysample)

    lowerc = np.percentile(ysample,16.0,axis=0)
    upperc = np.percentile(ysample,84.0,axis=0)
    middlec = (lowerc+upperc)/2.0
    
    lower = [lowerc for i in range(len(xi))]
    upper = [upperc for i in range(len(xi))]
    middle = [middlec for i in range(len(xi))]

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f)" % (labelstring,popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[0],perr[0]

def constant_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Constant Fit",linestring="r-"):
    """
    constant_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Constant Fit",linestring="r-")
    
    Fits a set of (x,y) data, with errors on the y values, with a constant function, y = C.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        sigmai: array of errors in the y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        y-intercept, error in y-intercept
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        intercept,dintercept = constant_fit_plot_errors_core(xi,yi,sigmai,labelstring,linestring)
        return intercept,dintercept
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            sigmai_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
                    sigmai_cut.append(sigmai[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            sigmai_cut = np.array(sigmai_cut)
            # Takes the x and y values to make a trendline
            intercept,dintercept = constant_fit_plot_errors_core(x_data_cut,y_data_cut,sigmai_cut,labelstring,linestring,plot_name)
            return intercept,dintercept

def linearfitfunction(x,*paramlist):
    return paramlist[0]+paramlist[1]*x

def linear_fit_plot_core(xi,yi,labelstring="Linear Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(2)]
    popt, pcov = curve_fit(linearfitfunction,xi,yi,p0=init_vals)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([linearfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,16.0,axis=0)
    upper = np.percentile(ysample,84.0,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f) x + (%0.5f +/- %0.5f)" % (labelstring,popt[1],perr[1],popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[0],popt[1],perr[0],perr[1]

def linear_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Linear Fit",linestring="r-"):
    """
    linear_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Linear Fit",linestring="r-")
    
    Fits a set of (x,y) data with a linear function, y = mx + b.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        y-intercept, slope, error in y-intercept, error in slope
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        intercept,slope,dintercept,dslope = linear_fit_plot_core(xi,yi,labelstring,linestring)
        return intercept,slope,dintercept,dslope
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            # Takes the x and y values to make a trendline
            intercept,slope,dintercept,dslope = linear_fit_plot_core(x_data_cut,y_data_cut,labelstring,linestring,plot_name)
            return intercept,slope,dintercept,dslope
        
def linear_fit_plot_errors_core(xi,yi,sigmai,labelstring="Linear Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(2)]
    popt, pcov = curve_fit(linearfitfunction,xi,yi,p0=init_vals,sigma=sigmai,absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([linearfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,2.5,axis=0)
    upper = np.percentile(ysample,97.5,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f) x + (%0.5f +/- %0.5f)" % (labelstring,popt[1],perr[1],popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[0],popt[1],perr[0],perr[1]

def linear_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Linear Fit",linestring="r-"):
    """
    linear_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Linear Fit",linestring="r-")
    
    Fits a set of (x,y) data, with errors on the y values, with a linear function, y = mx + b.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        sigmai: array of errors in the y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        y-intercept, slope, error in y-intercept, error in slope
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        intercept,slope,dintercept,dslope = linear_fit_plot_errors_core(xi,yi,sigmai,labelstring,linestring)
        return intercept,slope,dintercept,dslope
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            sigmai_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
                    sigmai_cut.append(sigmai[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            sigmai_cut = np.array(sigmai_cut)
            # Takes the x and y values to make a trendline
            intercept,slope,dintercept,dslope = linear_fit_plot_errors_core(x_data_cut,y_data_cut,sigmai_cut,labelstring,linestring,plot_name)
            return intercept,slope,dintercept,dslope
        
def quadraticfitfunction(x,*paramlist):
    return paramlist[0]+paramlist[1]*x+paramlist[2]*x*x
        
def quadratic_fit_plot_core(xi,yi,labelstring="Quadratic Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(3)]
    popt, pcov = curve_fit(quadraticfitfunction,xi,yi,p0=init_vals)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([quadraticfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,16.0,axis=0)
    upper = np.percentile(ysample,84.0,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f) x^2 + (%0.5f +/- %0.5f) x + (%0.5f +/- %0.5f)" %(labelstring,popt[2],perr[2],popt[1],perr[1],popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[2],popt[1],popt[0],perr[2],perr[1],perr[0]
           
def quadratic_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Quadratic Fit",linestring="r-"):
    """
    quadratic_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Quadratic Fit",linestring="r-")
    
    Fits a set of (x,y) data with a quadratic function, y = ax^2 + bx + c.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        a,b,c,error in a, error in b, error in c
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        a,b,c,da,db,dc = quadratic_fit_plot_core(xi,yi,labelstring,linestring,plot_name)
        return a,b,c,da,db,da
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            # Takes the x and y values to make a trendline
            a,b,c,da,db,dc = quadratic_fit_plot_core(x_data_cut,y_data_cut,labelstring,linestring,plot_name)
            return a,b,c,da,db,dc
        
def quadratic_fit_plot_errors_core(xi,yi,sigmai,labelstring="Quadratic Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [0.0 for x in range(3)]
    popt, pcov = curve_fit(quadraticfitfunction,xi,yi,p0=init_vals,sigma=sigmai,absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([quadraticfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,16.0,axis=0)
    upper = np.percentile(ysample,84.0,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f) x^2 + (%0.5f +/- %0.5f) x + (%0.5f +/- %0.5f)" %(labelstring,popt[2],perr[2],popt[1],perr[1],popt[0],perr[0]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt[2],popt[1],popt[0],perr[2],perr[1],perr[0]
           
def quadratic_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Quadratic Fit",linestring="r-"):
    """
    quadratic_fit_plot_errors(xi,yi,sigmai,plot_name,x_low="",x_high="",labelstring="Quadratic Fit",linestring="r-")
    
    Fits a set of (x,y) data, with errors on the y values, with a quadratic function, y = ax^2 + bx + c.
    
    Arguments:
        xi: array of x values
        yi: array of y values
        sigmai: array of errors in the y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        a,b,c,error in a, error in b, error in c
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        a,b,c,da,db,dc = quadratic_fit_plot_errors_core(xi,yi,sigmai,labelstring,linestring,plot_name)
        return a,b,c,da,db,da
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            sigmai_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
                    sigmai_cut.append(sigmai[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            sigmai_cut = np.array(sigmai_cut)
            # Takes the x and y values to make a trendline
            a,b,c,da,db,dc = quadratic_fit_plot_errors_core(x_data_cut,y_data_cut,sigmai_cut,labelstring,linestring,plot_name)
            return a,b,c,da,db,dc
        
def weighted_average(x,deltax,etype):
    """
    weighted_average(x,deltax,etype)
    
    Calculate the weighted average, along with statistical, systematic, and total error
    in the weighted average, for an array of values with uncertainties.
    
    Arguments:
        x: array of values
        deltax: array of uncertainties in the values
        etype: error type ... 1=uniform, 2=Gaussian
    Returns
        x_bar, dx_bar_statistical, dx_bar_systematic, dx_bar
    """
    
    if (etype == 1):
        w = 1/deltax
    else:
        w = 1/deltax**2
    
    # calculate the statistically weighted average of density
    sq_sum1 = 0.0
    sq_sum2 = 0.0
    sq_sum3 = 0.0
    sq_sum4 = 0.0
    sq_sum5 = 0.0
    
    for i in range(len(x)):
        sq_sum1 = sq_sum1 + w[i]*x[i]
        sq_sum2 = sq_sum2 + w[i]
        sq_sum3 = sq_sum3 + w[i]*x[i]**2
        sq_sum4 = sq_sum4 + w[i]
        sq_sum5 = sq_sum5 + w[i]**2
                   
    xbar = sq_sum1/sq_sum2
    delta_xbar_stat = np.sqrt((np.abs(sq_sum3/sq_sum2 - xbar**2))/(len(x)-1))
    
    if (etype == 1):
        delta_xbar_syst = len(x)/sq_sum2
    else:
        delta_xbar_syst = np.sqrt(len(x))/sq_sum2
        
    if (etype==1):
        delta_xbar = delta_xbar_stat+delta_xbar_syst
    else:
        delta_xbar = np.sqrt(delta_xbar_stat**2+delta_xbar_syst**2)
    
    return xbar,delta_xbar_stat,delta_xbar_syst,delta_xbar

def set_dark_mode(dark_mode = True):
    """
    set_dark_mode(dark_mode = True)
    
    Turns on/off dark mode!
    
    Arguments:
        dark_mode: boolean -> True or False
    Returns
        Nothing!
    """
    if (dark_mode):
        from jupyterthemes import jtplot
        jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False)
        linecolor = 'w'
    else:
        linecolor = 'k'

def expfitfunction(x,*paramlist):
    return paramlist[0]*np.exp(paramlist[1]*(x-start_year))

def exp_fit_plot_core(xi,yi,labelstring="Exponential Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    
    init_vals = [1000.0,0.0069]
    popt, pcov = curve_fit(expfitfunction,xi,yi,p0=init_vals)
    perr = np.sqrt(np.diag(pcov))

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([expfitfunction(xi,*pi) for pi in ps])

    lower = np.percentile(ysample,16.0,axis=0)
    upper = np.percentile(ysample,84.0,axis=0)
    middle = (lower+upper)/2.0

    print("%s: Coefficients (from curve_fit)" % labelstring)
    print (popt)
    print("%s: Covariance Matrix (from curve_fit)" % labelstring)
    print (pcov)

    print()
    print ("%s: Final Result: y = (%0.5f +/- %0.5f) e^((%0.5f +/- %0.5f)(x-1994))" % (labelstring,popt[0],perr[0],popt[1],perr[1]))
    print()

    #plt.plot(xi,yi,'o')

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)

    return popt,pcov,perr

def exp_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Exponential Fit",linestring="r-"):
    """
    exp_fit_plot(xi,yi,plot_name,x_low="",x_high="",labelstring="Exponential Fit",linestring="r-"):
    
    Fits a set of (x,y) data with a exponential function, y = Ae^(B(x-C)).
    
    Arguments:
        xi: array of x values
        yi: array of y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        popt - array of parameter values (A, B, C)
	pcov - covariance matrix (3 x 3)
	perr - array of uncertainty values (dA, dB, dC)
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        popt,pcov,perr = exp_fit_plot_core(xi,yi,labelstring,linestring)
        return popt,pcov,perr
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            y_data_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    y_data_cut.append(yi[i])
            x_data_cut = np.array(x_data_cut)
            y_data_cut = np.array(y_data_cut)
            # Takes the x and y values to make a trendline
            popt,pcov,perr = exp_fit_plot_core(x_data_cut,y_data_cut,labelstring,linestring,plot_name)
            return popt,pcov,perr

from scipy.odr import *

def chargingfitfunction(B,x):
    return B[0]*(1.0-np.exp(-(x-B[1])/B[2]))

def charging_fit_plot_core(xi,yi,sigmaxi,sigmayi,labelstring="Charging Exponential Fit",linestring="r-",plot_name=plt):

    linestring2 = linestring+"-"
    tlow = xi[0]

    charging = Model(chargingfitfunction) # create a Model object based on the fitfuncion we have defined
    mydata = RealData(xi, yi, sx=sigmaxi, sy=sigmayi) # create a data object based on our data, include errors.
    myodr = ODR(mydata, charging, beta0=[10.00, tlow, 2.2]) # create a fitting object, based on the data, fit Model, and an intial set of parameters.
    myoutput = myodr.run()  # run the fitting process to get optimized parameters!

    myoutput.pprint() # print out the result of the fit

    # Now assign the important fit results to some more convenient variables.

    popt = myoutput.beta # the vector of optimized parameters
    pcov = myoutput.cov_beta # the covariance matrix
    perr = myoutput.sd_beta # the vector of ERRORS in the optimized parameters

    # The following lines generate upper and lower 99% "Confidence Bands" on the fit, for visualization
    # purposes.

    ps = np.random.multivariate_normal(popt,pcov,10000)
    ysample=np.asarray([chargingfitfunction(pi,xi) for pi in ps])

    lower = np.percentile(ysample,0.5,axis=0)
    upper = np.percentile(ysample,99.5,axis=0)
    middle = (lower+upper)/2.0

    print()
    print ("Final Result: Y = (%0.9f +/- %0.9f) (1 - EXP(-(X - (%0.9f +/- %0.9f))/(%0.9f +/- %0.9f)))" % (popt[0],perr[0],popt[1],perr[1],popt[2],perr[2]))

    plot_name.figure(figsize=(8, 6), dpi=80)

    plot_name.errorbar(xi, yi, xerr=sigmaxi, yerr=sigmayi)

    plot_name.plot(xi,middle,linestring,label=labelstring,linewidth=1)
    plot_name.plot(xi,lower,linestring2,linewidth=1)
    plot_name.plot(xi,upper,linestring2,linewidth=1)
    
    return popt,pcov,perr

def charging_fit_plot(xi,yi,sigmaxi,sigmayi,plot_name,x_low="",x_high="",labelstring="Charging Function Fit",linestring="r-"):
    """
    charging_fit_plot(xi,yi,sigmaxi,sigmayi,plot_name,x_low="",x_high="",labelstring="Charging Function Fit",linestring="r-"):
    
    Fits a set of (x,y) data with a exponential function, y = A(1 - e^(-(x-B)/C)).
    
    Arguments:
        xi: array of x values
        yi: array of y values
	sigmaxi: array of errors in x values
	sigmayi: array of errors in y values
        plot_name: matlibpolot.pylot plot name
        x_low: lower x limit of fit (optional)
        x_high: upper x limit of fit (optional)
        label_string: Label for plotted data (optional)
        line_string: Python plotting code for plot symbol and color (optional)
    Returns:
        popt - array of parameter values (A, B, C)
	pcov - covariance matrix (3 x 3)
	perr - array of uncertainty values (dA, dB, dC)
    """
    if x_low=="":
        # Takes the x and y values to make a trendline
        popt,pcov,perr = charging_fit_plot_core(xi,yi,sigmaxi,sigmayi,labelstring,linestring)
        return popt,pcov,perr
    else:
        if x_high=="":
            print ('Missing x_high parameter!!')
            return -1000,-1000,-1000,-1000
        else:
            x_data_cut = []
            dx_data_cut = []
            y_data_cut = []
            dy_data_cut = []
            for i in range(len(xi)):
                if xi[i]>=float(x_low) and xi[i]<=float(x_high):
                    x_data_cut.append(xi[i])
                    dx_data_cut.append(sigmaxi[i])
                    y_data_cut.append(yi[i])
                    dy_data_cut.append(sigmayi[i])
            x_data_cut = np.array(x_data_cut)
            dx_data_cut = np.array(dx_data_cut)
            y_data_cut = np.array(y_data_cut)
            dy_data_cut = np.array(dy_data_cut)
            # Takes the x and y values to make a trendline
            popt,pcov,perr = charging_fit_plot_core(x_data_cut,y_data_cut,dx_data_cut,dy_data_cut,labelstring,linestring,plot_name)
            return popt,pcov,perr

