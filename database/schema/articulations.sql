-- Articulations stored as AND/OR expression trees.
--
-- An articulation maps a receiving-side expression (a university course or
-- series) to a sending-side expression (community college courses). Each side
-- is a tree of expression nodes: a node joins its members with And or Or, and
-- each member is either a course (expression_courses) or a child node
-- (expressions.parent).
--
--   (CS 36 And CS 38) Or CS 40
--
--   expressions:         e1  Or   parent = NULL   <- root of the sending side
--                        e2  And  parent = e1
--   expression_courses:  e2 -> CS 36, e2 -> CS 38, e1 -> CS 40
--
-- Courses are the many-to-many part: one course can appear in any number of
-- expressions, across any number of articulations. Expression nodes, however,
-- are owned by exactly one articulation, so a parent pointer is enough to form
-- the tree, and deleting an articulation removes its whole tree.

CREATE TABLE IF NOT EXISTS courses (
    id          INT PRIMARY KEY,            -- ASSIST courseIdentifierParentId
    prefix      TEXT NOT NULL,
    number      TEXT NOT NULL,              -- text: '3AH', 'C1001H', ...
    title       TEXT,
    department  TEXT,
    min_units   NUMERIC(5, 2),
    max_units   NUMERIC(5, 2)
);

CREATE TABLE IF NOT EXISTS articulations (
    id                      UUID PRIMARY KEY,
    agreement               TEXT NOT NULL,  -- ASSIST key, e.g. '76/124/to/11/AllMajors'
    template_cell           UUID,           -- ArticulationCell.templateCellId (major agreements)
    position                INT  NOT NULL,  -- order within the agreement
    receiving_type          TEXT NOT NULL CHECK (receiving_type IN
                                ('Course', 'Series', 'Requirement', 'GeneralEducation', 'Transferability')),
    receiving_label         TEXT,           -- course/series/requirement/GE area name
    no_articulation_reason  TEXT            -- set when nothing articulates
);
CREATE INDEX IF NOT EXISTS articulations_agreement ON articulations (agreement);

CREATE TABLE IF NOT EXISTS expressions (
    id              UUID PRIMARY KEY,
    articulation    UUID NOT NULL REFERENCES articulations (id) ON DELETE CASCADE,
    side            TEXT NOT NULL CHECK (side IN ('receiving', 'sending')),
    parent          UUID REFERENCES expressions (id) ON DELETE CASCADE,
    position        INT  NOT NULL DEFAULT 0,  -- order among the parent's members
    conjunction     TEXT NOT NULL CHECK (conjunction IN ('And', 'Or')),
    CHECK (parent IS DISTINCT FROM id)
);
-- Exactly one root per side of an articulation
CREATE UNIQUE INDEX IF NOT EXISTS expressions_one_root
    ON expressions (articulation, side) WHERE parent IS NULL;
CREATE INDEX IF NOT EXISTS expressions_parent ON expressions (parent);

CREATE TABLE IF NOT EXISTS expression_courses (
    expression  UUID NOT NULL REFERENCES expressions (id) ON DELETE CASCADE,
    course      INT  NOT NULL REFERENCES courses (id),
    position    INT  NOT NULL,              -- shares ordering with child nodes
    PRIMARY KEY (expression, course)
);
-- "Where is this course used?" lookups
CREATE INDEX IF NOT EXISTS expression_courses_course ON expression_courses (course);


-- Does a set of completed courses satisfy an expression?
--   SELECT expression_satisfied(e.id, ARRAY[191353, 204250]) ...
CREATE OR REPLACE FUNCTION expression_satisfied(expr UUID, completed INT[])
RETURNS BOOLEAN LANGUAGE plpgsql STABLE AS $$
BEGIN
    RETURN (
        SELECT CASE e.conjunction WHEN 'And' THEN bool_and(m.ok)
                                  ELSE            bool_or(m.ok) END
        FROM expressions e
        CROSS JOIN LATERAL (
            SELECT ec.course = ANY (completed) AS ok
            FROM expression_courses ec
            WHERE ec.expression = e.id
            UNION ALL
            SELECT expression_satisfied(c.id, completed)
            FROM expressions c
            WHERE c.parent = e.id
        ) m
        WHERE e.id = expr
        GROUP BY e.conjunction
    );
END $$;


-- Human-readable form of an expression, for debugging:
--   '(CS 36 And CS 38) Or CS 40'
CREATE OR REPLACE FUNCTION expression_text(expr UUID)
RETURNS TEXT LANGUAGE plpgsql STABLE AS $$
BEGIN
    RETURN (
        SELECT string_agg(m.label, ' ' || e.conjunction || ' ' ORDER BY m.position)
        FROM expressions e
        CROSS JOIN LATERAL (
            SELECT ec.position, c.prefix || ' ' || c.number AS label
            FROM expression_courses ec
            JOIN courses c ON c.id = ec.course
            WHERE ec.expression = e.id
            UNION ALL
            SELECT ch.position, '(' || expression_text(ch.id) || ')'
            FROM expressions ch
            WHERE ch.parent = e.id
        ) m
        WHERE e.id = expr
        GROUP BY e.conjunction
    );
END $$;


-- One row per articulation with both sides as text
CREATE OR REPLACE VIEW articulation_summary AS
SELECT a.id,
       a.agreement,
       a.position,
       a.receiving_type,
       coalesce(expression_text(r.id), a.receiving_label)   AS receiving,
       coalesce(expression_text(s.id), a.no_articulation_reason,
                'No course articulated')                     AS sending,
       s.id                                                  AS sending_root
FROM articulations a
LEFT JOIN expressions r ON r.articulation = a.id AND r.side = 'receiving' AND r.parent IS NULL
LEFT JOIN expressions s ON s.articulation = a.id AND s.side = 'sending'   AND s.parent IS NULL;
