import os
if not __path__.exists('data'):
 os.mkdir('data')
for i in range (10):
    os.rename(f'data/{i} day',f'data/{i+1} day')
