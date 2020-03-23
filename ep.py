import ep_model as epm
import ep_csv_importer as epi
from datetime import datetime, date, time, timedelta


def preprocess_matrix(context):
    """Prepares matrix suitable for easy serialization into HTML, XLS, etc."""

    # Some constant; TODO: Move to params
    day_start = datetime.combine(date.min, time(8, 0))
    day_end = datetime.combine(date.min, time(10, 0))
    interval = 15  # minimum time interval in minutes

    row_offset = 2
    col_offset = 1

    total_rows = row_offset + (day_end - day_start).seconds // 60 // interval
    total_cols = col_offset + \
        sum([e.days_count for e in context.events.values()])

    # initialization of empty matrix
    matrix = []
    for r in range(total_rows):
        row = []
        for c in range(total_cols):
            row.append(None)
        matrix.append(row)

    matrix[0][0] = ("", 1, 1)
    matrix[1][0] = ("", 1, 1)

    t_caption = day_start
    for t in range(row_offset, total_rows):
        matrix[t][0] = (t_caption.time(), 1, 1)
        t_caption += timedelta(minutes=15)

    skip_cols = col_offset
    for e in context.events.values():
        # header - events name
        pos_x = 0
        pos_y = skip_cols
        # each cell will be reprented by tuple (object, rowspan, colspan)
        matrix[pos_x][pos_y] = (e, 1, e.days_count)

        for d in range(e.days_count):
            # header - events dates
            day_start = datetime.combine(e.get_date(d).date(), time(8, 0))
            matrix[1][pos_y+d] = (e.get_date(d), 1, 1)
            for a in e.get_day_activities(d):
                x = (a.start - day_start).seconds // 60 // interval
                rowspan = (a.end - a.start).seconds // 60 // interval
                matrix[row_offset+x][pos_y+d] = (a, rowspan, 1)
                ...

        skip_cols += e.days_count

    return matrix


def serialize_html_matrix(matrix):
    """Really ugly implementation of HTML serialization. Just for a quick
    proof of concept. Refactoring strongly needed."""
    with open("test.html", mode="w") as file:
        file.write('<html><body><table border="1">')

        for row in matrix:
            file.write("<tr>")
            for col in row:
                if col:
                    file.write(
                        '<td rowspan="{}"  colspan="{}">'.format(col[1], col[2])
                    )
                    if type(col[0]) == epm.Event:
                        file.write(col[0].name)
                    if type(col[0]) == epm.Activity:
                        file.write(col[0].name)
                    if type(col[0]) == datetime:
                        file.write(col[0].date().isoformat())
                    if type(col[0]) == time:
                        file.write(col[0].isoformat())
                    if type(col[0]) == str:
                        file.write(col[0])
                    file.write('</td>')
            file.write("</tr>")

        file.write("</table></body></table>")


if __name__ == "__main__":
    context = epm.EPContext()
    epi.import_default_files("test_data", context)
    matrix = preprocess_matrix(context)
    serialize_html_matrix(matrix)
    ...
