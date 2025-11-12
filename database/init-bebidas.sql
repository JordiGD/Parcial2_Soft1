-- Inicialización de la base de datos para VirtualCoffee Bebidas API
-- Este script se ejecuta automáticamente cuando se crea el contenedor

-- Crear extensión para UUID si es necesario
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla bebidas (será gestionada por Alembic, pero incluimos por seguridad)
CREATE TABLE IF NOT EXISTS bebidas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    size VARCHAR(10) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_bebidas_name ON bebidas(name);
CREATE INDEX IF NOT EXISTS idx_bebidas_size ON bebidas(size);
CREATE INDEX IF NOT EXISTS idx_bebidas_price ON bebidas(price);

-- Insertar datos de prueba
INSERT INTO bebidas (name, size, price) VALUES 
    ('Espresso', 'small', 2.50),
    ('Americano', 'medium', 3.00),
    ('Cappuccino', 'large', 4.50),
    ('Latte', 'medium', 4.00),
    ('Mocha', 'large', 5.00),
    ('Macchiato', 'small', 3.50),
    ('Frappuccino', 'large', 5.50),
    ('Cold Brew', 'medium', 3.75),
    ('Espresso con Leche', 'small', 2.75),
    ('Café Bombón', 'medium', 4.25)
ON CONFLICT DO NOTHING;

-- Crear función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Crear trigger para actualizar timestamp
DROP TRIGGER IF EXISTS update_bebidas_updated_at ON bebidas;
CREATE TRIGGER update_bebidas_updated_at
    BEFORE UPDATE ON bebidas
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Mensaje de confirmación
SELECT 'VirtualCoffee Bebidas Database initialized successfully!' as status;