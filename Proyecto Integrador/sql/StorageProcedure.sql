--Procedimiento almacenado para agregar nuevos productos
DELIMITER //

CREATE PROCEDURE registro_productos(
    IN p_id            INT,
    IN p_ProductName   TEXT,
    IN p_Price         DECIMAL(10,2),
    IN p_CategoryID    INT,
    IN p_Class         TEXT,
    IN p_ModifyDate    DATE,
    IN p_Resistant     TEXT,
    IN p_IsAllergic    TEXT,
    IN p_VitalityDays  BIGINT
)
BEGIN
    -- 1) Verificar si ya existe un producto con ese nombre
    IF EXISTS (
        SELECT 1
        FROM products
        WHERE ProductName = p_ProductName
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: El producto ya se encuentra registrado.';
    ELSE
        -- 2) Si no existe, insertar normalmente
        INSERT INTO products (
            ProductID,
            ProductName,
            Price,
            CategoryID,
            Class,
            ModifyDate,
            Resistant,
            IsAllergic,
            VitalityDays
        )
        VALUES (
            p_id,
            p_ProductName,
            p_Price,
            p_CategoryID,
            p_Class,
            p_ModifyDate,
            p_Resistant,
            p_IsAllergic,
            p_VitalityDays
        );
    END IF;
END;
//

DELIMITER ;

CALL registro_productos(9999,'Dulce de leche',20,5,'Low','2024-04-02','Durable','Unknown',200);
select * from products
where ProductName='Dulce de leche';