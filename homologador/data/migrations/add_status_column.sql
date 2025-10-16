-- Agregar columna status a la tabla homologations
ALTER TABLE homologations ADD COLUMN status TEXT DEFAULT 'Pendiente';

-- Crear índice para mejorar performance en consultas por status
CREATE INDEX IF NOT EXISTS idx_homologations_status ON homologations(status);

-- Actualizar registros existentes con estado por defecto
UPDATE homologations SET status = 'Pendiente' WHERE status IS NULL;