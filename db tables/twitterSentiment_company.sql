------------------------------------------------------------------
--  TABLE twitterSentiment_company
------------------------------------------------------------------

CREATE TABLE `twitterSentiment_company`
(
   id               int(11),
   symbol           varchar(10),
   name             varchar(100),
   `lastSale`       decimal(24, 4),
   `marketCap`      decimal(24, 4),
   `adrTso`         varchar(20),
   `ipoYear`        varchar(4),
   sector           varchar(100),
   industry         varchar(200),
   `summaryQuote`   varchar(200),
   exchange         varchar(10),
   date_extracted   datetime(6)
);


