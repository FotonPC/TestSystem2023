class MapQuizPackFile:
    def __init__(self, mode=None, size=None, data=None, labels=None, title='', tnx_txt=''):
        self.mode = mode
        self.size = size
        self.data = data
        self.labels = labels
        self.title = title
        self.thanks_text = tnx_txt

    def __str__(self):
        res1 = []
        for k in self.labels.keys():
            res1.append(f"[{k}] - [{self.labels[k]}]")
        res1 = '\n'.join(res1)
        res = f"""
    ====== Main =======
    TITLE: [{self.title}]
    TNX_TXT: [{self.thanks_text}
    ====== Image ======
    MODE: [{self.mode}]
    SIZE: [{self.size[0]}px]x[{self.size[1]}px]
    DATA: [{len(self.data)}] BYTES
    ====== Labels =====
    {res1}
        """
        return res
    def img(self):
        return self.data, self.size, self.mode
