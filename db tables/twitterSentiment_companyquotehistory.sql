------------------------------------------------------------------
--  TABLE twitterSentiment_companyquotehistory
------------------------------------------------------------------

CREATE TABLE `twitterSentiment_companyquotehistory`
(
   id           int(11),
   `date`       date,
   open         decimal(24, 4),
   high         decimal(24, 4),
   low          decimal(24, 4),
   close        decimal(24, 4),
   volume       decimal(24, 4),
   adjs_close   decimal(24, 4),
   symbol       varchar(10),
   company_id   int(11)
);


