USE car_gallery;

-- کاربران
INSERT INTO users(full_name,email,password,phone,role) VALUES
('علی احمدی','ali@gmail.com','123456','09120000001','admin'),
('محمد رضایی','mohammad@gmail.com','123456','09120000002','user'),
('سارا کریمی','sara@gmail.com','123456','09120000003','user');

-- برندها
INSERT INTO brands(name) VALUES
('BMW'),
('Mercedes-Benz'),
('Toyota'),
('Hyundai'),
('Kia'),
('Peugeot');

-- خودروها
INSERT INTO cars
(user_id,brand_id,model,year,price,mileage,color,fuel_type,transmission,description,status)
VALUES
(2,1,'320i',2022,2500000000,35000,'مشکی','بنزین','اتومات','بدون رنگ','approved'),
(3,3,'Corolla',2021,1800000000,42000,'سفید','بنزین','اتومات','بسیار تمیز','approved');

-- تصاویر
INSERT INTO car_images(car_id,image_url,is_main)
VALUES
(1,'bmw.jpg',1),
(2,'corolla.jpg',1);

-- علاقه مندی
INSERT INTO favorites(user_id,car_id)
VALUES
(2,2),
(3,1);

-- تاریخچه قیمت
INSERT INTO price_history(car_id,old_price,new_price)
VALUES
(1,2600000000,2500000000),
(2,1900000000,1800000000);