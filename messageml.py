def __group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.

    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)])


def serialize(obj):
    objType = obj['type']
    value = obj['value']

    if objType == 'text':
        lines = value.splitlines()
        joinedLines = "<br/>".join(lines)
        return joinedLines

    elif objType == 'image':
        return value

    elif objType == 'table':
        columns = value['columns']
        data = value['data']
        column_tds = map(lambda name: f"<td>{name}</td>", columns)
        column_section = f"<tr>{''.join(column_tds)}</tr>"
        
        data_tds = [
            *map(lambda dataObj: f"<td>{serialize(dataObj)}</td>", data)]
        data_rows = __group(data_tds, len(columns))
        data_rows_print = [
            *map(lambda tupleObj: f"<tr>{''.join(tupleObj)}</tr>", data_rows)]
        print([*data_rows_print])
        data_section = "".join(data_rows_print)
        return f"<table>{column_section}{data_section}</table>"

    return obj
