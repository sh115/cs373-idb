import time

# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1383004800)))
reg_time = time.strftime('%m-%d-%Y', time.gmtime(1414454400))
print(reg_time)