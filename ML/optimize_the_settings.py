#%%
import numpy as np
import itertools
test=[['fast', 10, 24],
      ['slow', 20, 52],
      ['signal', 6, 16],
      ['source', 'low', 'high', 'close', 'open', 'hl2', 'hlc3', 'ohlc4'],
      ['MA', 'ema', 'sma', 'wma']
      ]

print(np.shape(test))

# fast, slow, signal, source, MA type
# (10, 24),(20,52),(6,16),(low, high, close, open, hl2, hlc3, ohlo4), (ema, sma, wma)

#%%
adad=[]
for i in range(len(test)):
      if isinstance(test[i][1],int):
            adad.append(np.arange(test[i][1], test[i][2]+1, 1).tolist())
      elif isinstance(test[i][1], str):
            adad.append((test[i])[1:])

print(adad)
#%%
elements=[]
for element in itertools.product(adad[0],adad[1],adad[2],adad[3],adad[4]):

      elements.append(list(element))

#%%
print(elements)


