
from google.cloud import bigtable
from google.cloud.bigtable.row_set import RowSet

client = bigtable.Client()


def bigtable_read_data(request):
    instance = client.instance(request.headers.get("instance_id"))
    table = instance.table(request.headers.get("table_id"))

    prefix = 'phone#'
    end_key = prefix[:-1] + chr(ord(prefix[-1]) + 1)

    outputs = []
    row_set = RowSet()
    row_set.add_row_range_from_keys(prefix.encode("utf-8"),
                                    end_key.encode("utf-8"))

    rows = table.read_rows(row_set=row_set)
    for row in rows:
        output = 'Rowkey: {}, os_build: {}'.format(
            row.row_key.decode('utf-8'),
            row.cells["stats_summary"]["os_build".encode('utf-8')][0]
            .value.decode('utf-8'))
        outputs.append(output)

    return '\n'.join(outputs)


