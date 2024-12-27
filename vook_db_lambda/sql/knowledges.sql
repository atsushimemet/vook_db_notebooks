SELECT
    a.id as knowledge_id,
    a.name as knowledge_name,
    a.brand_id,
    b.name as brand_name,
    c.name as line_name
FROM
    knowledges a
LEFT JOIN
    brands b
ON
    a.brand_id = b.id
LEFT JOIN
    `lines` c
ON
    a.line_id = c.id
