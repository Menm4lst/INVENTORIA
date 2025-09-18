-- Migración para actualizar la vista v_homologations_with_user
-- Fecha: 18/09/2025

-- Eliminar la vista existente
DROP VIEW IF EXISTS v_homologations_with_user;

-- Recrear la vista con el nuevo campo
CREATE VIEW IF NOT EXISTS v_homologations_with_user AS
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
    u.username as created_by_username,
    u.full_name as created_by_full_name,
    h.created_at,
    h.updated_at
FROM homologations h
JOIN users u ON h.created_by = u.id
WHERE u.is_active = 1;