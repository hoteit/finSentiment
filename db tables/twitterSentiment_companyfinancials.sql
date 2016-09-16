------------------------------------------------------------------
--  TABLE twitterSentiment_companyfinancials
------------------------------------------------------------------

CREATE TABLE `twitterSentiment_companyfinancials`
(
   id                  int(11),
   quarter             varchar(1),
   `year`              varchar(4),
   total_assets        decimal(24, 4),
   total_liability     decimal(24, 4),
   current_assets      decimal(24, 4),
   current_liability   decimal(24, 4),
   retained_earnings   decimal(24, 4),
   market_capital      decimal(24, 4),
   ebitda              decimal(24, 4),
   sales               decimal(24, 4),
   stockprice          decimal(24, 4),
   date_extracted      datetime(6),
   company_id          int(11)
);


