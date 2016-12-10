def _move_value(source, target, key):
    if key in source:
        target[key] = source[key]
        del source[key]

def _to_float(arg):
    if arg is None:
        return None
    elif isinstance(arg, float):
        return arg
    elif isinstance(arg, list):
        return [_to_float(a) for a in arg]
    elif isinstance(arg, tuple):
        return list(_to_float(a) for a in arg) # Make lists from tuples
    elif isinstance(arg, str):
        if arg == "":
            return None
        elif arg == "-":
            return None
        else:
            return float(arg.replace(',', '.'))
    else:
        raise TypeError("Unhandled type: %s" % arg)
    
# TODO the rows (including the header) shold be tuples so we know that they
# can't change
    
class Table:
    ##################
    ## Construction ##
    ##################
     
    def __init__(self, header_row=None, data_rows=[], column_names=[]):
        self._header_row   = header_row
        self._data_rows    = data_rows
        self._column_names = column_names
        
        self._file_name = None

    @classmethod
    def from_csv(cls, *args, **kwargs):
        table = cls()
        table.read_csv(*args, **kwargs)
        return table
    
    @classmethod
    def from_excel(cls, *args, **kwargs):
        table = cls()
        table.read_excel(*args, **kwargs)
        return table


    #########
    ## I/O ##
    #########

    def read_csv(self, file_name, header=True, open_args={}, csv_args={}, **kwargs):
        import csv
 
        _move_value(kwargs, open_args, "newline")
        _move_value(kwargs, open_args, "encoding")
 
        _move_value(kwargs, csv_args, "dialect")
        _move_value(kwargs, csv_args, "delimiter")
        _move_value(kwargs, csv_args, "doublequote")
        _move_value(kwargs, csv_args, "escapechar")
        _move_value(kwargs, csv_args, "lineterminator")
        _move_value(kwargs, csv_args, "quotechar")
        _move_value(kwargs, csv_args, "quoting")
        _move_value(kwargs, csv_args, "skipinitialspace")
 
        with open(file_name, 'r', **open_args) as csvfile:
            csv_reader = csv.reader(csvfile, **csv_args)
            for row in csv_reader:
                if header and self._header_row is None:
                    self._header_row = row
                else:
                    self._data_rows.append(row)
                    
        if not self.all_rows_equal_length():
            raise NotImplementedError("Rows have different lengths")
        
        self._column_names = [None] * self.column_count()
        self._file_name = file_name
  
    def read_excel(self, file_name, sheet_name, header=True, open_workbook_options={}):
        import xlrd
        
        workbook = xlrd.open_workbook(file_name, **open_workbook_options)
        sheet = workbook.sheet_by_name(sheet_name)
  
        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            if header and self._header_row is None:
                self._header_row = row
            else:
                self._data_rows.append(row)

        if not self.all_rows_equal_length():
            raise NotImplementedError("Rows have different lengths")

        self._column_names = [None] * self.column_count()
        self._file_name = file_name


    #####################
    ## Table structure ##
    #####################

    def column_count(self):
        row_lengths = (len(row) for row in self.all_rows())
        return max(row_lengths)

    def data_row_count(self):
        return len(self._data_rows)

    def all_rows(self):
        if self._header_row is None:
            return self._data_rows
        else:
            return [self._header_row] + self._data_rows
    
    def all_rows_equal_length(self):
        all_row_lengths = [len(row) for row in self.all_rows()]
        
        if len(all_row_lengths) == 0:
            return True
        else:
            return all(l == all_row_lengths[0] for l in all_row_lengths)

    def setup_column(self, index, header=None, name=None, datatype=None, mapping=None):
        '''
        If mapping is specified, map_column wil be called with skip_none=True.
        If you need more control over the mapping, call map_column yourself.
        '''
        # TODO allow not specifying index, find by header 
        
        actual_header = self._header_row[index]
        if header is not None and actual_header != header:
            if self._file_name is not None:
                file_string = " of %s" % self._file_name
            else:
                file_string = ""
            raise ValueError("Header mismatch for column %s%s:\n    Expected: %s\n    Actual:   %s" %
                 (index, file_string, header, actual_header))
    
        if name is not None:
            self._column_names[index] = name

        if datatype == float:
            transform = _to_float
        else:
            transform = datatype 
            
        if transform is not None:
            for row in self._data_rows:
                row[index] = transform(row[index])

        if mapping is not None:
            self.map_column(index, mapping, skip_none = True)

    def resolve_column(self, columnspec):
        """Resolves a column and returns its index.
         
        The columns can be specified as:
          * an integer: used as the column index
          * a string: the first column with a matching name is used
        For other types, an exception is raised.
        """
        # TODO allow regular expressions; allow header?
        if isinstance(columnspec, int):
            index = columnspec
            if index >= self.column_count():
                raise ValueError("Column number {} out of range".format(index))
            return index
        elif isinstance(columnspec, str):
            name = columnspec
            if name not in self._column_names:
                raise ValueError('Column name "%s" does not exist' % name)
            return self._column_names.index(name)
        else:
            raise Exception("Invalid column specification {}".format(repr(columnspec)))

    def resolve_columns(self, columnspecs):
        return [self.resolve_column(columnspec) for columnspec in columnspecs]
    
    
    ################
    ## Table data ##
    ################

    def columns(self, columnspecs):
        '''
        Columns is any sequence of anything that resolve_column accepts.
        '''
        # TODO can we allow both columns([1,2,3]) and columns(1,2,3)?
        
        # Resolve the columns and construct the new header and data.
        indices = self.resolve_columns(columnspecs)
        
        map_fn = lambda row: [row[i] for i in indices]
        new_header       = map_fn(self._header_row)
        new_data         = list(map(map_fn, self._data_rows))
        new_column_names = map_fn(self._header_row)
        
        # Create the new table
        return Table(new_header, new_data, new_column_names)


    def filter(self, conditions):
        '''
        conditions is one of:
          - a function, taking as many arguments as the table has columns
          - { columnspec: value, ...}  (dict form)
            columnspec is anything supported by resolve_column
            value is a string
          - [(columnspec, value), ...] (list form)
        '''
        # TODO allow regular expressions or functions for value
        # TODO allow kwargs (with column names only)
        # TODO allow auto functions (with automatic parameter name matching)
        # TODO allow eval'd string expressions

        # A dictionary is converted to list form
        if isinstance(conditions, dict):
            conditions = list(conditions.items())

        # A function is called with the values of the row as arguments         
        if hasattr(conditions, '__call__'):
            def row_matches(row):
                return conditions(*row)
        elif isinstance(conditions, list):
            # Resolve the columns
            conditions=[(self.resolve_column(columnspec), value) for
                columnspec, value in conditions]
     
            def row_matches(row):
                for column_index, value in conditions:
                    if row[column_index]!=value:
                        return False
                return True
        else:
            raise ValueError("Unsupported conditions value: %s" % repr(conditions))

        # Create the resulting table. The header does not change.
        new_header       = list(self._header_row)
        new_data         = list(filter(row_matches, self._data_rows))
        new_column_names = list(self._column_names)
        return Table(new_header, new_data, new_column_names)

    def records(self, record_class):
        return [record_class(*row) for row in self._data_rows]

    def map_column(self, columnspec, function, skip_none = True):
        column_index = self.resolve_column(columnspec)
        
        for row in self._data_rows:
            value = row[column_index]
            if not (value is None and skip_none):
                row[column_index] = function(row[column_index])


    ################
    ## Conversion ##
    ################

    def format(self, column_separator="|", row_separator="\n", hlines=None):
        rows = self.all_rows()
 
        if hlines is None:
            hlines = self._header_row is not None
 
        def column_width(index):
            lengths=(len(str(row[index])) for row in rows)
            return max(lengths)
         
        column_widths=[column_width(index) for index in range(self.column_count())]
 
        # Format the header and data, row by row
        def format_row(row):
            formatted_values=[str(row[column_index]).ljust(column_widths[column_index]) for column_index in range(len(column_widths))]
            return column_separator.join(formatted_values)
            pass
         
        formatted_rows=[format_row(row) for row in rows]
         
        if hlines:
            total_width = sum(column_widths) + (len(column_widths)-1)*len(column_separator)
            hline = "-" * total_width
            formatted_rows.insert(0, hline)
            formatted_rows.insert(2, hline)
            formatted_rows.append(hline)
         
        return row_separator.join(formatted_rows)
 
    def __str__(self):
        if self._header_row is not None:
            return "Table with {} rows (plus header) and {} columns".format(self.data_row_count (), self.column_count ())
        else:
            return "Table with {} rows and {} columns".format(self.data_row_count(), self.column_count ())
