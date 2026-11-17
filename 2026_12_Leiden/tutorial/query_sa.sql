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
    -- Only the 100 concepts from the Leipzig-Jakarta list
    -- p.core_concept like '%Tadmor-2009-100%'
    --    AND
    f.cldf_parameterReference = p.cldf_id
        AND
    f.cldf_languageReference = l.cldf_id
        AND
        (
            l.family IN ('Barbacoan', 'Chocoan', 'Guahiboan', 'Naduhup', 'Misumalpan', 'Cochimi-Yuman', 'Chumashan', 'Muskogean', 'Miwok-Costanoan', 'Chicham', 'Cahuapanan', 'Lencan')
            OR
            l.cldf_glottocode IN ('pume1238', 'paez1247', 'puin1248', 'natc1249', 'atak1252')
        )
        AND
    l.Selexion == 1
;