-- Actualizar vista v_homologations_with_user para incluir el campo status
DROP VIEW IF EXISTS v_homologations_with_user;

CREATE VIEW v_homologations_with_user AS
SELECT 
    h.id,
    h.real_name,
    h.logical_name,
    h.kb_url,
    h.kb_sync,
    h.homologation_date,
    h.has_previous_versions,
    h.repository_location,
    h.details,
    h.status,
    u.username as created_by_username,
    u.full_name as created_by_full_name,
    h.created_at,
    h.updated_at
FROM homologations h
JOIN users u ON h.created_by = u.id
WHERE u.is_active = 1;