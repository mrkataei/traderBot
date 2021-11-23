-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 23, 2021 at 08:11 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aitrader`
--

-- --------------------------------------------------------

--
-- Table structure for table `analysis`
--

CREATE TABLE `analysis` (
  `id` int(5) NOT NULL,
  `name` char(10) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `analysis`
--

INSERT INTO `analysis` (`id`, `name`, `description`) VALUES
(1, 'emerald', NULL),
(2, 'ruby', NULL),
(3, 'diamond', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `coins`
--

CREATE TABLE `coins` (
  `id` int(5) NOT NULL,
  `coin` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `coins`
--

INSERT INTO `coins` (`id`, `coin`) VALUES
(1, 'BTCUSDT'),
(2, 'ETHUSDT'),
(3, 'ADAUSDT'),
(4, 'ETCUSDT'),
(5, 'BCHUSDT'),
(6, 'DOGEUSDT');

-- --------------------------------------------------------

--
-- Table structure for table `exchanges`
--

CREATE TABLE `exchanges` (
  `id` int(5) NOT NULL,
  `exchange` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `exchanges`
--

INSERT INTO `exchanges` (`id`, `exchange`) VALUES
(1, 'bitfinex');

-- --------------------------------------------------------

--
-- Table structure for table `plans`
--

CREATE TABLE `plans` (
  `id` int(5) NOT NULL,
  `plan` char(15) NOT NULL,
  `cost` double NOT NULL,
  `duration` int(5) NOT NULL,
  `description` text NOT NULL,
  `strategy_number` int(5) NOT NULL,
  `account_number` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `plans`
--

INSERT INTO `plans` (`id`, `plan`, `cost`, `duration`, `description`, `strategy_number`, `account_number`) VALUES
(1, 'freemium', 0, 30, 'for test', 1, 1),
(2, 'beginner', 10000000, 30, 'first plan', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `plan_payments`
--

CREATE TABLE `plan_payments` (
  `username` char(30) NOT NULL,
  `plan_id` int(5) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `cost` double NOT NULL,
  `is_pay` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `id` int(11) NOT NULL,
  `analysis_id` int(5) NOT NULL,
  `coin_id` int(5) NOT NULL,
  `timeframe_id` int(5) NOT NULL,
  `position` char(8) NOT NULL,
  `price` double NOT NULL,
  `risk` char(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `timeframes`
--

CREATE TABLE `timeframes` (
  `id` int(5) NOT NULL,
  `timeframe` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `timeframes`
--

INSERT INTO `timeframes` (`id`, `timeframe`) VALUES
(1, '30min'),
(2, '1hour'),
(3, '4hour'),
(4, '1day'),
(5, '1min');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `username` char(15) NOT NULL,
  `watchlist_id` int(15) NOT NULL,
  `recommendation_id_open` int(15) NOT NULL,
  `recommendation_id_close` int(15) DEFAULT NULL,
  `amount` double NOT NULL,
  `is_open` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `tutorials`
--

CREATE TABLE `tutorials` (
  `name` char(10) NOT NULL,
  `category` int(5) NOT NULL,
  `media` longblob NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `tutorials_category`
--

CREATE TABLE `tutorials_category` (
  `id` int(5) NOT NULL,
  `name` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tutorials_category`
--

INSERT INTO `tutorials_category` (`id`, `name`) VALUES
(1, 'exchange'),
(2, 'wallet'),
(3, 'technical'),
(4, 'bot');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` char(12) NOT NULL,
  `chat_id` varchar(15) NOT NULL,
  `role` char(10) NOT NULL DEFAULT 'user',
  `email` varchar(30) DEFAULT NULL,
  `phone` char(13) NOT NULL,
  `signup_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `is_online` tinyint(1) NOT NULL DEFAULT 0,
  `is_use_freemium` tinyint(1) NOT NULL DEFAULT 1,
  `valid_time_plan` timestamp NULL DEFAULT NULL,
  `plan_id` int(5) NOT NULL DEFAULT 1,
  `timeframe` int(5) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `chat_id`, `role`, `email`, `phone`, `signup_time`, `last_login`, `is_online`, `is_use_freemium`, `valid_time_plan`, `plan_id`, `timeframe`) VALUES
('kouroshataei', '1210507821', 'admin', NULL, '+989036928421', '2021-11-20 15:13:22', '2021-11-23 18:40:52', 1, 1, '2021-12-20 15:13:22', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_settings`
--

CREATE TABLE `user_settings` (
  `id` int(12) NOT NULL,
  `username` char(12) NOT NULL,
  `public` varchar(30) NOT NULL,
  `secret` varchar(30) NOT NULL,
  `exchange_id` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `id` int(12) NOT NULL,
  `user_setting_id` int(12) NOT NULL,
  `coin_id` int(5) NOT NULL,
  `username` char(30) NOT NULL,
  `analysis_id` int(5) NOT NULL,
  `amount` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analysis`
--
ALTER TABLE `analysis`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `coins`
--
ALTER TABLE `coins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exchanges`
--
ALTER TABLE `exchanges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `plans`
--
ALTER TABLE `plans`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `plan_payments`
--
ALTER TABLE `plan_payments`
  ADD KEY `plan_payments_username` (`username`),
  ADD KEY `plan_payments_plan_id` (`plan_id`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recommendations_coin_id` (`coin_id`),
  ADD KEY `recommendations_timeframe_id` (`timeframe_id`),
  ADD KEY `recommendations_analysis_id` (`analysis_id`);

--
-- Indexes for table `timeframes`
--
ALTER TABLE `timeframes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD KEY `transactions_username` (`username`),
  ADD KEY `transactions_whatchlist_id` (`watchlist_id`),
  ADD KEY `transactions_reccomendation_id_close` (`recommendation_id_close`);

--
-- Indexes for table `tutorials`
--
ALTER TABLE `tutorials`
  ADD PRIMARY KEY (`name`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `fk_category_id` (`category`);

--
-- Indexes for table `tutorials_category`
--
ALTER TABLE `tutorials_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `chat_id` (`chat_id`),
  ADD KEY `users_plans_id` (`plan_id`),
  ADD KEY `users_timeframe_id` (`timeframe`);

--
-- Indexes for table `user_settings`
--
ALTER TABLE `user_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`,`exchange_id`),
  ADD KEY `user_setting_exchange_id` (`exchange_id`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_setting_id` (`user_setting_id`,`coin_id`,`username`,`analysis_id`),
  ADD KEY `whatchlist_coin_id` (`coin_id`),
  ADD KEY `whatchlits_analysis_id` (`analysis_id`),
  ADD KEY `whatchlist_username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analysis`
--
ALTER TABLE `analysis`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `coins`
--
ALTER TABLE `coins`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `exchanges`
--
ALTER TABLE `exchanges`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `plans`
--
ALTER TABLE `plans`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `timeframes`
--
ALTER TABLE `timeframes`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tutorials_category`
--
ALTER TABLE `tutorials_category`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_settings`
--
ALTER TABLE `user_settings`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(12) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `plan_payments`
--
ALTER TABLE `plan_payments`
  ADD CONSTRAINT `plan_payments_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`),
  ADD CONSTRAINT `plan_payments_username` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Constraints for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD CONSTRAINT `recommendations_analysis_id` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`),
  ADD CONSTRAINT `recommendations_coin_id` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `recommendations_timeframe_id` FOREIGN KEY (`timeframe_id`) REFERENCES `timeframes` (`id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_reccomendation_id_close` FOREIGN KEY (`recommendation_id_close`) REFERENCES `recommendations` (`id`),
  ADD CONSTRAINT `transactions_reccomendation_id_open` FOREIGN KEY (`recommendation_id_close`) REFERENCES `recommendations` (`id`),
  ADD CONSTRAINT `transactions_username` FOREIGN KEY (`username`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `transactions_whatchlist_id` FOREIGN KEY (`watchlist_id`) REFERENCES `watchlist` (`id`);

--
-- Constraints for table `tutorials`
--
ALTER TABLE `tutorials`
  ADD CONSTRAINT `fk_category_id` FOREIGN KEY (`category`) REFERENCES `tutorials_category` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_plans_id` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`),
  ADD CONSTRAINT `users_timeframe_id` FOREIGN KEY (`timeframe`) REFERENCES `timeframes` (`id`);

--
-- Constraints for table `user_settings`
--
ALTER TABLE `user_settings`
  ADD CONSTRAINT `user_setting_exchange_id` FOREIGN KEY (`exchange_id`) REFERENCES `exchanges` (`id`),
  ADD CONSTRAINT `user_setting_username` FOREIGN KEY (`username`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `user_setting_username_fk` FOREIGN KEY (`username`) REFERENCES `users` (`username`);

--
-- Constraints for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `whatchlist_coin_id` FOREIGN KEY (`coin_id`) REFERENCES `coins` (`id`),
  ADD CONSTRAINT `whatchlist_user_setting_id` FOREIGN KEY (`user_setting_id`) REFERENCES `user_settings` (`id`),
  ADD CONSTRAINT `whatchlist_username` FOREIGN KEY (`username`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `whatchlits_analysis_id` FOREIGN KEY (`analysis_id`) REFERENCES `analysis` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;