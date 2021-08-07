-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 07, 2021 at 11:34 AM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `algowatch`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis`
--

CREATE TABLE `analysis` (
  `id` int(11) NOT NULL,
  `name` char(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `analysis`
--

INSERT INTO `analysis` (`id`, `name`) VALUES
(1, 'ichimoku');

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `amount` double NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`user`, `amount`) VALUES
('kourosh', 10),
('kouroshataei', 1323545.6565);

-- --------------------------------------------------------

--
-- Table structure for table `coins`
--

CREATE TABLE `coins` (
  `id` int(11) NOT NULL,
  `coin` varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `coins`
--

INSERT INTO `coins` (`id`, `coin`) VALUES
(1, 'BTCUSDT'),
(2, 'ETHUSDT');

-- --------------------------------------------------------

--
-- Table structure for table `operations`
--

CREATE TABLE `operations` (
  `id` int(12) NOT NULL,
  `name` char(10) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `operations`
--

INSERT INTO `operations` (`id`, `name`) VALUES
(1, 'deposit'),
(2, 'withdrawal');

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `coin_id` int(11) NOT NULL,
  `analysis_id` int(11) NOT NULL,
  `position` char(12) NOT NULL,
  `target_price` double NOT NULL,
  `current_price` double NOT NULL,
  `timeframe_id` int(11) NOT NULL,
  `cost_price` double NOT NULL,
  `risk` char(12) NOT NULL,
  `timestmp` timestamp NOT NULL DEFAULT current_timestamp(),
  `id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `recommendations`
--

INSERT INTO `recommendations` (`coin_id`, `analysis_id`, `position`, `target_price`, `current_price`, `timeframe_id`, `cost_price`, `risk`, `timestmp`, `id`) VALUES
(1, 1, 'buy', 2250, 2200, 2, 1.5, 'high', '2021-08-07 08:46:22', 1);

-- --------------------------------------------------------

--
-- Table structure for table `score_analysis`
--

CREATE TABLE `score_analysis` (
  `recom_id` int(12) NOT NULL,
  `score` int(5) NOT NULL,
  `user` char(30) NOT NULL,
  `is_used` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `score_analysis`
--

INSERT INTO `score_analysis` (`recom_id`, `score`, `user`, `is_used`) VALUES
(1, 4, 'kourosh', 1);

-- --------------------------------------------------------

--
-- Table structure for table `secrity_question`
--

CREATE TABLE `secrity_question` (
  `id` int(11) NOT NULL,
  `question` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `secrity_question`
--

INSERT INTO `secrity_question` (`id`, `question`) VALUES
(1, 'What is the name of your first teacher?'),
(2, 'Wich city did you born?');

-- --------------------------------------------------------

--
-- Table structure for table `timeframes`
--

CREATE TABLE `timeframes` (
  `id` int(11) NOT NULL,
  `timeframe` varchar(12) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `timeframes`
--

INSERT INTO `timeframes` (`id`, `timeframe`) VALUES
(1, '1min'),
(2, '3min'),
(3, '5min'),
(4, '15min'),
(5, '30min'),
(6, '1hour'),
(7, '2hour'),
(8, '4hour'),
(9, '6hour'),
(10, '8hour'),
(11, '12hour'),
(12, '1day'),
(13, '3day'),
(14, 'weekly'),
(15, 'monthly');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `id` int(12) NOT NULL,
  `operation` int(12) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `amount` double NOT NULL,
  `detail` text COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` char(30) NOT NULL,
  `chat_id` char(12) NOT NULL,
  `password` char(255) NOT NULL,
  `salt` int(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `question_id` int(11) NOT NULL,
  `question_answer` varchar(254) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `chat_id`, `password`, `salt`, `role`, `question_id`, `question_answer`, `timestamp`) VALUES
('kourosh', '1079329555', 'a2c21f4bf5dd9245a0cda3addcc0df4d3a2bd3a63e93f1300250019a5b646fdd312e91514dc036bd2b1ae4aa4e9e96d3ed5e3e7de37ab0633b439e9c0d4aa5e4', 78066, 'user', 2, 'Ferdows', '2021-08-07 08:22:30'),
('kouroshataei', '1210507821', '93a898fa890e0a1d6370ce6715f241d08d83ffda7a7e4150feb91cff607683538d9ee7a45047a39354a21c9e9b1daf56b552d1966650062f23efa3a58a018a86', 89640, 'admin', 1, 'qoli', '2021-08-02 18:31:33');

-- --------------------------------------------------------

--
-- Table structure for table `user_analysis`
--

CREATE TABLE `user_analysis` (
  `id` int(12) NOT NULL,
  `user` char(30) NOT NULL,
  `analysis_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_analysis`
--

INSERT INTO `user_analysis` (`id`, `user`, `analysis_id`) VALUES
(9, 'kourosh', 1),
(10, 'kouroshataei', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_timeframe`
--

CREATE TABLE `user_timeframe` (
  `id` int(12) NOT NULL,
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `timeframe_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `user_timeframe`
--

INSERT INTO `user_timeframe` (`id`, `user`, `timeframe_id`) VALUES
(31, 'kouroshataei', 8),
(34, 'kourosh', 2);

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `coin_id` int(12) DEFAULT NULL,
  `name` char(40) COLLATE utf8_bin DEFAULT NULL,
  `id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `watchlist`
--

INSERT INTO `watchlist` (`user`, `coin_id`, `name`, `id`) VALUES
('kouroshataei', 1, 'my', 10),
('kouroshataei', 2, 'my', 11),
('kourosh', 2, 'crypto', 18),
('kourosh', 1, 'crypto', 19);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis`
--
ALTER TABLE `analysis`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`user`);

--
-- Indexes for table `coins`
--
ALTER TABLE `coins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `operations`
--
ALTER TABLE `operations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coin_id_recom` (`coin_id`),
  ADD KEY `analysis_id_recom` (`analysis_id`),
  ADD KEY `timeframe_id_recom` (`timeframe_id`);

--
-- Indexes for table `score_analysis`
--
ALTER TABLE `score_analysis`
  ADD UNIQUE KEY `recom_id` (`recom_id`,`user`),
  ADD KEY `user_score` (`user`);

--
-- Indexes for table `secrity_question`
--
ALTER TABLE `secrity_question`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `timeframes`
--
ALTER TABLE `timeframes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username_tran` (`user`),
  ADD KEY `operation_id` (`operation`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`,`chat_id`),
  ADD UNIQUE KEY `chat_id` (`chat_id`),
  ADD KEY `users_ibfk_1` (`question_id`);

--
-- Indexes for table `user_analysis`
--
ALTER TABLE `user_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `analysis_username` (`user`),
  ADD KEY `analysis_id` (`analysis_id`);

--
-- Indexes for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_timeframe_username` (`user`),
  ADD KEY `user_timeframe_timeframe_id` (`timeframe_id`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user` (`user`,`coin_id`),
  ADD KEY `username` (`user`),
  ADD KEY `coin_id` (`coin_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis`
--
ALTER TABLE `analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `operations`
--
ALTER TABLE `operations`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `timeframes`
--
ALTER TABLE `timeframes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_analysis`
--
ALTER TABLE `user_analysis`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bank`
--
ALTER TABLE `bank`
  ADD CONSTRAINT `username_bank` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD CONSTRAINT `analysis_id_recom` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `coin_id_recom` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `timeframe_id_recom` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`);

--
-- Constraints for table `score_analysis`
--
ALTER TABLE `score_analysis`
  ADD CONSTRAINT `recom_id_score` FOREIGN KEY (`recom_id`) REFERENCES `recommendations` (`id`),
  ADD CONSTRAINT `user_score` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `operation_id` FOREIGN KEY (`operation`) REFERENCES `operations` (`id`),
  ADD CONSTRAINT `username_tran` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `secrity_question` (`id`);

--
-- Constraints for table `user_analysis`
--
ALTER TABLE `user_analysis`
  ADD CONSTRAINT `analysis_id` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `analysis_username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  ADD CONSTRAINT `user_timeframe_timeframe_id` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`),
  ADD CONSTRAINT `user_timeframe_username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

--
-- Constraints for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `coin_id` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `username` FOREIGN KEY (`user`) REFERENCES `users` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;