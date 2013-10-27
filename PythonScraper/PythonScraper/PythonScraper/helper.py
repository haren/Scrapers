class Helper:
    @classmethod
    def isReal(self, txt):
        try:
            txt = ''.join(txt.replace(',','.').strip().split())
            float(txt)
            return True
        except ValueError:
            return False