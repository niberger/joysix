import math

def sinox(x):
	'''sin(x)/x'''
	if(abs(x) > 1e-2):
		return math.sin(x) / x
	else:
		return 1 - x*x / 6 + x*x*x*x / 120

def cosox2(x):		
	'''(1-cos(x))/(x*x)'''
	if (abs(x) > 1e-2):			
		return (1. - math.cos(x)) / (x*x)		
	else:			
		return 0.5 - x*x / 24 + x*x*x*x / 720.

def sinox3(x):		
	'''(x-sin(x))/(x*x*x)'''
	if (abs(x) > 1e-2):			
		return (x - math.sin(x)) / (x*x*x)			
	else:			
		return 1./6. - x*x / 120. + x*x*x*x / 5040.

def specialFun1(x):		
	'''(x*sin(x) - 2.*(1.-cos(x)))/(x*x*x*x)'''
	if (abs(x) > 1e-2):			
		return (x*math.sin(x) - 2.*(1. - math.cos(x))) / (x*x*x*x)			
	else:			
		return -1./12. + x*x / 180. - x*x*x*x / 6720.

def specialFun2(x):		
	'''(2.*(1.-cos(x)) - x*sin(x))/(2.*x*x*(1.-cos(x)))'''
	if (abs(x) > 1e-2):			
		return (2.*(1. - math.cos(x)) - x*math.sin(x)) / (2.*x*x*(1. - math.cos(x)))			
	else:			
		return 1./12. + x*x / 720. + x*x*x*x / 30240.

def specialFun3(x):		
	'''(-2.*x + 3.*sin(x) - x*cos(x))/(x*x*x*x*x)'''
	if (abs(x) > 1e-2):			
		return (-2.*x + 3.*math.sin(x) - x*math.cos(x)) / (x*x*x*x*x)			
	else:			
		return - 1./60. + x*x / 1260. - x*x*x*x / 60480.

def specialFun4(x):		
	'''x*sin(x)/(2.*(1.-cos(x)))'''
	if (abs(x) > 1e-2):			
		return (x*math.sin(x)) / (2.*(1. - math.cos(x)))			
	else:			
		return 1. - x*x / 12. - x*x*x*x / 720.

