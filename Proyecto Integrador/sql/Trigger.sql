--TRIGGER PARA VALIDAR EL PRECIO TOTAL
DELIMITER //

CREATE TRIGGER validate_totalprice_before_insert
BEFORE INSERT ON sales
FOR EACH ROW
BEGIN
    DECLARE unit_price DECIMAL(10,2);
    -- Obtengo el precio unitario del producto que estoy insertando
    SELECT Price 
      INTO unit_price 
    FROM products 
    WHERE ProductID = NEW.ProductID;
    
    -- Calculo cuál debería ser el total (cantidad * precio unitario - descuento)
    IF NEW.TotalPrice <> (NEW.Quantity * unit_price - COALESCE(NEW.Discount, 0)) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: TotalPrice no coincide con Quantity * Precio - Discount.';
    END IF;
END;
//

DELIMITER ;

--Vamos a probarlo (caso de que funciona mal)
INSERT INTO sales (
    SalesID, 
    SalesPersonID, 
    CustomerID, 
    ProductID, 
    Quantity, 
    Discount, 
    TotalPrice,            -- ahora sí coincide
    SalesDate, 
    TransactionNumber
)
VALUES (
    99999, 
    1, 
    33133, 
    12, 
    2, 
    0.1,
    500,                -- 2 * 12 *0.1 = 21.60
    '2025-03-15 12:00:00', 
    'TX-TEST-0001'
);