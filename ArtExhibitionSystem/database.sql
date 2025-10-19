-- Create paintings table
CREATE TABLE paintings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,  -- e.g., 'Oil', 'Watercolor', 'Abstract'
    artist VARCHAR(255) NOT NULL,
    description TEXT,
    image_path VARCHAR(500)  -- Path to image, e.g., 'static/images/painting1.jpg'
);

-- Insert sample data (optional, for testing)
INSERT INTO paintings (title, type, artist, description, image_path) VALUES
('Sunset Over Mountains', 'Oil', 'John Doe', 'A vibrant oil painting of a sunset.', 'static/images/sample1.jpg'),
('Abstract Waves', 'Abstract', 'Jane Smith', 'Modern abstract art representing ocean waves.', 'static/images/sample2.jpg');

-- Create admins table (for basic admin login; hardcoded for simplicity)
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL  -- In real app, hash this!
);

-- Insert sample admin (username: admin, password: admin123)
INSERT INTO admins (username, password) VALUES ('admin', 'admin123');