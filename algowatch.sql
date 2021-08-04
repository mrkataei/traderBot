-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 04, 2021 at 12:48 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.1

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
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `amount` double NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

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
-- Table structure for table `indicators`
--

CREATE TABLE `indicators` (
  `name` char(30) CHARACTER SET utf8 NOT NULL,
  `id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `indicators`
--

INSERT INTO `indicators` (`name`, `id`) VALUES
('ichimoku', 1);

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
  `chat_id` char(12) DEFAULT NULL,
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
('kouroshataei', '1210507821', '23a4c6b99fe5eb158062de39946c048ba768bdd20e11503f14a2c03e848a49d09f0a0b900d600e57170eb8f13f48a3ed6090e4549acfa8bf5a865b251d026663', 15920, 'admin', 1, 'qoli', '2021-08-02 18:31:33');

-- --------------------------------------------------------

--
-- Table structure for table `user_indicators`
--

CREATE TABLE `user_indicators` (
  `id` int(12) NOT NULL,
  `user` char(30) CHARACTER SET utf8mb4 NOT NULL,
  `indicator_id` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `user_indicators`
--

INSERT INTO `user_indicators` (`id`, `user`, `indicator_id`) VALUES
(1, 'kouroshataei', 1);

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
(1, 'kouroshataei', 15),
(2, 'kouroshataei', 9);

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
('kouroshataei', 1, 'my_watchlist', 1);

--
-- Indexes for dumped tables
--

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
-- Indexes for table `indicators`
--
ALTER TABLE `indicators`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `operations`
--
ALTER TABLE `operations`
  ADD PRIMARY KEY (`id`);

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
  ADD PRIMARY KEY (`username`),
  ADD KEY `users_ibfk_1` (`question_id`);

--
-- Indexes for table `user_indicators`
--
ALTER TABLE `user_indicators`
  ADD PRIMARY KEY (`id`),
  ADD KEY `indicator_id` (`indicator_id`),
  ADD KEY `username_indi` (`user`);

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
  ADD KEY `username` (`user`),
  ADD KEY `coin_id` (`coin_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `indicators`
--
ALTER TABLE `indicators`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `operations`
--
ALTER TABLE `operations`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
-- AUTO_INCREMENT for table `user_indicators`
--
ALTER TABLE `user_indicators`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_timeframe`
--
ALTER TABLE `user_timeframe`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bank`
--
ALTER TABLE `bank`
  ADD CONSTRAINT `username_bank` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

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
-- Constraints for table `user_indicators`
--
ALTER TABLE `user_indicators`
  ADD CONSTRAINT `indicator_id` FOREIGN KEY (`indicator_id`) REFERENCES `indicators` (`id`),
  ADD CONSTRAINT `username_indi` FOREIGN KEY (`user`) REFERENCES `users` (`username`);

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