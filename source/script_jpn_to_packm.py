import testclasses
import pickle

with open('res01.txt', encoding='utf-8') as file:
    text = file.read()
rows = text.split('\n')
pairs = list(map(lambda e: e.split(), rows))
pairs = list(map(lambda e: (e[0], e[1]), pairs))
eq = {e[0]: e[1] for e in pairs}
print(eq)
test = testclasses.MatchTestPack(title='jpn', equals=eq)
with open('testJpnHiragana.fts23m', 'wb') as file:
    pickle.dump(test, file)