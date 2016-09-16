------------------------------------------------------------------
--  TABLE twitterSentiment_companyaltmanzscore
------------------------------------------------------------------

CREATE TABLE `twitterSentiment_companyaltmanzscore`
(
   id                      int(11),
   zscore                  decimal(10, 4),
   date_updated            datetime(6),
   company_id              int(11),
   company_financials_id   int(11)
);


