-- Choose rows you want to extract
SELECT
    l.cldf_name,
    l.cldf_latitude,
    l.cldf_longitude,
    l.cldf_glottocode,
    l.family,
    p.cldf_name,
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
    p.core_concept like '%Tadmor-2009-100%'
        AND
    f.cldf_parameterReference = p.cldf_id
        AND
    f.cldf_languageReference = l.cldf_id
        AND
    l.family IN ('Bosavi', 'Guahiboan', 'Bosavi', 'Saharan', 'Tungusic', 'Songhay')
;