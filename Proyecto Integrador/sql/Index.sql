---INDICE, filtrado por fecha
CREATE INDEX idx_sales_salesdate 
  ON sales (SalesDate);

--- INDICE, filtrado por producto id
CREATE INDEX idx_sales_productid
  ON sales (ProductID);

--- INDICE COMPUESTO, filtrado por categoria y precio
CREATE INDEX idx_products_category_price
  ON products (CategoryID, Price);

---INDICE COMPUESTO, filtrado por producto y precio total
CREATE INDEX idx_sales_productid_totalprice
  ON sales (ProductID, TotalPrice);

--- INDICE COMPUESTO, filtrado por vendedor y precio total
CREATE INDEX idx_sales_person_total 
  ON sales (SalesPersonID, TotalPrice);