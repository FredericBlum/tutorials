-- Choose rows you want to extract
SELECT
    l.cldf_name,
    l.cldf_latitude,
    l.cldf_longitude,
    l.cldf_glottocode,
    l.family,
    p.concepticon_gloss,
    f.cldf_form,
    f.cldf_segments
-- Choose tables from which to extract
FROM
    formtable AS f,
    languagetable AS l,
    parametertable AS p
-- Set conditions and merger
WHERE
    f.cldf_parameterReference = p.cldf_id
        AND
    f.cldf_languageReference = l.cldf_id
        AND
        (
            l.family IN ()
            OR
            l.cldf_glottocode IN ()
        )
;