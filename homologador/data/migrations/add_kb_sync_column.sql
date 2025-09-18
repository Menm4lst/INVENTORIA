-- Migración para agregar la columna kb_sync a la tabla homologations
-- Fecha: 18/09/2025

-- Agregar la columna kb_sync si no existe
ALTER TABLE homologations ADD COLUMN kb_sync BOOLEAN DEFAULT 0;

-- Actualizar la fecha de modificación
UPDATE homologations SET updated_at = CURRENT_TIMESTAMP;