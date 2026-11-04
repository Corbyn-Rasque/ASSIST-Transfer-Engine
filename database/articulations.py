'''
Loads ASSIST articulations into the AND/OR expression tables defined in
`database/schema/articulations.sql`.

ASSIST describes the sending side of an articulation in two layers:

- Course groups, each joining its courses with `courseConjunction`.
- `courseGroupConjunctions`, which join the groups. These are position ranges
  ("groups 0 through 1 are joined by Or") rather than a tree.

`flatten` turns both layers, plus the receiving course or series, into
expression trees. It works on plain dicts (raw ASSIST JSON, or a parsed
model's `model_dump(mode = 'json')`), so it's independent of the parsing layer.

Usage:

    from database.engine        import engine
    from database.articulations import flatten, save

    rows = flatten('76/124/to/11/AllMajors', result['articulations'])
    with engine.begin() as connection:
        save(connection, rows)
'''

import json
from dataclasses    import dataclass, field
from uuid           import UUID, uuid4

from sqlalchemy     import Connection, text


@dataclass
class Rows:
    agreement:      str
    courses:        dict[int, dict] = field(default_factory = dict)
    articulations:  list[dict]      = field(default_factory = list)
    expressions:    list[dict]      = field(default_factory = list)
    members:        list[dict]      = field(default_factory = list)
    warnings:       list[str]       = field(default_factory = list)


def flatten(agreement: str, articulations: list | str) -> Rows:
    '''
    Flattens an agreement's `articulations` array into table rows.

    :agreement:     The ASSIST agreement key, used to replace an agreement's rows on reload
    :articulations: `Agreement.articulations`: `ArticulationCell`s (major agreements),
                    `Department`s (department agreements), or the JSON string of either
    '''
    if isinstance(articulations, str):
        articulations = json.loads(articulations)

    rows = Rows(agreement)
    for entry in articulations or []:
        if 'articulation' in entry:                                 # ArticulationCell
            _articulation(rows, entry['articulation'], entry.get('templateCellId'))
        else:                                                       # Department
            for articulation in entry.get('articulations') or []:
                _articulation(rows, articulation, None)
    return rows


def save(connection: Connection, rows: Rows) -> None:
    '''
    Replaces everything stored for `rows.agreement`. Deleting an articulation
    cascades to its expressions, so a reload never leaves orphaned trees.
    '''
    connection.execute(text('''
        INSERT INTO courses (id, prefix, number, title, department, min_units, max_units)
        VALUES (:id, :prefix, :number, :title, :department, :min_units, :max_units)
        ON CONFLICT (id) DO UPDATE SET
            prefix      = EXCLUDED.prefix,
            number      = EXCLUDED.number,
            title       = EXCLUDED.title,
            department  = EXCLUDED.department,
            min_units   = EXCLUDED.min_units,
            max_units   = EXCLUDED.max_units
    '''), list(rows.courses.values()))

    connection.execute(text('DELETE FROM articulations WHERE agreement = :agreement'),
                       {'agreement': rows.agreement})

    for table, data in (('articulations',      rows.articulations),
                        ('expressions',        rows.expressions),
                        ('expression_courses', rows.members)):
        if data:
            columns = ', '.join(data[0])
            values  = ', '.join(f':{column}' for column in data[0])
            connection.execute(text(f'INSERT INTO {table} ({columns}) VALUES ({values}) '
                                    'ON CONFLICT DO NOTHING'), data)


# ---------------------------------------------------------------------------- #

def _articulation(rows: Rows, articulation: dict, template_cell: str | None) -> None:
    id      = uuid4()
    kind    = articulation['type']
    sending = articulation.get('sendingArticulation') or {}

    rows.articulations.append({
        'id':                       id,
        'agreement':                rows.agreement,
        'template_cell':            UUID(template_cell) if template_cell else None,
        'position':                 len(rows.articulations),
        'receiving_type':           kind,
        'receiving_label':          _receiving_label(articulation),
        'no_articulation_reason':   sending.get('noArticulationReason'),
    })

    _receiving(rows, id, articulation)
    _sending(rows, id, sending)


def _receiving(rows: Rows, articulation: UUID, receiving: dict) -> None:
    '''A receiving course becomes a one-course And; a series keeps its own conjunction.'''
    if receiving['type'] == 'Course' and receiving.get('course'):
        root = _node(rows, articulation, 'receiving', 'And')
        _member(rows, root, receiving['course'], 0)

    elif receiving['type'] == 'Series' and receiving.get('series'):
        series = receiving['series']
        root   = _node(rows, articulation, 'receiving', series['conjunction'])
        for position, course in enumerate(_ordered(series.get('courses'))):
            _member(rows, root, course, position)


def _sending(rows: Rows, articulation: UUID, sending: dict) -> None:
    items  = _ordered(sending.get('items'))
    groups = [item for item in items if item['type'] == 'CourseGroup' and item.get('items')]

    skipped = len(items) - len(groups)
    if skipped:
        rows.warnings.append(f'{articulation}: skipped {skipped} sending item(s) that are not course groups')
    if not groups:
        return

    # Single group: the group itself is the root
    if len(groups) == 1:
        root = _node(rows, articulation, 'sending', groups[0]['courseConjunction'])
        for position, course in enumerate(_courses(groups[0])):
            _member(rows, root, course, position)
        return

    # Several groups: And binds tighter than Or, so split into runs of
    # And-joined groups, then Or the runs together
    runs = [[groups[0]]]
    for i, conjunction in enumerate(_between(sending, groups)):
        if conjunction == 'And':
            runs[-1].append(groups[i + 1])
        else:
            runs.append([groups[i + 1]])

    if len(runs) == 1:
        root = _node(rows, articulation, 'sending', 'And')
        for position, group in enumerate(runs[0]):
            _group(rows, articulation, root, group, position)
        return

    root = _node(rows, articulation, 'sending', 'Or')
    for position, run in enumerate(runs):
        if len(run) == 1:
            _group(rows, articulation, root, run[0], position)
        else:
            parent = _node(rows, articulation, 'sending', 'And', root, position)
            for inner, group in enumerate(run):
                _group(rows, articulation, parent, group, inner)


def _between(sending: dict, groups: list[dict]) -> list[str]:
    '''
    The conjunction between each adjacent pair of groups (`len(groups) - 1` entries).
    ASSIST gives these as ranges of item positions, usually one per adjacent
    pair, e.g. 0–1 Or, 1–2 Or.
    '''
    between: list[str | None] = [None] * (len(groups) - 1)
    for conjunction in sending.get('courseGroupConjunctions') or []:
        begin = conjunction['sendingCourseGroupBeginPosition']
        end   = conjunction['sendingCourseGroupEndPosition']
        for i in range(len(groups) - 1):
            if begin <= groups[i]['position'] and groups[i + 1]['position'] <= end:
                between[i] = conjunction['groupConjunction']

    # Groups with no conjunction between them are alternatives: in the cached
    # data these are transferability lists, honors/non-honors pairs (MATH 3B,
    # MATH 3BH), and requirement areas listing qualifying courses
    return [conjunction or 'Or' for conjunction in between]


def _group(rows: Rows, articulation: UUID, parent: UUID, group: dict, position: int) -> None:
    '''Places a course group under `parent`; a one-course group becomes just the course.'''
    courses = _courses(group)
    if len(courses) == 1:
        _member(rows, parent, courses[0], position)
        return

    node = _node(rows, articulation, 'sending', group['courseConjunction'], parent, position)
    for inner, course in enumerate(courses):
        _member(rows, node, course, inner)


def _node(rows: Rows, articulation: UUID, side: str, conjunction: str,
          parent: UUID | None = None, position: int = 0) -> UUID:
    id = uuid4()
    rows.expressions.append({
        'id':           id,
        'articulation': articulation,
        'side':         side,
        'parent':       parent,
        'position':     position,
        'conjunction':  conjunction,
    })
    return id


def _member(rows: Rows, expression: UUID, course: dict, position: int) -> None:
    id = course['courseIdentifierParentId']
    rows.courses[id] = {
        'id':           id,
        'prefix':       course['prefix'].strip(),
        'number':       str(course['courseNumber']).strip(),
        'title':        course.get('courseTitle'),
        'department':   course.get('department'),
        'min_units':    course.get('minUnits'),
        'max_units':    course.get('maxUnits'),
    }
    rows.members.append({'expression': expression, 'course': id, 'position': position})


def _courses(group: dict) -> list[dict]:
    return [item for item in _ordered(group.get('items')) if item['type'] == 'Course']


def _ordered(items: list | None) -> list[dict]:
    return sorted(items or [], key = lambda item: item.get('position') or 0)


def _receiving_label(articulation: dict) -> str | None:
    match articulation['type']:
        case 'Course':
            course = articulation.get('course') or {}
            return f"{course.get('prefix', '').strip()} {course.get('courseNumber', '')}".strip() or None
        case 'Series':
            return (articulation.get('series') or {}).get('name')
        case 'Requirement':
            return (articulation.get('requirement') or {}).get('name')
        case 'GeneralEducation':
            area = articulation.get('generalEducationArea') or {}
            return area.get('name') or area.get('code')
    return None
