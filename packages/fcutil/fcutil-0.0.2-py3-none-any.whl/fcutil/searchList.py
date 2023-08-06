class searchList:

    index = {}
    
    def __init__(self, data: list, fields: list):
        self.index = {}
        for item in data:
            # Crea una chiave univoca per i campi che stai filtrando
            key = tuple(item[field] for field in fields)
            if key not in self.index:
                self.index[key] = []
            self.index[key].append(item)
        self.index
    
    def filter_data(self, values: list):
        key = tuple(values)
        return self.index.get(key, [])
