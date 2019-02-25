from collections import OrderedDict
import datetime

def transform_builds_table_output(result):
    table_output = []
    for item in result:
        table_output.append(_transform_build_row(item))
    return table_output


def transform_build_table_output(result):
    """
    Prepares overall build table for ouput
    """
    table_output = [_transform_build_row(result)]
    return table_output


def _transform_build_row(row):
    """
    Prepares individual build rows for output
    """
    REF_HEADS_PREFIX = 'refs/heads/'
    table_row = OrderedDict()
    table_row['Build Number'] = row.build_number
    table_row['Definition Name'] = row.definition.name
    table_row['Status'] = row.status
    table_row['Reason'] = row.reason
    if row.result:
        table_row['Result'] = row.result
    else:
        table_row['Result'] = ' '
    table_row['Definition ID'] = row.definition.id
    table_row['Definition Name'] = row.definition.name

    if row.source_branch:
        source_branch = row.source_branch
        if source_branch[0:len(REF_HEADS_PREFIX)] == REF_HEADS_PREFIX:
            source_branch = source_branch[len(REF_HEADS_PREFIX):]
        table_row['Source Branch'] = source_branch
    else:
        table_row['Source Branch'] = ' '

    table_row['Repository'] = {}
    table_row['Repository']['Name'] = row.repository.name
    table_row['Repository']['ID'] = row.repository.id
    table_row['Repository']['Type'] = row.repository.type
    table_row['Repository']['URL'] = row.repository.url

    table_row['Agent Pool'] = {}
    table_row['Agent Pool']['ID'] = row.queue.pool.id
    table_row['Agent Pool']['Name'] = row.queue.pool.name

    table_row['Queue'] = {}
    table_row['Queue']['Queue Time'] = row.queue_time.strftime('%a, %d %B %Y - %H:%M:%S %Z')
    table_row['Queue']['Start Time'] = row.start_time.strftime('%a, %d %B %Y - %H:%M:%S %Z')
    table_row['Queue']['Finish Time'] = row.finish_time.strftime('%a, %d %B %Y - %H:%M:%S %Z')
    table_row['Queue']['Duration'] = str(row.finish_time - row.start_time)
    return table_row


def transform_build_tags_output(result):
    table_output = []
    for item in result:
        table_output.append(_transform_build_tags_row(item))
    return table_output


def _transform_build_tags_row(row):
    table_row = OrderedDict()
    table_row['Tags'] = row
    return table_row


def transform_definitions_table_output(result):
    table_output = []
    include_draft_column = False
    for item in result:
        if item['quality'] == 'draft':
            include_draft_column = True
            break
    for item in result:
        table_output.append(_transform_definition_row(item, include_draft_column))
    return table_output


def transform_definition_table_output(result):
    table_output = [_transform_definition_row(result, result.quality == 'draft')]
    return table_output


def _transform_definition_row(row, include_draft_column=False):
    table_row = OrderedDict()
    table_row['ID'] = row.id
    table_row['Name'] = row.name
    table_row['Authored By'] = row.authored_by.display_name
    table_row['Created Date'] = row.created_date.strftime('%a, %d %B %Y - %H:%M:%S %Z')

    table_row['Repository'] = {}
    table_row['Repository']['Name'] = row.repository.name
    table_row['Repository']['ID'] = row.repository.id
    table_row['Repository']['Type'] = row.repository.type
    table_row['Repository']['URL'] = row.repository.url


    table_row['Pool'] = {}
    table_row['Pool']['ID'] = row.queue.pool.id
    table_row['Pool']['Name'] = row.queue.pool.name

    table_row['Retention Policy'] = []
    for item in range(len(row.retention_rules)):
        table_row['Retention Policy'].append({'Days to Keep': row.retention_rules[item].days_to_keep,
                                              'Minium to Keep': row.retention_rules[item].minimum_to_keep})

    table_row['Triggers'] = []
    for item in range(len(row.triggers)):
        table_row['Triggers'].append(row.triggers[item])

    if include_draft_column:
        if row.quality == 'draft':
            table_row['Draft'] = True
        else:
            table_row['Draft'] = ' '
    if row.queue_status:
        table_row['Queue Status'] = row.queue_status
    else:
        table_row['Queue Status'] = ' '
    if row.queue:
        table_row['Default Queue'] = row.queue.name
    else:
        table_row['Default Queue'] = ' '
    return table_row


def transform_tasks_table_output(result):
    table_output = []
    for item in sorted(result, key=_get_task_key):
        table_output.append(_transform_task_row(item))
    return table_output


def transform_task_table_output(result):
    table_output = [_transform_task_row(result)]
    return table_output


def _transform_task_row(row):
    table_row = OrderedDict()
    table_row['ID'] = row['id']
    table_row['Name'] = row['name']
    table_row['Author'] = row['author']
    table_row['Version'] = '.'.join([str(row['version']['major']),
                                     str(row['version']['minor']),
                                     str(row['version']['patch'])])
    if row['version']['isTest']:
        table_row['Version'] += '*'
    return table_row


def _get_task_key(row):
    return row['name'].lower()


def transform_releases_table_output(result):
    table_output = []
    for item in result:
        table_output.append(_transform_release_row(item))
    return table_output


def transform_release_table_output(result):
    table_output = [_transform_release_row(result)]
    return table_output


def _transform_release_row(row):
    table_row = OrderedDict()
    table_row['ID'] = row['id']
    table_row['Name'] = row['name']
    table_row['Definition Name'] = row['releaseDefinition']['name']
    table_row['Created By'] = row['createdBy']['displayName']
    created_on = dateutil.parser.parse(row['createdOn']).astimezone(dateutil.tz.tzlocal())
    table_row['Created On'] = str(created_on.date()) + ' ' + str(created_on.time())
    table_row['Status'] = row['status']
    table_row['Description'] = row['description']
    return table_row


def transform_release_definitions_table_output(result):
    table_output = []
    for item in result:
        table_output.append(_transform_release_definition_row(item))
    return table_output


def transform_release_definition_table_output(result):
    table_output = [_transform_release_definition_row(result)]
    return table_output


def _transform_release_definition_row(row):
    table_row = OrderedDict()
    table_row['ID'] = row['id']
    table_row['Name'] = row['name']
    table_row['CreatedBy'] = row['createdBy']['displayName']
    table_row['Created On'] = row['createdOn']
    return table_row