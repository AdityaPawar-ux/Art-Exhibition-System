-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 12, 2025 at 01:04 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `art_exhibition`
--

-- --------------------------------------------------------

--
-- Table structure for table `about_content`
--

CREATE TABLE `about_content` (
  `id` int(11) NOT NULL DEFAULT 1,
  `content` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `about_content`
--

INSERT INTO `about_content` (`id`, `content`) VALUES
(1, 'This is an art exhibition management system built with Python, Flask, HTML/CSS, and MySQL. It allows viewing, adding, and managing paintings. Welcome to our virtual gallery!\r\nThis project is made by\r\n\r\n\r\n --Aditya Pawar from TY- BBA CA');

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`id`, `name`, `email`, `message`, `created_at`) VALUES
(1, 'Sujal Gangapure', 'sujal@gmail.com', 'I just checked out your web application, and it looks fantastic! The design is sleek, and everything flows smoothly. Great job on all the features! Can\'t wait to see it evolve!', '2025-10-06 15:36:29'),
(2, 'Darshan ', 'darshan@gmail.com', 'this u have created is one of the best pages i have reached out and the webpage created by owner and the best part is the paintings are awesome...', '2025-10-07 12:09:04'),
(3, 'Jaypal Ronge', 'jaypal@gmail.com', 'I like this website and i loved it how the paintings are and one the rarest painting is also there ', '2025-10-10 09:34:00');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `painting_id` int(11) NOT NULL,
  `purchase_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(20) DEFAULT 'Pending',
  `name` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `painting_id`, `purchase_date`, `status`, `name`, `address`, `payment_method`) VALUES
(11, 1, 12, '2025-10-12 10:43:28', 'Pending', 'vinyak', 'Kothrud Pune-411014', 'COD'),
(12, 4, 22, '2025-10-12 10:47:58', 'Shipped', 'Kashesh Agarwal', 'Sainikiwadi,pune-14,Maharastra ', 'COD');

-- --------------------------------------------------------

--
-- Table structure for table `paintings`
--

CREATE TABLE `paintings` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `paintings`
--

INSERT INTO `paintings` (`id`, `title`, `type`, `artist`, `description`, `image_path`, `price`) VALUES
(10, 'The Mona Lisa ', 'Watercolor', 'Leonardo Da Vinci', 'A woman with an enigmatic smile sits against a distant landscape in Leonardo da Vinci\'s famous Renaissance portrait, her mysterious expression and direct gaze captivating viewers for over 500 years.', '\\static\\images\\art1.jpeg', 100001.00),
(11, 'The Marvel ', 'Watercolor', 'SujalX', 'This is One of the painting that is been given tribute to marvel \r\nAvengers Assemble ', '\\static\\images\\art12.jpg', 20000.00),
(12, 'Night Scenery ', 'Other', 'Raj', 'Night Painting', '\\static\\images\\art2.jpg', 1000.00),
(13, 'The Orange Block', 'Abstract', 'Numan', 'This is the Orange Abstracted Painting.', '\\static\\images\\art3.jpg', 500.00),
(14, 'Stoic ', 'Other', 'Marcus Aurelius', 'This is one of the Stoic Philosopher ', '\\static\\images\\art4.jpg', 2000.00),
(15, 'The Autumn ', 'Abstract', 'Darshan', 'This is the autumn season  painting mainly we can see this in Russia ..', '\\static\\images\\art5.jpg', 3000.00),
(16, 'F1', 'Abstract', 'Raunak', 'This painting is tribute to our F1 players', '\\static\\images\\art6.jpg', 50000.00),
(17, 'THE UNIVERSE ', 'Watercolor', 'Shradha Sagar', 'This painting is realted to all Indian Gods ', '\\static\\images\\art7.jpg', 6000.00),
(18, 'Stand Alone', 'Watercolor', 'KasheshUx', 'Simple Elegant Painting', '\\static\\images\\art8.jpg', 4000.00),
(19, 'Stoics Oil', 'Oil', 'Rushikesh Dhore ', 'This painting is done using oil paints to make it Realistic', '\\static\\images\\art9.jpg', 8000.00),
(20, 'The Night Owlers', 'Oil', 'RiteshX', 'This is the Painting is related to Night where a farmer show\'s his life ', '\\static\\images\\art10.jpg', 9000.00),
(21, 'The Cities', 'Watercolor', 'JayyXR', 'This painting is related to sunset of buildings. ', '\\static\\images\\art11.jpg', 400.00),
(22, 'Audi R8', 'Watercolor', 'AdiiX', 'This painting is tribute for the launch of  new Audi R8', '\\static\\images\\art13.jpg', 1000000.00),
(23, 'sunset', 'Watercolor', 'adb', 'thid is best', '\\static\\images\\sample1.jpg', 4000.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `artist_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `artist_name`) VALUES
(1, 'Aditya', 'aditya@gmail.com', 'scrypt:32768:8:1$KeRkkm2g29oa4F5w$edbc5bde67707bf19bd2412f3baff7f20634869a16d7a3e2a8a4206b67a4bda3ce6fa944d288ea1c9b67cf273411de038c4af4da561b97740562fc263f4d81bc', 'Adiix'),
(2, 'Sujal', 'sujal@gmail.com', 'scrypt:32768:8:1$f4MsdJYdVdNnMBIV$bf14fdd585c769ef88fe8ac289b2d382ca37113162fbb4c544f1618e15ad9b1dfaa0ddab0fee654d3f17c4d0e0439dff547897ed653af536ec5a865adc3b45f5', 'SujalX'),
(3, 'Divjyot', 'divjyot@gmail.com', 'scrypt:32768:8:1$WLmvqgRPHT4TM5Jq$47a2ed82c2b8f4d62abef709ac567038c7bb01b72646c3947667aa69618f4ad192835cfb41142cc5dc7517ebce7f5a2693cd402d88d0c6a70d5554539332706e', 'Divjyot'),
(4, 'Kashesh ', 'kashesh20@gmail.com', 'scrypt:32768:8:1$eMZYISo2IsYoLVRy$f35f5d579df8e10670ffb6d2f6991d8b4edaac6dc46a6c99cd6e6c3b8fdb4a456912c1535d0f90a672246c4b2ca90f120d31760e4b0fc66c290a394e0f980e6a', 'KasheshUx');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `about_content`
--
ALTER TABLE `about_content`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `painting_id` (`painting_id`);

--
-- Indexes for table `paintings`
--
ALTER TABLE `paintings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `paintings`
--
ALTER TABLE `paintings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`painting_id`) REFERENCES `paintings` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
