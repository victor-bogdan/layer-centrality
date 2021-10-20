

class LayerCentralityExcelModel:

    def __init__(
        self,
        sheet_title,
        dataframe,
        start_row,
        start_col,
        end_row,
        end_col
    ):

        self.sheet_title = sheet_title
        self.dataframe = dataframe.copy()
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
